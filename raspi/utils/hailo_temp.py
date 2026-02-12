from hailo_platform import Device
import time
import psutil
import argparse

def _get_cpu_temp():
    t = psutil.sensors_temperatures()
    return t["cpu_thermal"][0].current

def _run_periodic(delay=1):
    target = Device()

    try:
        while True:
            hat_temp = target.control.get_chip_temperature().ts0_temperature
            throttling = target.control.get_throttling_state()
            t = _get_cpu_temp()
            print(f"\rHailo chip: {hat_temp:.2f} C\t(throttling: {throttling})\tCPU: {t:.2f}", end="")
            time.sleep(delay)
    except KeyboardInterrupt:
        print("\n-I- Received keyboard interrupt, exiting")

def main():
    parser = argparse.ArgumentParser(description="Monitor RaspberryPi's CPU and Hailo temperatures")
    parser.add_argument("-i", "--interval",
                        dest="interval",
                        metavar="N",
                        type=float,
                        default=1.0,
                        help="probing interval (s)")
    args = parser.parse_args()
    _run_periodic(args.interval)


if __name__ == "__main__":
    main()