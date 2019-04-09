try:
    import time
    import serial
except ImportError as i_error:
    print(i_error.__class__.__name__ + ": " + i_error.message)
    exit(-1)


def main():
    # PMS7003 SENSOR:
    pms_serial = serial.Serial(
        port='/dev/ttyS0',
        baudrate=9600,
    )

    # MAIN LOOP:
    while True:
        try:
            r = str(pms_serial.read())
            print(r)
        except Exception:
            pass
        except KeyboardInterrupt:
            print("Exit")
            exit(0)


if __name__ == '__main__':
    main()
