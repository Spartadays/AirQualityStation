#!/usr/bin/env python3

# To auto execute this script after login it should be added to crontab with @reboot flag.
# Edit the file:
# sudo crontab -e
# Add line to file:
# @reboot /home/pi/AirQualityStation/send_to_.py STATION_ID STATION_KEY &

try:
    # import pms7003
    # import w1thermsensor
    import datetime
    import requests
    import sys
    import time
    import Adafruit_DHT
    import adafruit_bmp280
    import board
    import busio
except ImportError as i_error:
    print(i_error.__class__.__name__ + ": " + i_error.name)
    exit(-1)


def send(api_key, temperature, pressure, humidity, pm1_0=None, pm_2_5=None, pm_10=None):
    url = 'https://api.thingspeak.com/update?api_key='
    r = requests.get(url + api_key +
                     '&field1=' + str(temperature) +
                     '&field2=' + str(pressure) +
                     '&field3=' + str(humidity)
                     )
    print('Received ' + str(r.status_code) + ' ' + str(r.text))


if __name__ == '__main__':
    try:
        print("Ctrl+C to stop script")

        # STARTUP:
        dht_sensor_number = 22
        dht_pin = 25
        print(board.SCL)
        print(board.SDA)
        i2c = busio.I2C(board.SCL, board.SDA)
        # TODO: nie dziala bo czujnik nie jest z adafruita tylko jakis inny/ na Arduino dziala/ trzeba ogarnac biblioteke do tego modelu
        bmp_sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

        # LOOP:
        while True:
            # now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                humidity, temperature = Adafruit_DHT.read_retry(dht_sensor_number, dht_pin)
            except Exception:
                print('ERROR using temperature and humidity sensor')
                humidity = None
                temperature = None

            try:
                pressure = bmp_sensor.pressure
            except Exception:
                print('ERROR using pressure sensor')
                pressure = None

            send('BY3E4OY6MMTCFJLR', temperature, pressure, humidity)
            time.sleep(30)
    except KeyboardInterrupt:
        print('Exit')
        exit(0)
