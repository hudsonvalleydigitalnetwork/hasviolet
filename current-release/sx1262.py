#!/usr/bin/python3
SX126X_PA_CONFIG_SX1262 = (0x00)
SX126X_FREQUENCY_STEP_SIZE = 0.9536743164
SX126X_MAX_PACKET_LENGTH = (255)
SX126X_CRYSTAL_FREQ = 32.0
SX126X_DIV_EXPONENT = (25)
SX126X_CMD_NOP = (0x00)
SX126X_CMD_SET_SLEEP = (0x84)
SX126X_CMD_SET_STANDBY = (0x80)
SX126X_CMD_SET_FS = (0xC1)
SX126X_CMD_SET_TX = (0x83)
SX126X_CMD_SET_RX = (0x82)
SX126X_CMD_STOP_TIMER_ON_PREAMBLE = (0x9F)
SX126X_CMD_SET_RX_DUTY_CYCLE = (0x94)
SX126X_CMD_SET_CAD = (0xC5)
SX126X_CMD_SET_TX_CONTINUOUS_WAVE = (0xD1)
SX126X_CMD_SET_TX_INFINITE_PREAMBLE = (0xD2)
SX126X_CMD_SET_REGULATOR_MODE = (0x96)
SX126X_CMD_CALIBRATE = (0x89)
SX126X_CMD_CALIBRATE_IMAGE = (0x98)
SX126X_CMD_SET_PA_CONFIG = (0x95)
SX126X_CMD_SET_RX_TX_FALLBACK_MODE = (0x93)
SX126X_CMD_WRITE_REGISTER = (0x0D)
SX126X_CMD_READ_REGISTER = (0x1D)
SX126X_CMD_WRITE_BUFFER = (0x0E)
SX126X_CMD_READ_BUFFER = (0x1E)
SX126X_CMD_SET_DIO_IRQ_PARAMS = (0x08)
SX126X_CMD_GET_IRQ_STATUS = (0x12)
SX126X_CMD_CLEAR_IRQ_STATUS = (0x02)
SX126X_CMD_SET_DIO2_AS_RF_SWITCH_CTRL = (0x9D)
SX126X_CMD_SET_DIO3_AS_TCXO_CTRL = (0x97)
SX126X_CMD_SET_RF_FREQUENCY = (0x86)
SX126X_CMD_SET_PACKET_TYPE = (0x8A)
SX126X_CMD_GET_PACKET_TYPE = (0x11)
SX126X_CMD_SET_TX_PARAMS = (0x8E)
SX126X_CMD_SET_MODULATION_PARAMS = (0x8B)
SX126X_CMD_SET_PACKET_PARAMS = (0x8C)
SX126X_CMD_SET_CAD_PARAMS = (0x88)
SX126X_CMD_SET_BUFFER_BASE_ADDRESS = (0x8F)
SX126X_CMD_SET_LORA_SYMB_NUM_TIMEOUT = (0x0A)
SX126X_CMD_GET_STATUS = (0xC0)
SX126X_CMD_GET_RSSI_INST = (0x15)
SX126X_CMD_GET_RX_BUFFER_STATUS = (0x13)
SX126X_CMD_GET_PACKET_STATUS = (0x14)
SX126X_CMD_GET_DEVICE_ERRORS = (0x17)
SX126X_CMD_CLEAR_DEVICE_ERRORS = (0x07)
SX126X_CMD_GET_STATS = (0x10)
SX126X_CMD_RESET_STATS = (0x00)
SX126X_REG_WHITENING_INITIAL_MSB = (0x06B8)
SX126X_REG_WHITENING_INITIAL_LSB = (0x06B9)
SX126X_REG_CRC_INITIAL_MSB = (0x06BC)
SX126X_REG_CRC_INITIAL_LSB = (0x06BD)
SX126X_REG_CRC_POLYNOMIAL_MSB = (0x06BE)
SX126X_REG_CRC_POLYNOMIAL_LSB = (0x06BF)
SX126X_REG_SYNC_WORD_0 = (0x06C0)
SX126X_REG_SYNC_WORD_1 = (0x06C1)
SX126X_REG_SYNC_WORD_2 = (0x06C2)
SX126X_REG_SYNC_WORD_3 = (0x06C3)
SX126X_REG_SYNC_WORD_4 = (0x06C4)
SX126X_REG_SYNC_WORD_5 = (0x06C5)
SX126X_REG_SYNC_WORD_6 = (0x06C6)
SX126X_REG_SYNC_WORD_7 = (0x06C7)
SX126X_REG_NODE_ADDRESS = (0x06CD)
SX126X_REG_BROADCAST_ADDRESS = (0x06CE)
SX126X_REG_LORA_SYNC_WORD_MSB = (0x0740)
SX126X_REG_LORA_SYNC_WORD_LSB = (0x0741)
SX126X_REG_RANDOM_NUMBER_0 = (0x0819)
SX126X_REG_RANDOM_NUMBER_1 = (0x081A)
SX126X_REG_RANDOM_NUMBER_2 = (0x081B)
SX126X_REG_RANDOM_NUMBER_3 = (0x081C)
SX126X_REG_RX_GAIN = (0x08AC)
SX126X_REG_OCP_CONFIGURATION = (0x08E7)
SX126X_REG_XTA_TRIM = (0x0911)
SX126X_REG_XTB_TRIM = (0x0912)
SX126X_REG_SENSITIVITY_CONFIG = (0x0889)
SX126X_REG_TX_CLAMP_CONFIG = (0x08D8)
SX126X_REG_RTC_STOP = (0x0920)
SX126X_REG_RTC_EVENT = (0x0944)
SX126X_REG_IQ_CONFIG = (0x0736)
SX126X_REG_RX_GAIN_RETENTION_0 = (0x029F)
SX126X_REG_RX_GAIN_RETENTION_1 = (0x02A0)
SX126X_REG_RX_GAIN_RETENTION_2 = (0x02A1)
SX126X_SLEEP_START_COLD = (0b00000000)
SX126X_SLEEP_START_WARM = (0b00000100)
SX126X_SLEEP_RTC_OFF = (0b00000000)
SX126X_SLEEP_RTC_ON = (0b00000001)
SX126X_STANDBY_RC = (0x00)
SX126X_STANDBY_XOSC = (0x01)
SX126X_RX_TIMEOUT_NONE = (0x000000)
SX126X_RX_TIMEOUT_INF = (0xFFFFFF)
SX126X_TX_TIMEOUT_NONE = (0x000000)
SX126X_STOP_ON_PREAMBLE_OFF = (0x00)
SX126X_STOP_ON_PREAMBLE_ON = (0x01)
SX126X_REGULATOR_LDO = (0x00)
SX126X_REGULATOR_DC_DC = (0x01)
SX126X_CALIBRATE_IMAGE_OFF = (0b00000000)
SX126X_CALIBRATE_IMAGE_ON = (0b01000000)
SX126X_CALIBRATE_ADC_BULK_P_OFF = (0b00000000)
SX126X_CALIBRATE_ADC_BULK_P_ON = (0b00100000)
SX126X_CALIBRATE_ADC_BULK_N_OFF = (0b00000000)
SX126X_CALIBRATE_ADC_BULK_N_ON = (0b00010000)
SX126X_CALIBRATE_ADC_PULSE_OFF = (0b00000000)
SX126X_CALIBRATE_ADC_PULSE_ON = (0b00001000)
SX126X_CALIBRATE_PLL_OFF = (0b00000000)
SX126X_CALIBRATE_RC13M_ON = (0b00000010)
SX126X_CALIBRATE_RC64K_OFF = (0b00000000)
SX126X_CALIBRATE_RC64K_ON = (0b00000001)
SX126X_CALIBRATE_ALL = (0b01111111)
SX126X_CAL_IMG_430_MHZ_1 = (0x6B)
SX126X_CAL_IMG_430_MHZ_2 = (0x6F)
SX126X_CAL_IMG_470_MHZ_1 = (0x75)
SX126X_CAL_IMG_470_MHZ_2 = (0x81)
SX126X_CAL_IMG_779_MHZ_1 = (0xC1)
SX126X_CAL_IMG_779_MHZ_2 = (0xC5)
SX126X_CAL_IMG_863_MHZ_1 = (0xD7)
SX126X_CAL_IMG_863_MHZ_2 = (0xDB)
SX126X_CAL_IMG_902_MHZ_1 = (0xE1)
SX126X_CAL_IMG_902_MHZ_2 = (0xE9)
SX126X_PA_CONFIG_HP_MAX = (0x07)
SX126X_PA_CONFIG_PA_LUT = (0x01)
SX126X_PA_CONFIG_SX1262_8 = (0x00)
SX126X_RX_TX_FALLBACK_MODE_FS = (0x40)
SX126X_RX_TX_FALLBACK_MODE_STDBY_XOSC = (0x30)
SX126X_RX_TX_FALLBACK_MODE_STDBY_RC = (0x20)
SX126X_IRQ_TIMEOUT = (0b1000000000)
SX126X_IRQ_CAD_DETECTED = (0b0100000000)
SX126X_IRQ_CAD_DONE = (0b0010000000)
SX126X_IRQ_CRC_ERR = (0b0001000000)
SX126X_IRQ_HEADER_ERR = (0b0000100000)
SX126X_IRQ_HEADER_VALID = (0b0000010000)
SX126X_IRQ_SYNC_WORD_VALID = (0b0000001000)
SX126X_IRQ_PREAMBLE_DETECTED = (0b0000000100)
SX126X_IRQ_RX_DONE = (0b0000000010)
SX126X_IRQ_TX_DONE = (0b0000000001)
SX126X_IRQ_ALL = (0b1111111111)
SX126X_IRQ_NONE = (0b0000000000)
SX126X_DIO2_AS_IRQ = (0x00)
SX126X_DIO2_AS_RF_SWITCH = (0x01)
SX126X_DIO3_OUTPUT_1_6 = (0x00)
SX126X_DIO3_OUTPUT_1_7 = (0x01)
SX126X_DIO3_OUTPUT_1_8 = (0x02)
SX126X_DIO3_OUTPUT_2_2 = (0x03)
SX126X_DIO3_OUTPUT_2_4 = (0x04)
SX126X_DIO3_OUTPUT_2_7 = (0x05)
SX126X_DIO3_OUTPUT_3_0 = (0x06)
SX126X_DIO3_OUTPUT_3_3 = (0x07)
SX126X_PACKET_TYPE_GFSK = (0x00)
SX126X_PACKET_TYPE_LORA = (0x01)
SX126X_PA_RAMP_10U = (0x00)
SX126X_PA_RAMP_20U = (0x01)
SX126X_PA_RAMP_40U = (0x02)
SX126X_PA_RAMP_80U = (0x03)
SX126X_PA_RAMP_200U = (0x04)
SX126X_PA_RAMP_800U = (0x05)
SX126X_PA_RAMP_1700U = (0x06)
SX126X_PA_RAMP_3400U = (0x07)
SX126X_GFSK_FILTER_NONE = (0x00)
SX126X_GFSK_FILTER_GAUSS_0_3 = (0x08)
SX126X_GFSK_FILTER_GAUSS_0_5 = (0x09)
SX126X_GFSK_FILTER_GAUSS_0_7 = (0x0A)
SX126X_GFSK_FILTER_GAUSS_1 = (0x0B)
SX126X_GFSK_RX_BW_4_8 = (0x1F)
SX126X_GFSK_RX_BW_5_8 = (0x17)
SX126X_GFSK_RX_BW_7_3 = (0x0F)
SX126X_GFSK_RX_BW_9_7 = (0x1E)
SX126X_GFSK_RX_BW_11_7 = (0x16)
SX126X_GFSK_RX_BW_14_6 = (0x0E)
SX126X_GFSK_RX_BW_19_5 = (0x1D)
SX126X_GFSK_RX_BW_23_4 = (0x15)
SX126X_GFSK_RX_BW_29_3 = (0x0D)
SX126X_GFSK_RX_BW_39_0 = (0x1C)
SX126X_GFSK_RX_BW_46_9 = (0x14)
SX126X_GFSK_RX_BW_58_6 = (0x0C)
SX126X_GFSK_RX_BW_78_2 = (0x1B)
SX126X_GFSK_RX_BW_93_8 = (0x13)
SX126X_GFSK_RX_BW_117_3 = (0x0B)
SX126X_GFSK_RX_BW_156_2 = (0x1A)
SX126X_GFSK_RX_BW_187_2 = (0x12)
SX126X_GFSK_RX_BW_234_3 = (0x0A)
SX126X_GFSK_RX_BW_312_0 = (0x19)
SX126X_GFSK_RX_BW_373_6 = (0x11)
SX126X_GFSK_RX_BW_467_0 = (0x09)
SX126X_LORA_BW_7_8 = (0x00)
SX126X_LORA_BW_10_4 = (0x08)
SX126X_LORA_BW_15_6 = (0x01)
SX126X_LORA_BW_20_8 = (0x09)
SX126X_LORA_BW_31_25 = (0x02)
SX126X_LORA_BW_41_7 = (0x0A)
SX126X_LORA_BW_62_5 = (0x03)
SX126X_LORA_BW_125_0 = (0x04)
SX126X_LORA_BW_250_0 = (0x05)
SX126X_LORA_BW_500_0 = (0x06)
SX126X_LORA_CR_4_5 = (0x01)
SX126X_LORA_CR_4_6 = (0x02)
SX126X_LORA_CR_4_7 = (0x03)
SX126X_LORA_CR_4_8 = (0x04)
SX126X_LORA_LOW_DATA_RATE_OPTIMIZE_OFF = (0x00)
SX126X_LORA_LOW_DATA_RATE_OPTIMIZE_ON = (0x01)
SX126X_GFSK_PREAMBLE_DETECT_OFF = (0x00)
SX126X_GFSK_PREAMBLE_DETECT_8 = (0x04)
SX126X_GFSK_PREAMBLE_DETECT_16 = (0x05)
SX126X_GFSK_PREAMBLE_DETECT_24 = (0x06)
SX126X_GFSK_PREAMBLE_DETECT_32 = (0x07)
SX126X_GFSK_ADDRESS_FILT_OFF = (0x00)
SX126X_GFSK_ADDRESS_FILT_NODE = (0x01)
SX126X_GFSK_ADDRESS_FILT_NODE_BROADCAST = (0x02)
SX126X_GFSK_PACKET_FIXED = (0x00)
SX126X_GFSK_PACKET_VARIABLE = (0x01)
SX126X_GFSK_CRC_OFF = (0x01)
SX126X_GFSK_CRC_1_BYTE = (0x00)
SX126X_GFSK_CRC_2_BYTE = (0x02)
SX126X_GFSK_CRC_1_BYTE_INV = (0x04)
SX126X_GFSK_CRC_2_BYTE_INV = (0x06)
SX126X_GFSK_WHITENING_OFF = (0x00)
SX126X_GFSK_WHITENING_ON = (0x01)
SX126X_LORA_HEADER_EXPLICIT = (0x00)
SX126X_LORA_HEADER_IMPLICIT = (0x01)
SX126X_LORA_CRC_OFF = (0x00)
SX126X_LORA_CRC_ON = (0x01)
SX126X_LORA_IQ_STANDARD = (0x00)
SX126X_LORA_IQ_INVERTED = (0x01)
SX126X_CAD_ON_1_SYMB = (0x00)
SX126X_CAD_ON_2_SYMB = (0x01)
SX126X_CAD_ON_4_SYMB = (0x02)
SX126X_CAD_ON_8_SYMB = (0x03)
SX126X_CAD_ON_16_SYMB = (0x04)
SX126X_CAD_GOTO_STDBY = (0x00)
SX126X_CAD_GOTO_RX = (0x01)
SX126X_STATUS_MODE_STDBY_RC = (0b00100000)
SX126X_STATUS_MODE_STDBY_XOSC = (0b00110000)
SX126X_STATUS_MODE_FS = (0b01000000)
SX126X_STATUS_MODE_RX = (0b01010000)
SX126X_STATUS_MODE_TX = (0b01100000)
SX126X_STATUS_DATA_AVAILABLE = (0b00000100)
SX126X_STATUS_CMD_TIMEOUT = (0b00000110)
SX126X_STATUS_CMD_INVALID = (0b00001000)
SX126X_STATUS_CMD_FAILED = (0b00001010)
SX126X_STATUS_TX_DONE = (0b00001100)
SX126X_STATUS_SPI_FAILED = (0b11111111)
SX126X_GFSK_RX_STATUS_PREAMBLE_ERR = (0b10000000)
SX126X_GFSK_RX_STATUS_SYNC_ERR = (0b01000000)
SX126X_GFSK_RX_STATUS_ADRS_ERR = (0b00100000)
SX126X_GFSK_RX_STATUS_CRC_ERR = (0b00010000)
SX126X_GFSK_RX_STATUS_LENGTH_ERR = (0b00001000)
SX126X_GFSK_RX_STATUS_ABORT_ERR = (0b00000100)
SX126X_GFSK_RX_STATUS_PACKET_RECEIVED = (0b00000010)
SX126X_GFSK_RX_STATUS_PACKET_SENT = (0b00000001)
SX126X_PA_RAMP_ERR = (0b100000000)
SX126X_PLL_LOCK_ERR = (0b001000000)
SX126X_XOSC_START_ERR = (0b000100000)
SX126X_IMG_CALIB_ERR = (0b000010000)
SX126X_ADC_CALIB_ERR = (0b000001000)
SX126X_PLL_CALIB_ERR = (0b000000100)
SX126X_RC13M_CALIB_ERR = (0b000000010)
SX126X_RC64K_CALIB_ERR = (0b000000001)
SX126X_SYNC_WORD_PUBLIC = (0x34)
SX126X_SYNC_WORD_PRIVATE = (0x12)
ERR_NONE = (0)
ERR_UNKNOWN = (-1)
ERR_CHIP_NOT_FOUND = (-2)
ERR_MEMORY_ALLOCATION_FAILED = (-3)
ERR_PACKET_TOO_LONG = (-4)
ERR_TX_TIMEOUT = (-5)
ERR_RX_TIMEOUT = (-6)
ERR_CRC_MISMATCH = (-7)
ERR_INVALID_BANDWIDTH = (-8)
ERR_INVALID_SPREADING_FACTOR = (-9)
ERR_INVALID_CODING_RATE = (-10)
ERR_INVALID_BIT_RANGE = (-11)
ERR_INVALID_FREQUENCY = (-12)
ERR_INVALID_OUTPUT_POWER = (-13)
PREAMBLE_DETECTED = (-14)
CHANNEL_FREE = (-15)
ERR_SPI_WRITE_FAILED = (-16)
ERR_INVALID_CURRENT_LIMIT = (-17)
ERR_INVALID_PREAMBLE_LENGTH = (-18)
ERR_INVALID_GAIN = (-19)
ERR_WRONG_MODEM = (-20)
ERR_INVALID_NUM_SAMPLES = (-21)
ERR_INVALID_RSSI_OFFSET = (-22)
ERR_INVALID_ENCODING = (-23)
ERR_INVALID_BIT_RATE = (-101)
ERR_INVALID_FREQUENCY_DEVIATION = (-102)
ERR_INVALID_BIT_RATE_BW_RATIO = (-103)
ERR_INVALID_RX_BANDWIDTH = (-104)
ERR_INVALID_SYNC_WORD = (-105)
ERR_INVALID_DATA_SHAPING = (-106)
ERR_INVALID_MODULATION = (-107)
ERR_AT_FAILED = (-201)
ERR_URL_MALFORMED = (-202)
ERR_RESPONSE_MALFORMED_AT = (-203)
ERR_RESPONSE_MALFORMED = (-204)
ERR_MQTT_CONN_VERSION_REJECTED = (-205)
ERR_MQTT_CONN_ID_REJECTED = (-206)
ERR_MQTT_CONN_SERVER_UNAVAILABLE = (-207)
ERR_MQTT_CONN_BAD_USERNAME_PASSWORD = (-208)
ERR_MQTT_CONN_NOT_AUTHORIZED = (-208)
ERR_MQTT_UNEXPECTED_PACKET_ID = (-209)
ERR_MQTT_NO_NEW_PACKET_AVAILABLE = (-210)
ERR_CMD_MODE_FAILED = (-301)
ERR_FRAME_MALFORMED = (-302)
ERR_FRAME_INCORRECT_CHECKSUM = (-303)
ERR_FRAME_UNEXPECTED_ID = (-304)
ERR_FRAME_NO_RESPONSE = (-305)
ERR_INVALID_RTTY_SHIFT = (-401)
ERR_UNSUPPORTED_ENCODING = (-402)
ERR_INVALID_DATA_RATE = (-501)
ERR_INVALID_ADDRESS_WIDTH = (-502)
ERR_INVALID_PIPE_NUMBER = (-503)
ERR_ACK_NOT_RECEIVED = (-504)
ERR_INVALID_NUM_BROAD_ADDRS = (-601)
ERR_INVALID_CRC_CONFIGURATION = (-701)
LORA_DETECTED = (-702)
ERR_INVALID_TCXO_VOLTAGE = (-703)
ERR_INVALID_MODULATION_PARAMETERS = (-704)
ERR_SPI_CMD_TIMEOUT = (-705)
ERR_SPI_CMD_INVALID = (-706)
ERR_SPI_CMD_FAILED = (-707)
ERR_INVALID_SLEEP_PERIOD = (-708)
ERR_INVALID_RX_PERIOD = (-709)
ERR_INVALID_CALLSIGN = (-801)
ERR_INVALID_NUM_REPEATERS = (-802)
ERR_INVALID_REPEATER_CALLSIGN = (-803)
ERR_INVALID_PACKET_TYPE = (-804)
ERR_INVALID_PACKET_LENGTH = (-805)

