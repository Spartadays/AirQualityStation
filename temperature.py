try:
    import time
    import w1thermsensor
    import sys
except ImportError as i_error:
    print(i_error.__class__.__name__ + ": " + i_error.message)
    exit(-1)


def main():
    try:
        print("Ctrl+C to stop script")

        # 1-Wire Sensor:
        sensor = w1thermsensor.W1ThermSensor()
        # sensor_max = 125
        # sensor_min = -55

        # ARG 1:
        try:
            deg = str(sys.argv[1])  # Celsius ["C"] or Fahrenheit ["F"] or Kelvin ["K"]
            print("Degrees: *" + deg)
        except IndexError:
            deg = "C"
            print("First argument is not given, using default/n Degrees: *C")

        # ARG 2:
        try:
            num_of_measures = int(sys.argv[2])  # int
            print("Measures to mean: " + str(num_of_measures))
        except IndexError:
            num_of_measures = 10
            print("Second argument is not given, using default/n Measures to mean: 10")

        # MAIN LOOP:
        while True:
            i = 0
            temp_sum = 0
            while i < num_of_measures:
                if deg == "C":
                    temp_sum = temp_sum + sensor.get_temperature()
                elif deg == "F":
                    temp_sum = temp_sum + sensor.get_temperature(sensor.DEGREES_F)
                elif deg == "K":
                    temp_sum = temp_sum + sensor.get_temperature(sensor.KELVIN)
                else:
                    print("Wrong unit - using *C as default")
                    deg = "C"
                    i = i - 1
                i = i + 1

            temp_mean = round(temp_sum/num_of_measures, 2)
            print(str(temp_mean) + " *" + deg)

    except KeyboardInterrupt:
        print("Exit")
        exit(0)


if __name__ == '__main__':
    main()
