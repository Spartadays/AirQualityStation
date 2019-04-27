#!/usr/bin/env python3

# To auto execute this script after login it should be added to crontab with @reboot flag.
# Edit the file:
# sudo crontab -e
# Add line to file:
# @reboot /home/pi/AirQualityStation/send_to_wunderground.py STATION_ID STATION_KEY &

try:
    import pms7003
    import w1thermsensor
    import datetime
    import requests
    import sys
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
        try:
            temp_sensor = w1thermsensor.W1ThermSensor()
            pms_sensor = pms7003.PMS7003(port='/dev/ttyS0')
        except w1thermsensor.errors.NoSensorFoundError:
            print('Check connections to temperature sensor and try again')
            exit(-1)

        # ARG 1:
        try:
            pws_id = str(sys.argv[1])
        except IndexError:
            print('Specify your station id in first argument')
            pws_id = None
            exit(-1)

        # ARG 2:
        try:
            password = str(sys.argv[2])
        except IndexError:
            print('Specify your stations password in second argument')
            password = None
            exit(-1)

        # LOOP:
        while True:
            now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            temp_C = round(temp_sensor.get_temperature(), 2)
            temp_F = round(temp_sensor.get_temperature(unit=temp_sensor.DEGREES_F), 2)

            pm_10 = pms_sensor.get_pm10()
            pm_2_5 = pms_sensor.get_pm2_5()

            print(str(now) + ' temperature = ' + str(temp_C) + '*C PM10 = ' + str(pm_10) + ' PM2.5 = ' + str(pm_2_5))

            # TODO: format and add variable now as date= to send func below
            send(station_id=pws_id,
                 station_pwd=password,
                 tempf=temp_F,
                 pm10=pm_10,
                 pm2_5=pm_2_5)
    except KeyboardInterrupt:
        print('Exit')
        exit(0)