def ASSERT(state):
    assert state == ERR_NONE, ERROR[state]

def yield_():
    time.sleep(.001)

ERROR = {
    0: 'ERR_NONE',
    -1: 'ERR_UNKNOWN',
    -2: 'ERR_CHIP_NOT_FOUND',
    -3: 'ERR_MEMORY_ALLOCATION_FAILED',
    -4: 'ERR_PACKET_TOO_LONG',
    -5: 'ERR_TX_TIMEOUT',
    -6: 'ERR_RX_TIMEOUT',
    -7: 'ERR_CRC_MISMATCH',
    -8: 'ERR_INVALID_BANDWIDTH',
    -9: 'ERR_INVALID_SPREADING_FACTOR',
    -10: 'ERR_INVALID_CODING_RATE',
    -11: 'ERR_INVALID_BIT_RANGE',
    -12: 'ERR_INVALID_FREQUENCY',
    -13: 'ERR_INVALID_OUTPUT_POWER',
    -14: 'PREAMBLE_DETECTED',
    -15: 'CHANNEL_FREE',
    -16: 'ERR_SPI_WRITE_FAILED',
    -17: 'ERR_INVALID_CURRENT_LIMIT',
    -18: 'ERR_INVALID_PREAMBLE_LENGTH',
    -19: 'ERR_INVALID_GAIN',
    -20: 'ERR_WRONG_MODEM',
    -21: 'ERR_INVALID_NUM_SAMPLES',
    -22: 'ERR_INVALID_RSSI_OFFSET',
    -23: 'ERR_INVALID_ENCODING',
    -101: 'ERR_INVALID_BIT_RATE',
    -102: 'ERR_INVALID_FREQUENCY_DEVIATION',
    -103: 'ERR_INVALID_BIT_RATE_BW_RATIO',
    -104: 'ERR_INVALID_RX_BANDWIDTH',
    -105: 'ERR_INVALID_SYNC_WORD',
    -106: 'ERR_INVALID_DATA_SHAPING',
    -107: 'ERR_INVALID_MODULATION',
    -201: 'ERR_AT_FAILED',
    -202: 'ERR_URL_MALFORMED',
    -203: 'ERR_RESPONSE_MALFORMED_AT',
    -204: 'ERR_RESPONSE_MALFORMED',
    -205: 'ERR_MQTT_CONN_VERSION_REJECTED',
    -206: 'ERR_MQTT_CONN_ID_REJECTED',
    -207: 'ERR_MQTT_CONN_SERVER_UNAVAILABLE',
    -208: 'ERR_MQTT_CONN_BAD_USERNAME_PASSWORD',
    -208: 'ERR_MQTT_CONN_NOT_AUTHORIZED',
    -209: 'ERR_MQTT_UNEXPECTED_PACKET_ID',
    -210: 'ERR_MQTT_NO_NEW_PACKET_AVAILABLE',
    -301: 'ERR_CMD_MODE_FAILED',
    -302: 'ERR_FRAME_MALFORMED',
    -303: 'ERR_FRAME_INCORRECT_CHECKSUM',
    -304: 'ERR_FRAME_UNEXPECTED_ID',
    -305: 'ERR_FRAME_NO_RESPONSE',
    -401: 'ERR_INVALID_RTTY_SHIFT',
    -402: 'ERR_UNSUPPORTED_ENCODING',
    -501: 'ERR_INVALID_DATA_RATE',
    -502: 'ERR_INVALID_ADDRESS_WIDTH',
    -503: 'ERR_INVALID_PIPE_NUMBER',
    -504: 'ERR_ACK_NOT_RECEIVED',
    -601: 'ERR_INVALID_NUM_BROAD_ADDRS',
    -701: 'ERR_INVALID_CRC_CONFIGURATION',
    -702: 'LORA_DETECTED',
    -703: 'ERR_INVALID_TCXO_VOLTAGE',
    -704: 'ERR_INVALID_MODULATION_PARAMETERS',
    -705: 'ERR_SPI_CMD_TIMEOUT',
    -706: 'ERR_SPI_CMD_INVALID',
    -707: 'ERR_SPI_CMD_FAILED',
    -708: 'ERR_INVALID_SLEEP_PERIOD',
    -709: 'ERR_INVALID_RX_PERIOD',
    -801: 'ERR_INVALID_CALLSIGN',
    -802: 'ERR_INVALID_NUM_REPEATERS',
    -803: 'ERR_INVALID_REPEATER_CALLSIGN',
    -804: 'ERR_INVALID_PACKET_TYPE',
    -805: 'ERR_INVALID_PACKET_LENGTH'
    }

