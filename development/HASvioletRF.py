#!/usr/bin/python3
#
# HASvioletRF Library
#
#
#
#
# TO-DO:
#
#


#
# LIBRARIES
#

import sys
import time
import signal
import spidev
import RPi.GPIO as GPIO
import subprocess
from threading import RLock
import argparse
import configparser


#
# VARIABLES
#


#
#
# HOPERF RFM95 Static Variable Section
#
# Based on 
# https://github.com/ladecadence/pyRF95
# (C) 2016 David Pello Gonzalez for ASHAB
# (C) 2018 Caleb Johnson
#
# in turn is based on
# http://www.airspayce.com/mikem/arduino/RadioHead/
#
#




#
# CLASSES
#

class HASradio:
    def __init__(self):
        iniconfig = configparser.ConfigParser()
        iniconfig.sections()
        iniconfig.read('HASviolet.ini')
        try:
            self.gpio_rfm_cs = int(iniconfig["DEFAULT"]["gpio_rfm_cs"])
            self.gpio_rfm_irq = int(iniconfig["DEFAULT"]["gpio_rfm_irq"])
            self.node_address = int(iniconfig["DEFAULT"]["node_address"])
            self.freqmhz = float(iniconfig["DEFAULT"]["freqmhz"])
            self.txpwr = int(iniconfig["DEFAULT"]["txpwr"])
            self.modemcfg = str(iniconfig["DEFAULT"]["modemcfg"])
            self.mycall = str(iniconfig["DEFAULT"]["mycall"])
            self.ssid = int(iniconfig["DEFAULT"]["ssid"])
            self.beacon = str(iniconfig["DEFAULT"]["beacon"])
        except KeyError as e:
            raise LookupError("Error HASviolet.ini[DEFAULT] : {} missing.".format(str(e)))
            exit (1)
        self.station = self.mycall + "-" + str(self.ssid)
        self.rf95 = RFM95(cs=self.gpio_rfm_cs, int_pin=self.gpio_rfm_irq, reset_pin=None)
        self.rf95.set_frequency(self.freqmhz)
        self.rf95.set_tx_power(self.txpwr)
        self.rf95.init()
        self.receive = ""
        self.receive_rssi = ""
        self.receive_string = ""
        self.receive_ascii=""
        
    def cleanup(self):
        self.rf95.cleanup()  

    def rx(self):
        while not self.rf95.available():
            pass
        self.receive = self.rf95.recv()
        self.receive_rssi = str(int(self.rf95.last_rssi))
        self.receive_string = str(self.receive)
        self.receive_ascii=""
        for i in self.receive:
            self.receive_ascii=self.receive_ascii+chr(i)
        return
   
    def tx(self, data):
        # Send message
        self.rf95.send(self.str_to_data(data))
        self.rf95.wait_packet_sent()

