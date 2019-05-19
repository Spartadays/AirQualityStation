#!/usr/bin/env python3

# To auto execute this script after login it should be added to crontab with @reboot flag.
# Edit the file:
# sudo crontab -e
# Add line to file:
# @reboot /home/pi/AirQualityStation/send_to_thingspeak.py &

import pms7003 as pms
import requests
import time
import Adafruit_DHT
import smbus2
import bme280


def send(_api_key, _temperature, _pressure, _humidity, _pm_1_0, _pm_2_5, _pm_10, _num_of_0_3_um, _num_of_0_5_um):
    url = 'https://api.thingspeak.com/update?api_key='
    r = requests.get(url + _api_key +
                     '&field1=' + str(_temperature) +
                     '&field2=' + str(_pressure) +
                     '&field3=' + str(_humidity) +
                     '&field4=' + str(_pm_1_0) +
                     '&field5=' + str(_pm_2_5) +
                     '&field6=' + str(_pm_10) +
                     '&field7=' + str(_num_of_0_3_um) +
                     '&field8=' + str(_num_of_0_5_um)
                     )
    # print('Received ' + str(r.status_code) + ' ' + str(r.text))


if __name__ == '__main__':
    try:
        print("Ctrl+C to stop script")

        # STARTUP:
        start_time = time.time()  # start time measure (including startup)
        delay_time = 60.0  # minimum is 30 (if we send data during whole year)

        api = 'BY3E4OY6MMTCFJLR'

        dht_sensor_number = 22
        dht_pin = 25

        bme280_port = 1
        bme280_address = 0x76
        bme280_bus = smbus2.SMBus(bme280_port)
        bme280_calibration_params = bme280.load_calibration_params(bme280_bus, bme280_address)

        pms_sensor = pms.PMS7003()

        # LOOP:
        while True:
            try:
                humidity, temperature = Adafruit_DHT.read_retry(dht_sensor_number, dht_pin)
            except Exception as error:
                print(error)
                print('ERROR using temperature and humidity sensor')
                humidity = None
                temperature = None

            try:
                bme280_data = bme280.sample(bme280_bus, bme280_address, bme280_calibration_params)
                pressure = bme280_data.pressure
            except Exception as error:
                print(error)
                print('ERROR using pressure sensor')
                pressure = None

            try:
                pms_sensor.wakeup()
                pms_measures = pms_sensor.get_all_measures()
                pm_1_0 = pms_measures[pms.PM1_0]
                pm_2_5 = pms_measures[pms.PM2_5]
                pm_10 = pms_measures[pms.PM10]
                num_of_0_3_um = pms_measures[pms.NUM_OF_PAR_0_3_UM_IN_0_1_L_OF_AIR]
                num_of_0_5_um = pms_measures[pms.NUM_OF_PAR_0_5_UM_IN_0_1_L_OF_AIR]
                pms_sensor.sleep()
            except Exception as error:
                print(error)
                print('ERROR using pms sensor')
                pm_1_0 = None
                pm_2_5 = None
                pm_10 = None
                num_of_0_3_um = None
                num_of_0_5_um = None

            stop_time = time.time()  # stop measuring time before sending

            # print((stop_time - start_time))
            if stop_time-start_time < delay_time:
                time.sleep(delay_time-(stop_time-start_time))  # Sleep to provide X seconds between sending next data

            send(api, temperature, pressure, humidity, pm_1_0, pm_2_5, pm_10, num_of_0_3_um, num_of_0_5_um)
            start_time = time.time()  # start measure of time after data sending

    except KeyboardInterrupt:
        print('Exit')
        exit(0)
