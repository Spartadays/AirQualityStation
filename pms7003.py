try:
    import serial
except ImportError as i_error:
    print(i_error.__class__.__name__ + ": " + i_error.name)
    exit(-1)


class PMS7003:

    def __init__(self, port):
        self.port = port
        self.baud_rate = 9600
        self.stop_bits = 1
        self.parity = serial.PARITY_NONE

        self.transmission = None
        self.start_bits = None
        self.data_length = None

        self.data_1 = None  # PM1.0 concentration unit ug/m3 (CF = 1, standard particle)
        self.data_2 = None  # PM2.5 concentration unit ug/m3 (CF = 1, standard particle)
        self.data_3 = None  # PM10 concentration unit ug/m3 (CF = 1, standard particle)

        # Call Factor: CF = 1 should be used in the factory environment

        self.data_4 = None  # PM1.0 concentration unit ug/m3 (under atmospheric environment)
        self.data_5 = None  # PM2.5 concentration unit ug/m3 (under atmospheric environment)
        self.data_6 = None  # PM10 concentration unit ug/m3 (under atmospheric environment)

        self.data_7 = None  # Number of particles with diameter beyond 0.3 um in 0.1 L of air
        self.data_8 = None  # Number of particles with diameter beyond 0.5 um in 0.1 L of air
        self.data_9 = None  # Number of particles with diameter beyond 1.0 um in 0.1 L of air
        self.data_10 = None  # Number of particles with diameter beyond 2.5 um in 0.1 L of air
        self.data_11 = None  # Number of particles with diameter beyond 5.0 um in 0.1 L of air
        self.data_12 = None  # Number of particles with diameter beyond 10 um in 0.1 L of air

        self.data_13 = None  # Reserved

        self.check_code = None

    def get_data_by_number(self, number):
        pass  # TODO:

    def get_pm1_0(self, cf=0):
        if cf == 1:
            return self.get_data_by_number(1)
        else:
            return self.get_data_by_number(4)

    def get_pm2_5(self, cf=0):
        if cf == 1:
            return self.get_data_by_number(2)
        else:
            return self.get_data_by_number(5)

    def get_pm10(self, cf=0):
        if cf == 1:
            return self.get_data_by_number(3)
        else:
            return self.get_data_by_number(6)


# TODO: zrob funkcje do zwracania poszczegolnych pomiarow z obiektu, funkcje do wypisania w konsoli calosci,
#       obsluge bledow, funkcje update ktora odczytuje ramke z pms a jak nie to czeka