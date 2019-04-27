"""SCRIPT MADE TO TEST PMS SENSOR"""
try:
    import time
    import pms7003 as pms_sensor
    import datetime
    import matplotlib.pyplot as plt
except ImportError as i_error:
    print(i_error.__class__.__name__ + ": " + i_error.name)
    exit(-1)

temp_measures_pm2_5 = []
temp_datetime = []

if __name__ == '__main__':
    try:
        sensor = pms_sensor.PMS7003()
        while True:
            i = 0
            while i <= 10:
                my_measures = sensor.get_all_measures()
                sensor.print_all_measures(update=False)
                i = i + 1
            sensor.sleep()
            time.sleep(60)
            sensor.wakeup()
            # now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # print(now)
            # temp_datetime.append(now)
            # temp_measures_pm2_5.append(my_measures[pms.PM2_5])
            # plt.plot(temp_datetime, temp_measures_pm2_5)
            # plt.show()
            # plt.close('all')
    except KeyboardInterrupt:
        print('Exit')
        exit(0)
