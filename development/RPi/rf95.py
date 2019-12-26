# (C) 2016 David Pello Gonzalez for ASHAB
# (C) 2018 Caleb Johnson
# Based on code from the RadioHead Library:
# http://www.airspayce.com/mikem/arduino/RadioHead/
#
# This program is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.
# If not, see <http://www.gnu.org/licenses/>.

# TODO:
# - change constants to Enum members where appropriate
# - use threading.Condition instead of busy loops
# - timeout parameters on blocking functions
# - maybe switch libraries for GPIO + SPI
#   - native sysfs + epoll, supports other boards
# - asyncio integration?

import time
from threading import RLock

import spidev
import RPi.GPIO as GPIO

FXOSC = 32000000.0
FSTEP = FXOSC / 524288.0

# Register names (LoRa Mode, from table 85)
REG_00_FIFO = 0x00
REG_01_OP_MODE = 0x01
REG_02_RESERVED = 0x02
REG_03_RESERVED = 0x03
REG_04_RESERVED = 0x04
REG_05_RESERVED = 0x05
REG_06_FRF_MSB = 0x06
REG_07_FRF_MID = 0x07
REG_08_FRF_LSB = 0x08
REG_09_PA_CONFIG = 0x09
REG_0A_PA_RAMP = 0x0a
REG_0B_OCP = 0x0b
REG_0C_LNA = 0x0c
REG_0D_FIFO_ADDR_PTR = 0x0d
REG_0E_FIFO_TX_BASE_ADDR = 0x0e
REG_0F_FIFO_RX_BASE_ADDR = 0x0f
REG_10_FIFO_RX_CURRENT_ADDR = 0x10
REG_11_IRQ_FLAGS_MASK = 0x11
REG_12_IRQ_FLAGS = 0x12
REG_13_RX_NB_BYTES = 0x13
REG_14_RX_HEADER_CNT_VALUE_MSB = 0x14
REG_15_RX_HEADER_CNT_VALUE_LSB = 0x15
REG_16_RX_PACKET_CNT_VALUE_MSB = 0x16
REG_17_RX_PACKET_CNT_VALUE_LSB = 0x17
REG_18_MODEM_STAT = 0x18
REG_19_PKT_SNR_VALUE = 0x19
REG_1A_PKT_RSSI_VALUE = 0x1a
REG_1B_RSSI_VALUE = 0x1b
REG_1C_HOP_CHANNEL = 0x1c
REG_1D_MODEM_CONFIG1 = 0x1d
REG_1E_MODEM_CONFIG2 = 0x1e
REG_1F_SYMB_TIMEOUT_LSB = 0x1f
REG_20_PREAMBLE_MSB = 0x20
REG_21_PREAMBLE_LSB = 0x21
REG_22_PAYLOAD_LENGTH = 0x22
REG_23_MAX_PAYLOAD_LENGTH = 0x23
REG_24_HOP_PERIOD = 0x24
REG_25_FIFO_RX_BYTE_ADDR = 0x25
REG_26_MODEM_CONFIG3 = 0x26
REG_28_FREQ_ERROR = 0x28
REG_31_DETECT_OPT = 0x31
REG_37_DETECTION_THRESHOLD = 0x37

REG_40_DIO_MAPPING1 = 0x40
REG_41_DIO_MAPPING2 = 0x41
REG_42_VERSION = 0x42

REG_4B_TCXO = 0x4b
REG_4D_PA_DAC = 0x4d
REG_5B_FORMER_TEMP = 0x5b
REG_61_AGC_REF = 0x61
REG_62_AGC_THRESH1 = 0x62
REG_63_AGC_THRESH2 = 0x63
REG_64_AGC_THRESH3 = 0x64

# REG_01_OP_MODE                             0x01
LONG_RANGE_MODE = 0x80
ACCESS_SHARED_REG = 0x40
MODE = 0x07
MODE_SLEEP = 0x00
MODE_STDBY = 0x01
MODE_FSTX = 0x02
MODE_TX = 0x03
MODE_FSRX = 0x04
MODE_RXCONTINUOUS = 0x05
MODE_RXSINGLE = 0x06
MODE_CAD = 0x07

# REG_09_PA_CONFIG                           0x09
PA_SELECT = 0x80
MAX_POWER = 0x70
OUTPUT_POWER = 0x0f