def ASSERT(state):
    assert state == ERR_NONE, ERROR[state]

def yield_():
    time.sleep(.001)

class SX1262():
    TX_DONE = SX126X_IRQ_TX_DONE
    RX_DONE = SX126X_IRQ_RX_DONE
    ADDR_FILT_OFF = SX126X_GFSK_ADDRESS_FILT_OFF
    ADDR_FILT_NODE = SX126X_GFSK_ADDRESS_FILT_NODE
    ADDR_FILT_NODE_BROAD = SX126X_GFSK_ADDRESS_FILT_NODE_BROADCAST
    PREAMBLE_DETECT_OFF = SX126X_GFSK_PREAMBLE_DETECT_OFF
    PREAMBLE_DETECT_8 = SX126X_GFSK_PREAMBLE_DETECT_8
    PREAMBLE_DETECT_16 = SX126X_GFSK_PREAMBLE_DETECT_16
    PREAMBLE_DETECT_24 = SX126X_GFSK_PREAMBLE_DETECT_24
    PREAMBLE_DETECT_32 = SX126X_GFSK_PREAMBLE_DETECT_32
    STATUS = ERROR

    def __init__(self, cs, irq, rst, gpio, clk='P10', mosi='P11', miso='P14'):
        super().__init__(cs, irq, rst, gpio, clk, mosi, miso)
        self._callbackFunction = self._dummyFunction

    def begin(self, freq=434.0, bw=125.0, sf=9, cr=7, syncWord=SX126X_SYNC_WORD_PRIVATE,
              power=14, currentLimit=60.0, preambleLength=8, implicit=False, implicitLen=0xFF,
              crcOn=True, txIq=False, rxIq=False, tcxoVoltage=1.6, useRegulatorLDO=False,
              blocking=True):
        state = super().begin(bw, sf, cr, syncWord, currentLimit, preambleLength, tcxoVoltage, useRegulatorLDO, txIq, rxIq)
        ASSERT(state)

        if not implicit:
            state = super().explicitHeader()
        else:
            state = super().implicitHeader(implicitLen)
        ASSERT(state)

        state = super().setCRC(crcOn)
        ASSERT(state)

        state = self.setFrequency(freq)
        ASSERT(state)

        state = self.setOutputPower(power)
        ASSERT(state)

        state = super().fixPaClamping()
        ASSERT(state)

        state = self.setBlockingCallback(blocking)

        return state

    def beginFSK(self, freq=434.0, br=48.0, freqDev=50.0, rxBw=156.2, power=14, currentLimit=60.0,
                 preambleLength=16, dataShaping=0.5, syncWord=[0x2D, 0x01], syncBitsLength=16,
                 addrFilter=SX126X_GFSK_ADDRESS_FILT_OFF, addr=0x00, crcLength=2, crcInitial=0x1D0F, crcPolynomial=0x1021,
                 crcInverted=True, whiteningOn=True, whiteningInitial=0x0100,
                 fixedPacketLength=False, packetLength=0xFF, preambleDetectorLength=SX126X_GFSK_PREAMBLE_DETECT_16,
                 tcxoVoltage=1.6, useRegulatorLDO=False,
                 blocking=True):
        state = super().beginFSK(br, freqDev, rxBw, currentLimit, preambleLength, dataShaping, preambleDetectorLength, tcxoVoltage, useRegulatorLDO)
        ASSERT(state)

        state = super().setSyncBits(syncWord, syncBitsLength)
        ASSERT(state)

        if addrFilter == SX126X_GFSK_ADDRESS_FILT_OFF:
            state = super().disableAddressFiltering()
        elif addrFilter == SX126X_GFSK_ADDRESS_FILT_NODE:
            state = super().setNodeAddress(addr)
        elif addrFilter == SX126X_GFSK_ADDRESS_FILT_NODE_BROADCAST:
            state = super().setBroadcastAddress(addr)
        else:
            state = ERR_UNKNOWN
        ASSERT(state)

        state = super().setCRC(crcLength, crcInitial, crcPolynomial, crcInverted)
        ASSERT(state)

        state = super().setWhitening(whiteningOn, whiteningInitial)
        ASSERT(state)

        if fixedPacketLength:
            state = super().fixedPacketLengthMode(packetLength)
        else:
            state = super().variablePacketLengthMode(packetLength)
        ASSERT(state)

        state = self.setFrequency(freq)
        ASSERT(state)

        state = self.setOutputPower(power)
        ASSERT(state)

        state = super().fixPaClamping()
        ASSERT(state)

        state = self.setBlockingCallback(blocking)

        return state

    def setFrequency(self, freq, calibrate=True):
        if freq < 150.0 or freq > 960.0:
            return ERR_INVALID_FREQUENCY

        state = ERR_NONE

        if calibrate:
            data = bytearray(2)
            if freq > 900.0:
                data[0] = SX126X_CAL_IMG_902_MHZ_1
                data[1] = SX126X_CAL_IMG_902_MHZ_2
            elif freq > 850.0:
                data[0] = SX126X_CAL_IMG_863_MHZ_1
                data[1] = SX126X_CAL_IMG_863_MHZ_2
            elif freq > 770.0:
                data[0] = SX126X_CAL_IMG_779_MHZ_1
                data[1] = SX126X_CAL_IMG_779_MHZ_2
            elif freq > 460.0:
                data[0] = SX126X_CAL_IMG_470_MHZ_1
                data[1] = SX126X_CAL_IMG_470_MHZ_2
            else:
                data[0] = SX126X_CAL_IMG_430_MHZ_1
                data[1] = SX126X_CAL_IMG_430_MHZ_2
            state = super().calibrateImage(data)
            ASSERT(state)

        return super().setFrequencyRaw(freq)

    def setOutputPower(self, power):
        if not ((power >= -9) and (power <= 22)):
            return ERR_INVALID_OUTPUT_POWER

        ocp = bytearray(1)
        ocp_mv = memoryview(ocp)
        state = super().readRegister(SX126X_REG_OCP_CONFIGURATION, ocp_mv, 1)
        ASSERT(state)

        state = super().setPaConfig(0x04, _SX126X_PA_CONFIG_SX1262)
        ASSERT(state)

        state = super().setTxParams(power)
        ASSERT(state)

        return super().writeRegister(SX126X_REG_OCP_CONFIGURATION, ocp, 1)

    def setTxIq(self, txIq):
        self._txIq = txIq

    def setRxIq(self, rxIq):
        self._rxIq = rxIq
        if not self.blocking:
            ASSERT(super().startReceive())

    def setPreambleDetectorLength(self, preambleDetectorLength):
        self._preambleDetectorLength = preambleDetectorLength
        if not self.blocking:
            ASSERT(super().startReceive())

    def setBlockingCallback(self, blocking, callback=None):
        self.blocking = blocking
        if not self.blocking:
            state = super().startReceive()
            ASSERT(state)
            if callback != None:
                self._callbackFunction = callback
                super().setDio1Action(self._onIRQ)
            else:
                self._callbackFunction = self._dummyFunction
                super().clearDio1Action()
            return state
        else:
            state = super().standby()
            ASSERT(state)
            self._callbackFunction = self._dummyFunction
            super().clearDio1Action()
            return state

    def recv(self, len_=0):
        if not self.blocking:
            return self._readData(len_)
        else:
            return self._receive(len_)

    def send(self, data):
        if not self.blocking:
            return self._startTransmit(data)
        else:
            return self._transmit(data)

    def _events(self):
        return super().getIrqStatus()

    def _receive(self, len_=0):
        state = ERR_NONE
        
        length = len_
        
        if len_ == 0:
            length = SX126X_MAX_PACKET_LENGTH

        data = bytearray(length)
        data_mv = memoryview(data)

        try:
            state = super().receive(data_mv, length)
        except AssertionError as e:
            state = list(ERROR.keys())[list(ERROR.values()).index(str(e))]

        if state == ERR_NONE:
            if len_ == 0:
                length = super().getPacketLength(False)
                data = data[:length]

        else:
            return b'', state

        return  bytes(data), state

    def _transmit(self, data):
        if isinstance(data, bytes) or isinstance(data, bytearray):
            pass
        else:
            return 0, ERR_INVALID_PACKET_TYPE

        state = super().transmit(data, len(data))
        return len(data), state

    def _readData(self, len_=0):
        state = ERR_NONE

        length = super().getPacketLength()

        if len_ < length and len_ != 0:
            length = len_

        data = bytearray(length)
        data_mv = memoryview(data)

        try:
            state = super().readData(data_mv, length)
        except AssertionError as e:
            state = list(ERROR.keys())[list(ERROR.values()).index(str(e))]

        ASSERT(super().startReceive())

        if state == ERR_NONE:
            return bytes(data), state

        else:
            return b'', state

    def _startTransmit(self, data):
        if isinstance(data, bytes) or isinstance(data, bytearray):
            pass
        else:
            return 0, ERR_INVALID_PACKET_TYPE

        state = super().startTransmit(data, len(data))
        return len(data), state

    def _dummyFunction(self, *args):
        pass

    def _onIRQ(self, callback):
        events = self._events()
        if events & SX126X_IRQ_TX_DONE:
            super().startReceive()
        self._callbackFunction(events)