try:
    import time
    import serial
except ImportError as i_error:
    print(i_error.__class__.__name__ + ": " + i_error.name)
    exit(-1)


def main():
    # PMS7003 SENSOR:
    pms_serial = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
        stopbits=1,
        parity=serial.PARITY_NONE
    )

# TODO: MOVE PMS7003 TO CLASS

    # MAIN LOOP:
    while True:
        try:
            data = pms_serial.read(32)
            if data[0] == 0x42 and data[1] == 0x4d:
                # print('Start Bits OK')
                pass
            else:
                print('Start Bits ERROR')
                pass

            if int.from_bytes(data[2:4], byteorder='big', signed=False) == 28:
                # print('Transmission Length OK')
                pass
            else:
                print('Transmission Length ERROR')
                pass

            print(data)

            pm1_0_ug_m3 = int.from_bytes(data[4:6], byteorder='big', signed=False)
            print('PM1.0 = ' + str(pm1_0_ug_m3) + ' ug/m3, factory environment')

            pm2_5_ug_m3 = int.from_bytes(data[6:8], byteorder='big', signed=False)
            print('PM2.5 = ' + str(pm2_5_ug_m3) + ' ug/m3, factory environment')

            pm10_ug_m3 = int.from_bytes(data[8:10], byteorder='big', signed=False)
            print('PM10 = ' + str(pm10_ug_m3) + ' ug/m3, factory environment')

            pm1_0_ug_m3_a = int.from_bytes(data[10:12], byteorder='big', signed=False)
            print('PM1.0 = ' + str(pm1_0_ug_m3_a) + ' ug/m3, atmospheric environment')

            pm2_5_ug_m3_a = int.from_bytes(data[12:14], byteorder='big', signed=False)
            print('PM2.5 = ' + str(pm2_5_ug_m3_a) + ' ug/m3, atmospheric environment')

            pm10_ug_m3_a = int.from_bytes(data[14:16], byteorder='big', signed=False)
            print('PM10 = ' + str(pm10_ug_m3_a) + ' ug/m3, atmospheric environment')

            in_L = int.from_bytes(data[16:18], byteorder='big', signed=False)
            print('Number of particles with diameter beyond 0.3 um in 0.1L of air = ' + str(in_L))

            in_L = int.from_bytes(data[18:20], byteorder='big', signed=False)
            print('Number of particles with diameter beyond 0.5 um in 0.1L of air = ' + str(in_L))

            in_L = int.from_bytes(data[20:22], byteorder='big', signed=False)
            print('Number of particles with diameter beyond 1.0 um in 0.1L of air = ' + str(in_L))

            in_L = int.from_bytes(data[22:24], byteorder='big', signed=False)
            print('Number of particles with diameter beyond 2.5 um in 0.1L of air = ' + str(in_L))

            in_L = int.from_bytes(data[24:26], byteorder='big', signed=False)
            print('Number of particles with diameter beyond 5.0 um in 0.1L of air = ' + str(in_L))

            in_L = int.from_bytes(data[26:28], byteorder='big', signed=False)
            print('Number of particles with diameter beyond 10 um in 0.1L of air = ' + str(in_L))

            in_L = int.from_bytes(data[28:30], byteorder='big', signed=False)
            print('reserved data = ' + str(in_L))

            check_code = int.from_bytes(data[30:32], byteorder='big', signed=False)
            print('Check Code: ' + str(check_code))

            time.sleep(3)

        except KeyboardInterrupt:
            print('Exit')
            exit(0)


if __name__ == '__main__':
    main()