# REG_0A_PA_RAMP                             0x0a
LOW_PN_TX_PLL_OFF = 0x10
PA_RAMP = 0x0f
PA_RAMP_3_4MS = 0x00
PA_RAMP_2MS = 0x01
PA_RAMP_1MS = 0x02
PA_RAMP_500US = 0x03
PA_RAMP_250US = 0x0
PA_RAMP_125US = 0x05
PA_RAMP_100US = 0x06
PA_RAMP_62US = 0x07
PA_RAMP_50US = 0x08
PA_RAMP_40US = 0x09
PA_RAMP_31US = 0x0a
PA_RAMP_25US = 0x0b
PA_RAMP_20US = 0x0c
PA_RAMP_15US = 0x0d
PA_RAMP_12US = 0x0e
PA_RAMP_10US = 0x0f

# REG_0B_OCP                                 0x0b
OCP_ON = 0x20
OCP_TRIM = 0x1f

# REG_0C_LNA                                 0x0c
LNA_GAIN = 0xe0
LNA_BOOST = 0x03
LNA_BOOST_DEFAULT = 0x00
LNA_BOOST_150PC = 0x11

# REG_11_IRQ_FLAGS_MASK                      0x11
RX_TIMEOUT_MASK = 0x80
RX_DONE_MASK = 0x40
PAYLOAD_CRC_ERROR_MASK = 0x20
VALID_HEADER_MASK = 0x10
TX_DONE_MASK = 0x08
CAD_DONE_MASK = 0x04
FHSS_CHANGE_CHANNEL_MASK = 0x02
CAD_DETECTED_MASK = 0x01

# REG_12_IRQ_FLAGS                           0x12
RX_TIMEOUT = 0x80
RX_DONE = 0x40
PAYLOAD_CRC_ERROR = 0x20
VALID_HEADER = 0x10
TX_DONE = 0x08
CAD_DONE = 0x04
FHSS_CHANGE_CHANNEL = 0x02
CAD_DETECTED = 0x01

# REG_18_MODEM_STAT                          0x18
RX_CODING_RATE = 0xe0
MODEM_STATUS_CLEAR = 0x10
MODEM_STATUS_HEADER_INFO_VALID = 0x08
MODEM_STATUS_RX_ONGOING = 0x04
MODEM_STATUS_SIGNAL_SYNCHRONIZED = 0x02
MODEM_STATUS_SIGNAL_DETECTED = 0x01

# REG_1C_HOP_CHANNEL                         0x1c
PLL_TIMEOUT = 0x80
RX_PAYLOAD_CRC_IS_ON = 0x40
FHSS_PRESENT_CHANNEL = 0x3f

# REG_1D_MODEM_CONFIG1                       0x1d
BW_7K8HZ = 0x00
BW_10K4HZ = 0x10
BW_15K6HZ = 0x20
BW_20K8HZ = 0x30
BW_31K25HZ = 0x40
BW_41K7HZ = 0x50
BW_62K5HZ = 0x60
BW_125KHZ = 0x70
BW_250KHZ = 0x80
BW_500KHZ = 0x90

CODING_RATE_4_5 = 0x02
CODING_RATE_4_6 = 0x04
CODING_RATE_4_7 = 0x06
CODING_RATE_4_8 = 0x08

IMPLICIT_HEADER_MODE_ON = 0x00
IMPLICIT_HEADER_MODE_OFF = 0x01

# REG_1E_MODEM_CONFIG2                       0x1e
SPREADING_FACTOR_64CPS = 0x60
SPREADING_FACTOR_128CPS = 0x70
SPREADING_FACTOR_256CPS = 0x80
SPREADING_FACTOR_512CPS = 0x90
SPREADING_FACTOR_1024CPS = 0xa0
SPREADING_FACTOR_2048CPS = 0xb0
SPREADING_FACTOR_4096CPS = 0xc0
TX_CONTINUOUS_MODE_ON = 0x08
TX_CONTINUOUS_MODE_OFF = 0x00
RX_PAYLOAD_CRC_ON = 0x02
RX_PAYLOAD_CRC_OFF = 0x00
SYM_TIMEOUT_MSB = 0x03

# REG_26_MODEM_CONFIG3
AGC_AUTO_ON = 0x04
AGC_AUTO_OFF = 0x00

# REG_4D_PA_DAC                              0x4d
PA_DAC_DISABLE = 0x04
PA_DAC_ENABLE = 0x07

MAX_MESSAGE_LEN = 255

# default params
Bw125Cr45Sf128 = (0x72, 0x74, 0x00)
Bw500Cr45Sf128 = (0x92, 0x74, 0x00)
Bw31_25Cr48Sf512 = (0x48, 0x94, 0x00)
Bw125Cr48Sf4096 = (0x78, 0xc4, 0x00)

