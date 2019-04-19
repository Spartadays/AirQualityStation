try:
    import serial
except ImportError as i_error:
    print(i_error.__class__.__name__ + ": " + i_error.name)
    exit(-1)

DATA_1 = 0  # PM1.0 concentration unit ug/m3 (CF = 1, standard particle)
DATA_2 = 1  # PM2.5 concentration unit ug/m3 (CF = 1, standard particle)
DATA_3 = 2  # PM10 concentration unit ug/m3 (CF = 1, standard particle)
DATA_4 = 3  # PM1.0 concentration unit ug/m3 (under atmospheric environment)
DATA_5 = 4  # PM2.5 concentration unit ug/m3 (under atmospheric environment)
DATA_6 = 5  # PM10 concentration unit ug/m3 (under atmospheric environment)
DATA_7 = 6  # Number of particles with diameter beyond 0.3 um in 0.1 L of air
DATA_8 = 7  # Number of particles with diameter beyond 0.5 um in 0.1 L of air
DATA_9 = 8  # Number of particles with diameter beyond 1.0 um in 0.1 L of air
DATA_10 = 9  # Number of particles with diameter beyond 2.5 um in 0.1 L of air
DATA_11 = 10  # Number of particles with diameter beyond 5.0 um in 0.1 L of air
DATA_12 = 11  # Number of particles with diameter beyond 10 um in 0.1 L of air


class PMS7003:

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

        self.mode = 'active'  # 'active' or 'passive'

        self.transmission_flag = False
        self.start_bits_flag = False
        self.data_length_flag = False

        self.measures = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.cf = 0  # Call Factor: CF = 1 should be used in the factory environment

        self.check_code = None

    def read_transmission(self):
        """Read serial data, process them and update class variables"""

        def bytes_to_int(sequence):
            return int.from_bytes(sequence, byteorder='big', signed=False)

        data = self.pms_serial.read(32)
        self.transmission_flag = True

        if data[0] == 0x42 and data[1] == 0x4d:
            self.start_bits_flag = True
        else:
            self.start_bits_flag = False
            print('Start Bits ERROR')
            print(data)

        if bytes_to_int(data[2:4]) == 28:
            self.data_length_flag = True
        else:
            self.data_length_flag = False
            print('Transmission Length ERROR')
            print(data)

        for c in range(len(self.measures)):
            self.measures[c] = bytes_to_int(data[c*2+4:c*2+6])

        self.check_code = bytes_to_int(data[30:32])

    def get_measure_by_data_number(self, number, itr=0):
        """Returns data of given data number (from pms7003 datasheet)"""
        self.read_transmission()  # refresh variables
        if self.start_bits_flag is True and self.data_length_flag is True and self.transmission_flag is True:
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