class RFM95:
    def __init__(self, cs=0, int_pin=25, reset_pin=None):
        # init class
        self.FXOSC = 32000000.0
        self.FSTEP = FXOSC / 524288.0

        # Register names (LoRa Mode, from table 85)
        self.REG_00_FIFO = 0x00
        self.REG_01_OP_MODE = 0x01
        self.REG_02_RESERVED = 0x02
        self.REG_03_RESERVED = 0x03
        self.REG_04_RESERVED = 0x04
        self.REG_05_RESERVED = 0x05
        self.REG_06_FRF_MSB = 0x06
        self.REG_07_FRF_MID = 0x07
        self.REG_08_FRF_LSB = 0x08
        self.REG_09_PA_CONFIG = 0x09
        self.REG_0A_PA_RAMP = 0x0a
        self.REG_0B_OCP = 0x0b
        self.REG_0C_LNA = 0x0c
        self.REG_0D_FIFO_ADDR_PTR = 0x0d
        self.REG_0E_FIFO_TX_BASE_ADDR = 0x0e
        self.REG_0F_FIFO_RX_BASE_ADDR = 0x0f
        self.REG_10_FIFO_RX_CURRENT_ADDR = 0x10
        self.REG_11_IRQ_FLAGS_MASK = 0x11
        self.REG_12_IRQ_FLAGS = 0x12
        self.REG_13_RX_NB_BYTES = 0x13
        self.REG_14_RX_HEADER_CNT_VALUE_MSB = 0x14
        self.REG_15_RX_HEADER_CNT_VALUE_LSB = 0x15
        self.REG_16_RX_PACKET_CNT_VALUE_MSB = 0x16
        self.REG_17_RX_PACKET_CNT_VALUE_LSB = 0x17
        self.REG_18_MODEM_STAT = 0x18
        self.REG_19_PKT_SNR_VALUE = 0x19
        self.REG_1A_PKT_RSSI_VALUE = 0x1a
        self.REG_1B_RSSI_VALUE = 0x1b
        self.REG_1C_HOP_CHANNEL = 0x1c
        self.REG_1D_MODEM_CONFIG1 = 0x1d
        self.REG_1E_MODEM_CONFIG2 = 0x1e
        self.REG_1F_SYMB_TIMEOUT_LSB = 0x1f
        self.REG_20_PREAMBLE_MSB = 0x20
        self.REG_21_PREAMBLE_LSB = 0x21
        self.REG_22_PAYLOAD_LENGTH = 0x22
        self.REG_23_MAX_PAYLOAD_LENGTH = 0x23
        self.REG_24_HOP_PERIOD = 0x24
        self.REG_25_FIFO_RX_BYTE_ADDR = 0x25
        self.REG_26_MODEM_CONFIG3 = 0x26
        self.REG_28_FREQ_ERROR = 0x28
        self.REG_31_DETECT_OPT = 0x31
        self.REG_37_DETECTION_THRESHOLD = 0x37

        self.REG_40_DIO_MAPPING1 = 0x40
        self.REG_41_DIO_MAPPING2 = 0x41
        self.REG_42_VERSION = 0x42

        self.REG_4B_TCXO = 0x4b
        self.REG_4D_PA_DAC = 0x4d
        self.REG_5B_FORMER_TEMP = 0x5b
        self.REG_61_AGC_REF = 0x61
        self.REG_62_AGC_THRESH1 = 0x62
        self.REG_63_AGC_THRESH2 = 0x63
        self.REG_64_AGC_THRESH3 = 0x64

        # REG_01_OP_MODE                             0x01
        self.LONG_RANGE_MODE = 0x80
        self.ACCESS_SHARED_REG = 0x40
        self.MODE = 0x07
        self.MODE_SLEEP = 0x00
        self.MODE_STDBY = 0x01
        self.MODE_FSTX = 0x02
        self.MODE_TX = 0x03
        self.MODE_FSRX = 0x04
        self.MODE_RXCONTINUOUS = 0x05
        self.MODE_RXSINGLE = 0x06
        self.MODE_CAD = 0x07

        # REG_09_PA_CONFIG                           0x09
        self.PA_SELECT = 0x80
        self.MAX_POWER = 0x70
        self.OUTPUT_POWER = 0x0f

        # REG_0A_PA_RAMP                             0x0a
        self.LOW_PN_TX_PLL_OFF = 0x10
        self.PA_RAMP = 0x0f
        self.PA_RAMP_3_4MS = 0x00
        self.PA_RAMP_2MS = 0x01
        self.PA_RAMP_1MS = 0x02
        self.PA_RAMP_500US = 0x03
        self.PA_RAMP_250US = 0x0
        self.PA_RAMP_125US = 0x05
        self.PA_RAMP_100US = 0x06
        self.PA_RAMP_62US = 0x07
        self.PA_RAMP_50US = 0x08
        self.PA_RAMP_40US = 0x09
        self.PA_RAMP_31US = 0x0a
        self.PA_RAMP_25US = 0x0b
        self.PA_RAMP_20US = 0x0c
        self.PA_RAMP_15US = 0x0d
        self.PA_RAMP_12US = 0x0e
        self.PA_RAMP_10US = 0x0f

        # REG_0B_OCP                                 0x0b
        self.OCP_ON = 0x20
        self.OCP_TRIM = 0x1f

        # REG_0C_LNA                                 0x0c
        self.LNA_GAIN = 0xe0
        self.LNA_BOOST = 0x03
        self.LNA_BOOST_DEFAULT = 0x00
        self.LNA_BOOST_150PC = 0x11

        # REG_11_IRQ_FLAGS_MASK                      0x11
        self.RX_TIMEOUT_MASK = 0x80
        self.RX_DONE_MASK = 0x40
        self.PAYLOAD_CRC_ERROR_MASK = 0x20
        self.VALID_HEADER_MASK = 0x10
        self.TX_DONE_MASK = 0x08
        self.CAD_DONE_MASK = 0x04
        self.FHSS_CHANGE_CHANNEL_MASK = 0x02
        self.CAD_DETECTED_MASK = 0x01

        # REG_12_IRQ_FLAGS                           0x12
        self.RX_TIMEOUT = 0x80
        self.RX_DONE = 0x40
        self.PAYLOAD_CRC_ERROR = 0x20
        self.VALID_HEADER = 0x10
        self.TX_DONE = 0x08
        self.CAD_DONE = 0x04
        self.FHSS_CHANGE_CHANNEL = 0x02
        self.CAD_DETECTED = 0x01

        # REG_18_MODEM_STAT                          0x18
        self.RX_CODING_RATE = 0xe0
        self.MODEM_STATUS_CLEAR = 0x10
        self.MODEM_STATUS_HEADER_INFO_VALID = 0x08
        self.MODEM_STATUS_RX_ONGOING = 0x04
        self.MODEM_STATUS_SIGNAL_SYNCHRONIZED = 0x02
        self.MODEM_STATUS_SIGNAL_DETECTED = 0x01

        # REG_1C_HOP_CHANNEL                         0x1c
        self.PLL_TIMEOUT = 0x80
        self.RX_PAYLOAD_CRC_IS_ON = 0x40
        self.FHSS_PRESENT_CHANNEL = 0x3f

        # REG_1D_MODEM_CONFIG1                       0x1d
        self.BW_7K8HZ = 0x00
        self.BW_10K4HZ = 0x10
        self.BW_15K6HZ = 0x20
        self.BW_20K8HZ = 0x30
        self.BW_31K25HZ = 0x40
        self.BW_41K7HZ = 0x50
        self.BW_62K5HZ = 0x60
        self.BW_125KHZ = 0x70
        self.BW_250KHZ = 0x80
        self.BW_500KHZ = 0x90

        self.CODING_RATE_4_5 = 0x02
        self.CODING_RATE_4_6 = 0x04
        self.CODING_RATE_4_7 = 0x06
        self.CODING_RATE_4_8 = 0x08

        self.IMPLICIT_HEADER_MODE_ON = 0x00
        self.IMPLICIT_HEADER_MODE_OFF = 0x01

        # REG_1E_MODEM_CONFIG2                       0x1e
        self.SPREADING_FACTOR_64CPS = 0x60
        self.SPREADING_FACTOR_128CPS = 0x70
        self.SPREADING_FACTOR_256CPS = 0x80
        self.SPREADING_FACTOR_512CPS = 0x90
        self.SPREADING_FACTOR_1024CPS = 0xa0
        self.SPREADING_FACTOR_2048CPS = 0xb0
        self.SPREADING_FACTOR_4096CPS = 0xc0
        self.TX_CONTINUOUS_MODE_ON = 0x08
        self.TX_CONTINUOUS_MODE_OFF = 0x00
        self.RX_PAYLOAD_CRC_ON = 0x02
        self.RX_PAYLOAD_CRC_OFF = 0x00
        self.SYM_TIMEOUT_MSB = 0x03

        # REG_26_MODEM_CONFIG3
        self.AGC_AUTO_ON = 0x04
        self.AGC_AUTO_OFF = 0x00

        # REG_4D_PA_DAC                              0x4d
        self.PA_DAC_DISABLE = 0x04
        self.PA_DAC_ENABLE = 0x07

        self.MAX_MESSAGE_LEN = 255

        # default params
        self.Bw125Cr45Sf128 = (0x72, 0x74, 0x00)
        self.Bw500Cr45Sf128 = (0x92, 0x74, 0x00)
        self.Bw31_25Cr48Sf512 = (0x48, 0x94, 0x00)
        self.Bw125Cr48Sf4096 = (0x78, 0xc4, 0x00)

        # SPI
        self.SPI_WRITE_MASK = 0x80

        # Modes
        self.RADIO_MODE_INITIALISING = 0
        self.RADIO_MODE_SLEEP = 1
        self.RADIO_MODE_IDLE = 2
        self.RADIO_MODE_TX = 3
        self.RADIO_MODE_RX = 4
        self.RADIO_MODE_CAD = 5
        self.spi = spidev.SpiDev()
        self.spi_lock = RLock()
        self.cs = cs
        self.int_pin = int_pin
        self.reset_pin = reset_pin
        self.mode = self.RADIO_MODE_INITIALISING
        self.buf = []         # RX Buffer for interrupts
        self.buflen = 0       # RX Buffer length
        self.last_rssi = -99  # last packet RSSI
        self.last_snr = -99   # last packet SNR
        self.rx_bad = 0       # rx error count
        self.tx_good = 0      # tx packets sent
        self.rx_good = 0      # rx packets recv
        self.rx_buf_valid = False
        self._using_hf_port = None

    def init(self):
        # open SPI and initialize RF95
        self.spi.open(0, self.cs)
        self.spi.max_speed_hz = 488000
        self.spi.close()

        # set interrupt pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.int_pin, GPIO.IN)
        GPIO.add_event_detect(self.int_pin, GPIO.RISING, callback=self.handle_interrupt)

        # set reset pin
        if self.reset_pin is not None:
            GPIO.setup(self.reset_pin, GPIO.OUT)
            GPIO.output(self.reset_pin, GPIO.HIGH)

        # wait for reset
        time.sleep(0.05)

        # set sleep mode and LoRa mode
        self.spi_write(self.REG_01_OP_MODE, self.MODE_SLEEP | self.LONG_RANGE_MODE)

        time.sleep(0.01)
        # check if we are set
        if self.spi_read(self.REG_01_OP_MODE) != (self.MODE_SLEEP | self.LONG_RANGE_MODE):
            return False

        # set up FIFO
        self.spi_write(self.REG_0E_FIFO_TX_BASE_ADDR, 0)
        self.spi_write(self.REG_0F_FIFO_RX_BASE_ADDR, 0)

        # default mode
        self.set_mode_idle()

        self.set_modem_config(Bw125Cr45Sf128)
        self.set_preamble_length(8)

        return True

    def handle_interrupt(self, channel):
        # Read the interrupt register
        irq_flags = self.spi_read(self.REG_12_IRQ_FLAGS)

        if self.mode == self.RADIO_MODE_RX and irq_flags & (self.RX_TIMEOUT | self.PAYLOAD_CRC_ERROR):
            self.rx_bad = self.rx_bad + 1
        elif self.mode == self.RADIO_MODE_RX and irq_flags & self.RX_DONE:
            # packet received
            length = self.spi_read(self.REG_13_RX_NB_BYTES)
            # Reset the fifo read ptr to the beginning of the packet
            self.spi_write(self.REG_0D_FIFO_ADDR_PTR, self.spi_read(self.REG_10_FIFO_RX_CURRENT_ADDR))
            self.buf = self.spi_read_data(self.REG_00_FIFO, length)
            self.buflen = length
            # clear IRQ flags
            self.spi_write(self.REG_12_IRQ_FLAGS, 0xff)

            # save SNR
            self.last_snr = self.spi_read(self.REG_19_PKT_SNR_VALUE) / 4

            # save RSSI
            self.last_rssi = self.spi_read(self.REG_1A_PKT_RSSI_VALUE)

            # Adjust the RSSI, datasheet page 87
            if self.last_snr < 0:
                self.last_rssi += self.last_snr
            else:
                self.last_rssi = (self.last_rssi * 16) / 15

            if self._using_hf_port:
                self.last_rssi -= 157
            else:
                self.last_rssi -= 164

            # We have received a message
            self.rx_good = self.rx_good + 1
            self.rx_buf_valid = True
            self.set_mode_idle()
        elif self.mode == self.RADIO_MODE_TX and irq_flags & self.TX_DONE:
            self.tx_good = self.tx_good + 1
            self.set_mode_idle()
        elif self.mode == self.RADIO_MODE_CAD and irq_flags & self.CAD_DONE:
            self.cad = bool(irq_flags & self.CAD_DETECTED)
            self.set_mode_idle()

        # Clear all IRQ flags
        self.spi_write(self.REG_12_IRQ_FLAGS, 0xff)

    def spi_write(self, reg, data):
        self.spi_lock.acquire()
        self.spi.open(0, self.cs)
        # spi speed is reset on opening, change it
        self.spi.max_speed_hz = 488000
        # transfer one byte
        self.spi.xfer2([reg | self.SPI_WRITE_MASK, data])
        self.spi.close()
        self.spi_lock.release()

    def spi_read(self, reg):
        self.spi_lock.acquire()
        self.spi.open(0, self.cs)
        self.spi.max_speed_hz = 488000
        data = self.spi.xfer2([reg & ~self.SPI_WRITE_MASK, 0])
        self.spi.close()
        self.spi_lock.release()
        return data[1]

    def spi_write_data(self, reg, data):
        self.spi_lock.acquire()
        self.spi.open(0, self.cs)
        self.spi.max_speed_hz = 488000
        # transfer byte list
        self.spi.xfer2([reg | self.SPI_WRITE_MASK] + data)
        self.spi.close()
        self.spi_lock.release()

    def spi_read_data(self, reg, length):
        self.spi_lock.acquire()
        data = []
        self.spi.open(0, self.cs)
        self.spi.max_speed_hz = 488000
        # start address + amount of bytes to read
        data = self.spi.xfer2([reg & ~self.SPI_WRITE_MASK] + [0] * length)
        self.spi.close()
        self.spi_lock.release()
        # all but first byte
        return data[1:]

    def set_frequency(self, freq):
        freq_value = int((freq * 1000000.0) / FSTEP)
        self._using_hf_port = freq >= 779

        self.spi_write(self.REG_06_FRF_MSB, (freq_value >> 16) & 0xff)
        self.spi_write(self.REG_07_FRF_MID, (freq_value >> 8) & 0xff)
        self.spi_write(self.REG_08_FRF_LSB, freq_value & 0xff)

    def set_mode_idle(self):
        if self.mode != self.RADIO_MODE_IDLE:
            self.spi_write(self.REG_01_OP_MODE, self.MODE_STDBY)
            self.mode = self.RADIO_MODE_IDLE

    def sleep(self):
        if self.mode != self.RADIO_MODE_SLEEP:
            self.spi_write(self.REG_01_OP_MODE, self.MODE_SLEEP)
            self.mode = self.RADIO_MODE_SLEEP

        return True

    def set_mode_rx(self):
        if self.mode != self.RADIO_MODE_RX:
            self.spi_write(self.REG_01_OP_MODE, self.MODE_RXCONTINUOUS)
            self.spi_write(self.REG_40_DIO_MAPPING1, 0x00)
            self.mode = self.RADIO_MODE_RX

    def set_mode_tx(self):
        if self.mode != self.RADIO_MODE_TX:
            self.spi_write(self.REG_01_OP_MODE, self.MODE_TX)
            self.spi_write(self.REG_40_DIO_MAPPING1, 0x40)
            self.mode = self.RADIO_MODE_TX

        return True

    def set_mode_cad(self):
        if self.mode != self.RADIO_MODE_CAD:
            self.spi_write(self.REG_01_OP_MODE, MODE_CAD)
            self.spi_write(self.REG_40_DIO_MAPPING1, 0x80)
            self.mode = self.RADIO_MODE_CAD

    def set_tx_power(self, power):
        if power > 23:
            power = 23

        if power < 5:
            power = 5

        # A_DAC_ENABLE actually adds about 3dBm to all
        # power levels. We will us it for 21, 22 and 23dBm
        if power > 20:
            self.spi_write(self.REG_4D_PA_DAC, self.PA_DAC_ENABLE)
            power = power - 3
        else:
            self.spi_write(self.REG_4D_PA_DAC, self.PA_DAC_DISABLE)

        self.spi_write(self.REG_09_PA_CONFIG, self.PA_SELECT | (power - 5))

    # set a default mode
    def set_modem_config(self, config):
        self.spi_write(self.REG_1D_MODEM_CONFIG1, config[0])
        self.spi_write(self.REG_1E_MODEM_CONFIG2, config[1])
        self.spi_write(REG_26_MODEM_CONFIG3, config[2])

    # set custom mode
    def set_modem_config_custom(self,
        bandwidth = self.BW_125KHZ,
        coding_rate = self.CODING_RATE_4_5,
        implicit_header = self.IMPLICIT_HEADER_MODE_OFF,
        spreading_factor = self.SPREADING_FACTOR_128CPS,
        crc = self.RX_PAYLOAD_CRC_ON,
        continuous_tx = self.TX_CONTINUOUS_MODE_OFF,
        timeout = self.SYM_TIMEOUT_MSB,
        agc_auto = self.AGC_AUTO_OFF):

        self.spi_write(self.REG_1D_MODEM_CONFIG1,
            bandwidth | coding_rate | implicit_header)
        self.spi_write(self.REG_1E_MODEM_CONFIG2,
            spreading_factor | continuous_tx | crc | timeout)
        self.spi_write(self.REG_26_MODEM_CONFIG3, agc_auto)

    def set_preamble_length(self, length):
        self.spi_write(self.REG_20_PREAMBLE_MSB, length >> 8)
        self.spi_write(self.REG_21_PREAMBLE_LSB, length & 0xff)

    # send data list
    def send(self, data):
        if len(data) > self.MAX_MESSAGE_LEN:
            return False

        self.wait_packet_sent()
        self.set_mode_idle()
        # beggining of FIFO
        # self.spi_write(REG_0E_FIFO_TX_BASE_ADDR, 0)
        self.spi_write(self.REG_0D_FIFO_ADDR_PTR, 0)

        # write data
        self.spi_write_data(self.REG_00_FIFO, data)
        self.spi_write(self.REG_22_PAYLOAD_LENGTH, len(data))

        # put radio in TX mode
        self.set_mode_tx()
        return True

    def wait_packet_sent(self):
        while self.mode == self.RADIO_MODE_TX:
            pass
        return True

    def available(self):
        if self.mode == self.RADIO_MODE_TX:
            return False
        self.set_mode_rx()
        return self.rx_buf_valid

    def channel_active(self):
        if self.mode != self.RADIO_MODE_CAD:
            self.set_mode_cad()

        while self.mode == self.RADIO_MODE_CAD:
            pass

        return self.cad

    def clear_rx_buf(self):
        self.rx_buf_valid = False
        self.buflen = 0

    # receive data list
    def recv(self):
        if not self.available():
            return False
        data = self.buf
        self.clear_rx_buf()
        return data

    # cleans all GPIOs, etc
    def cleanup(self):
        if self.reset_pin:
            GPIO.output(self.reset_pin, GPIO.LOW)
            GPIO.cleanup(self.reset_pin)
        if self.int_pin:
            GPIO.cleanup(self.int_pin)

    # helper method to send bytes
    @staticmethod
    def bytes_to_data(bytelist):
        return list(bytelist)

    # helper method to send strings
    @staticmethod
    def str_to_data(string):
        return [ord(c) for c in string]

