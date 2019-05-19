"""SCRIPT MADE TO TEST PMS SENSOR"""
import time
import pms7003 as pms_sensor
import datetime
import matplotlib.pyplot as plt


temp_measures_pm2_5 = []
temp_datetime = []

if __name__ == '__main__':
    try:
        sensor = pms_sensor.PMS7003()
        while True:
            i = 0
            while True:
                my_measures = sensor.get_all_measures()
                sensor.print_all_measures(update=False)
            # sensor.sleep()
            # time.sleep(60)
            # sensor.wakeup()
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
