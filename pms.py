try:
    import time
    import pms7003 as pms
except ImportError as i_error:
    print(i_error.__class__.__name__ + ": " + i_error.name)
    exit(-1)

if __name__ == '__main__':
    while True:
        try:
            sensor = pms.PMS7003()
            my_measures = sensor.get_all_measures()
            sensor.print_all_measures(False)
        except KeyboardInterrupt:
            print('Exit')
            exit(0)
