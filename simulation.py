from meter import Meter
from argparse import ArgumentParser
from threading import Thread


# main function with argument parsing

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="Meter Data Sending Simulation",
        description="Simulate sending meter data to Kafka",
        epilog="",
    )

    parser.add_argument(
        "-n", "--num_meters", type=int, required=False, help="Number of meters"
    )
    parser.add_argument("-t", "--topic", type=str, required=False, help="Kafka Topic")
    parser.add_argument(
        "-i", "--interval", type=int, required=False, help="Interval in seconds"
    )

    num_meters = 5
    topic = "meter_data"
    interval = 60

    args = parser.parse_args()

    if args.num_meters:
        num_meters = args.num_meters
    if args.topic:
        topic = args.topic
    if args.interval:
        interval = args.interval

    for i in range(num_meters):
        meter = Meter(f"SM_{i + 1}", topic, interval)
        t = Thread(target=meter.send_data)

        print(f"Meter {meter.get_id()} started")
