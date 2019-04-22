try:
    import pms7003
    import w1thermsensor
    import datetime
    import time
    import requests
except ImportError as i_error:
    print(i_error.__class__.__name__ + ": " + i_error.name)
    exit(-1)


def send(station_id, station_pwd, tempf, pm10, pm2_5):
    url = 'https://weatherstation.wunderground.com/weatherstation/updateweatherstation.php?'
    my_id = 'ID=' + station_id + '&PASSWORD=' + station_pwd
    date = '&dateutc=now'
    action = '&action=updateraw'
    r = requests.get(url + my_id
                     + '&tempf=' + str(tempf)
                     + '&AqPM10=' + str(pm10)
                     + '&AqPM2.5=' + str(pm2_5)
                     + date + action)
    print('Received ' + str(r.status_code) + ' ' + str(r.text))


if __name__ == '__main__':
    try:
        print("Ctrl+C to stop script")

        # STARTUP:
        temp_sensor = w1thermsensor.W1ThermSensor()
        pms_sensor = pms7003.PMS7003(port='/dev/ttyS0')
        id_poznan = 'IPOZNA82'
        id_szc = 'ISZYDO1'
        pwd_poznan = 'mh11hcit'
        pwd_szc = 'pOmlarZy'

        # LOOP:
        while True:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            temp_C = round(temp_sensor.get_temperature(), 2)
            temp_F = round(temp_sensor.get_temperature(unit=temp_sensor.DEGREES_F), 2)

            pm_10 = pms_sensor.get_pm10()
            pm_2_5 = pms_sensor.get_pm2_5()

            print(str(now) + ' temperature = ' + str(temp_C) + '*C  PM10 = ' + str(pm_10) + '  PM2.5 = ' + str(pm_2_5))

            send(station_id=id_szc,
                 station_pwd=pwd_szc,
                 tempf=temp_F,
                 pm10=pm_10,
                 pm2_5=pm_2_5)
    except KeyboardInterrupt:
        print('Exit')
        exit(0)
