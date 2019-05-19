try:
    import serial
    import time
except ImportError as i_error:
    print(i_error.__class__.__name__ + ": " + i_error.name)
    exit(-1)

# MODE:
active = 'active'
# passive = 'passive'  # TODO: in progress

# STATES:
sleep = 'sleep'
wakeup = 'wakeup'

# DATA:
DATA_1 = PM1_0CF1 = 0  # PM1.0 concentration unit ug/m3 (CF = 1, standard particle)
DATA_2 = PM2_5CF1 = 1  # PM2.5 concentration unit ug/m3 (CF = 1, standard particle)
DATA_3 = PM10CF1 = 2  # PM10 concentration unit ug/m3 (CF = 1, standard particle)
DATA_4 = PM1_0 = 3  # PM1.0 concentration unit ug/m3 (under atmospheric environment)
DATA_5 = PM2_5 = 4  # PM2.5 concentration unit ug/m3 (under atmospheric environment)
DATA_6 = PM10 = 5  # PM10 concentration unit ug/m3 (under atmospheric environment)
DATA_7 = NUM_OF_PAR_0_3_UM_IN_0_1_L_OF_AIR = 6  # Number of particles with diameter beyond 0.3 um in 0.1 L of air
DATA_8 = NUM_OF_PAR_0_5_UM_IN_0_1_L_OF_AIR = 7  # Number of particles with diameter beyond 0.5 um in 0.1 L of air
DATA_9 = NUM_OF_PAR_1_UM_IN_0_1_L_OF_AIR = 8  # Number of particles with diameter beyond 1.0 um in 0.1 L of air
DATA_10 = NUM_OF_PAR_2_5_UM_IN_0_1_L_OF_AIR = 9  # Number of particles with diameter beyond 2.5 um in 0.1 L of air
DATA_11 = NUM_OF_PAR_5_0_UM_IN_0_1_L_OF_AIR = 10  # Number of particles with diameter beyond 5.0 um in 0.1 L of air
DATA_12 = NUM_OF_PAR_10_UM_IN_0_1_L_OF_AIR = 11  # Number of particles with diameter beyond 10 um in 0.1 L of air