# SPI
SPI_WRITE_MASK = 0x80

# Modes
RADIO_MODE_INITIALISING = 0
RADIO_MODE_SLEEP = 1
RADIO_MODE_IDLE = 2
RADIO_MODE_TX = 3
RADIO_MODE_RX = 4
RADIO_MODE_CAD = 5


class RF95:
    def __init__(self, cs=0, int_pin=25, reset_pin=None):
        # init class
        self.spi = spidev.SpiDev()
        self.spi_lock = RLock()
        self.cs = cs
        self.int_pin = int_pin
        self.reset_pin = reset_pin
        self.mode = RADIO_MODE_INITIALISING
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
        self.spi_write(REG_01_OP_MODE, MODE_SLEEP | LONG_RANGE_MODE)

        time.sleep(0.01)
        # check if we are set
        if self.spi_read(REG_01_OP_MODE) != (MODE_SLEEP | LONG_RANGE_MODE):
            return False

        # set up FIFO
        self.spi_write(REG_0E_FIFO_TX_BASE_ADDR, 0)
        self.spi_write(REG_0F_FIFO_RX_BASE_ADDR, 0)

        # default mode
        self.set_mode_idle()

        self.set_modem_config(Bw125Cr45Sf128)
        self.set_preamble_length(8)

        return True

    def handle_interrupt(self, channel):
        # Read the interrupt register
        irq_flags = self.spi_read(REG_12_IRQ_FLAGS)

        if self.mode == RADIO_MODE_RX and irq_flags & (RX_TIMEOUT | PAYLOAD_CRC_ERROR):
            self.rx_bad = self.rx_bad + 1
        elif self.mode == RADIO_MODE_RX and irq_flags & RX_DONE:
            # packet received
            length = self.spi_read(REG_13_RX_NB_BYTES)
            # Reset the fifo read ptr to the beginning of the packet
            self.spi_write(REG_0D_FIFO_ADDR_PTR, self.spi_read(REG_10_FIFO_RX_CURRENT_ADDR))
            self.buf = self.spi_read_data(REG_00_FIFO, length)
            self.buflen = length
            # clear IRQ flags
            self.spi_write(REG_12_IRQ_FLAGS, 0xff)

            # save SNR
            self.last_snr = self.spi_read(REG_19_PKT_SNR_VALUE) / 4

            # save RSSI
            self.last_rssi = self.spi_read(REG_1A_PKT_RSSI_VALUE)

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
        elif self.mode == RADIO_MODE_TX and irq_flags & TX_DONE:
            self.tx_good = self.tx_good + 1
            self.set_mode_idle()
        elif self.mode == RADIO_MODE_CAD and irq_flags & CAD_DONE:
            self.cad = bool(irq_flags & CAD_DETECTED)
            self.set_mode_idle()

        # Clear all IRQ flags
        self.spi_write(REG_12_IRQ_FLAGS, 0xff)

    def spi_write(self, reg, data):
        self.spi_lock.acquire()
        self.spi.open(0, self.cs)
        # spi speed is reset on opening, change it
        self.spi.max_speed_hz = 488000
        # transfer one byte
        self.spi.xfer2([reg | SPI_WRITE_MASK, data])
        self.spi.close()
        self.spi_lock.release()

    def spi_read(self, reg):
        self.spi_lock.acquire()
        self.spi.open(0, self.cs)
        self.spi.max_speed_hz = 488000
        data = self.spi.xfer2([reg & ~SPI_WRITE_MASK, 0])
        self.spi.close()
        self.spi_lock.release()
        return data[1]

    def spi_write_data(self, reg, data):
        self.spi_lock.acquire()
        self.spi.open(0, self.cs)
        self.spi.max_speed_hz = 488000
        # transfer byte list
        self.spi.xfer2([reg | SPI_WRITE_MASK] + data)
        self.spi.close()
        self.spi_lock.release()

    def spi_read_data(self, reg, length):
        self.spi_lock.acquire()
        data = []
        self.spi.open(0, self.cs)
        self.spi.max_speed_hz = 488000
        # start address + amount of bytes to read
        data = self.spi.xfer2([reg & ~SPI_WRITE_MASK] + [0] * length)
        self.spi.close()
        self.spi_lock.release()
        # all but first byte
        return data[1:]

    def set_frequency(self, freq):
        freq_value = int((freq * 1000000.0) / FSTEP)
        self._using_hf_port = freq >= 779

        self.spi_write(REG_06_FRF_MSB, (freq_value >> 16) & 0xff)
        self.spi_write(REG_07_FRF_MID, (freq_value >> 8) & 0xff)
        self.spi_write(REG_08_FRF_LSB, freq_value & 0xff)

    def set_mode_idle(self):
        if self.mode != RADIO_MODE_IDLE:
            self.spi_write(REG_01_OP_MODE, MODE_STDBY)
            self.mode = RADIO_MODE_IDLE

    def sleep(self):
        if self.mode != RADIO_MODE_SLEEP:
            self.spi_write(REG_01_OP_MODE, MODE_SLEEP)
            self.mode = RADIO_MODE_SLEEP

        return True

    def set_mode_rx(self):
        if self.mode != RADIO_MODE_RX:
            self.spi_write(REG_01_OP_MODE, MODE_RXCONTINUOUS)
            self.spi_write(REG_40_DIO_MAPPING1, 0x00)
            self.mode = RADIO_MODE_RX

    def set_mode_tx(self):
        if self.mode != RADIO_MODE_TX:
            self.spi_write(REG_01_OP_MODE, MODE_TX)
            self.spi_write(REG_40_DIO_MAPPING1, 0x40)
            self.mode = RADIO_MODE_TX

        return True

    def set_mode_cad(self):
        if self.mode != RADIO_MODE_CAD:
            self.spi_write(REG_01_OP_MODE, MODE_CAD)
            self.spi_write(REG_40_DIO_MAPPING1, 0x80)
            self.mode = RADIO_MODE_CAD

    def set_tx_power(self, power):
        if power > 23:
            power = 23

        if power < 5:
            power = 5

        # A_DAC_ENABLE actually adds about 3dBm to all
        # power levels. We will us it for 21, 22 and 23dBm
        if power > 20:
            self.spi_write(REG_4D_PA_DAC, PA_DAC_ENABLE)
            power = power - 3
        else:
            self.spi_write(REG_4D_PA_DAC, PA_DAC_DISABLE)

        self.spi_write(REG_09_PA_CONFIG, PA_SELECT | (power - 5))

    # set a default mode
    def set_modem_config(self, config):
        self.spi_write(REG_1D_MODEM_CONFIG1, config[0])
        self.spi_write(REG_1E_MODEM_CONFIG2, config[1])
        self.spi_write(REG_26_MODEM_CONFIG3, config[2])

    # set custom mode
    def set_modem_config_custom(self,
        bandwidth = BW_125KHZ,
        coding_rate = CODING_RATE_4_5,
        implicit_header = IMPLICIT_HEADER_MODE_OFF,
        spreading_factor = SPREADING_FACTOR_128CPS,
        crc = RX_PAYLOAD_CRC_ON,
        continuous_tx = TX_CONTINUOUS_MODE_OFF,
        timeout = SYM_TIMEOUT_MSB,
        agc_auto = AGC_AUTO_OFF):

        self.spi_write(REG_1D_MODEM_CONFIG1,
            bandwidth | coding_rate | implicit_header)
        self.spi_write(REG_1E_MODEM_CONFIG2,
            spreading_factor | continuous_tx | crc | timeout)
        self.spi_write(REG_26_MODEM_CONFIG3, agc_auto)

    def set_preamble_length(self, length):
        self.spi_write(REG_20_PREAMBLE_MSB, length >> 8)
        self.spi_write(REG_21_PREAMBLE_LSB, length & 0xff)

    # send data list
    def send(self, data):
        if len(data) > MAX_MESSAGE_LEN:
            return False

        self.wait_packet_sent()
        self.set_mode_idle()
        # beggining of FIFO
        # self.spi_write(REG_0E_FIFO_TX_BASE_ADDR, 0)
        self.spi_write(REG_0D_FIFO_ADDR_PTR, 0)

        # write data
        self.spi_write_data(REG_00_FIFO, data)
        self.spi_write(REG_22_PAYLOAD_LENGTH, len(data))

        # put radio in TX mode
        self.set_mode_tx()
        return True

    def wait_packet_sent(self):
        while self.mode == RADIO_MODE_TX:
            pass
        return True

    def available(self):
        if self.mode == RADIO_MODE_TX:
            return False
        self.set_mode_rx()
        return self.rx_buf_valid

    def channel_active(self):
        if self.mode != RADIO_MODE_CAD:
            self.set_mode_cad()

        while self.mode == RADIO_MODE_CAD:
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