class PMS7003:
    """PMS7003 - air quality sensor class"""
    def __init__(self, port=None):
        """Crate PMS7003 sensor object on given COM port (default '/dev/ttyS0' rx/tx pins on Raspberry)"""
        if port is None:
            port = '/dev/ttyS0'
        self.pms_serial = serial.Serial(
            port=port,
            baudrate=9600,
            stopbits=1,
            parity=serial.PARITY_NONE
        )
        self.read_flag = False
        self.measures = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.cf = 0  # Call Factor: CF = 1 should be used in the factory environment
        self.send_command(wakeup)
        self.send_command(active)
        print('Initializing sensor. Please wait...')
        for i in range(10):
            self.get_all_measures()
        print('PMS7003 sensor is ready to use')

    def read_transmission(self):
        """Read serial data, process them and update class variables"""

        def bytes_to_int(sequence):
            return int.from_bytes(sequence, byteorder='big', signed=False)

        try:
            data = self.pms_serial.read(32)
        except serial.SerialException:
            print('ERROR while reading serial port, maybe other script is using sensor...')
            exit(-1)

        if data[0] == 0x42 and data[1] == 0x4d:
            start_bits_flag = True
        else:
            start_bits_flag = False
            print('Start Bits ERROR')

        if bytes_to_int(data[2:4]) == 28:
            data_length_flag = True
        else:
            data_length_flag = False
            print('Transmission Length ERROR')

        check_code = bytes_to_int(data[30:32])
        my_sum = sum(data[:30])

        if my_sum == check_code:
            check_code_flag = True
        else:
            check_code_flag = False
            print('Check Sum ERROR')

        if start_bits_flag is True and data_length_flag is True and check_code_flag is True:
            for c in range(len(self.measures)):
                self.measures[c] = bytes_to_int(data[c * 2 + 4:c * 2 + 6])
            self.read_flag = True
        else:
            self.read_flag = False

    def get_measure_by_data_number(self, number, itr=0):
        """Returns data of given data number (from pms7003 datasheet)"""
        self.read_transmission()  # refresh variables
        if self.read_flag is True:
            return self.measures[number]
        elif itr == 32:
            print("Transmission ERROR")
            return None
        else:
            print("Please wait")
            self.get_measure_by_data_number(number, itr + 1)

    def get_pm1_0(self, cf=0):
        """Returns PM1.0 in ug/m3, cf=1 when under factory environment"""
        if cf == 1:
            return self.get_measure_by_data_number(DATA_1)
        else:
            return self.get_measure_by_data_number(DATA_4)

    def get_pm2_5(self, cf=0):
        """Returns PM2.5 in ug/m3, cf=1 when under factory environment"""
        if cf == 1:
            return self.get_measure_by_data_number(DATA_2)
        else:
            return self.get_measure_by_data_number(DATA_5)

    def get_pm10(self, cf=0):
        """Returns PM10 in ug/m3, cf=1 when under factory environment"""
        if cf == 1:
            return self.get_measure_by_data_number(DATA_3)
        else:
            return self.get_measure_by_data_number(DATA_6)

    def get_all_measures(self):
        """Returns list of measures DATA1-DATA12"""
        self.read_transmission()  # refresh variables
        return self.measures

    def print_all_measures(self, update=True):
        """Prints list of measures in console"""
        if update is True:
            self.read_transmission()  # refresh variables
        print('PM1.0 = ' + str(self.measures[DATA_1]) + ' ug/m3, factory environment')
        print('PM2.5 = ' + str(self.measures[DATA_2]) + ' ug/m3, factory environment')
        print('PM10 = ' + str(self.measures[DATA_3]) + ' ug/m3, factory environment')
        print('PM1.0 = ' + str(self.measures[DATA_4]) + ' ug/m3, atmospheric environment')
        print('PM2.5 = ' + str(self.measures[DATA_5]) + ' ug/m3, atmospheric environment')
        print('PM10 = ' + str(self.measures[DATA_6]) + ' ug/m3, atmospheric environment')
        print('Number of particles with diameter beyond 0.3 um in 0.1L of air = ' + str(self.measures[DATA_7]))
        print('Number of particles with diameter beyond 0.5 um in 0.1L of air = ' + str(self.measures[DATA_8]))
        print('Number of particles with diameter beyond 1.0 um in 0.1L of air = ' + str(self.measures[DATA_9]))
        print('Number of particles with diameter beyond 2.5 um in 0.1L of air = ' + str(self.measures[DATA_10]))
        print('Number of particles with diameter beyond 5.0 um in 0.1L of air = ' + str(self.measures[DATA_11]))
        print('Number of particles with diameter beyond 10 um in 0.1L of air = ' + str(self.measures[DATA_12]))

    def send_command(self, command):
        """Send command to sensor. Modes: active(default) or passive. States: sleep or wakeup(default)"""
        start_b1 = 0x42
        start_b2 = 0x4d
        if command == active:
            cmd = 0xe1
            data_h = 0x00
            data_l = 0x01
            lrc_h = 0x01
            lrc_l = 0x71
        elif command == sleep:
            cmd = 0xe4
            data_h = 0x00
            data_l = 0x00
            lrc_h = 0x01
            lrc_l = 0x73
        elif command == wakeup:
            cmd = 0xe4
            data_h = 0x00
            data_l = 0x01
            lrc_h = 0x01
            lrc_l = 0x74
        elif command == 'read':
            cmd = 0xe2
            data_h = 0x00
            data_l = 0x00
            lrc_h = 0x01
            lrc_l = 0x71
        # elif command == passive:  # TODO: passive mode in progress
            # cmd = 0xe1
            # data_h = 0x00
            # data_l = 0x00
            # lrc_h = 0x01
            # lrc_l = 0x70
        else:
            print('Skipped command sending')
            return
        protocol = bytearray([start_b1, start_b2, cmd, data_h, data_l, lrc_h, lrc_l])
        self.pms_serial.write(protocol)

    def sleep(self):
        self.send_command(sleep)
        self.pms_serial.read_all()

    def wakeup(self):
        self.send_command(wakeup)
        self.pms_serial.read_all()
        for i in range(20):
            self.get_all_measures()
