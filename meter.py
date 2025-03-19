from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


class Meter:
    def __init__(self, meter_id, topic="meter_data", interval=60):
        self.METER_ID = meter_id
        self.TOPIC = topic
        self.INTERVAL = interval  # seconds

    def send_data(self):
        while True:
            data = {
                "meter_id": self.get_id(),
                "timestamp": int(time.time()),
                "energy_consumption": round(random.uniform(0.1, 5.0), 2),
                "voltage": round(random.uniform(210, 240), 1),
                "current": round(random.uniform(5, 30), 2),
                "power_factor": round(random.uniform(0.8, 1.0), 2),
            }

            producer.send(
                self.get_topic(), key=bytes(self.get_id(), "utf-8"), value=data
            )
            producer.flush()

            print(f"Sent: {data}")

            time.sleep(self.get_interval())

    def get_id(self):
        return self.METER_ID

    def get_topic(self):
        return self.TOPIC

    def get_interval(self):
        return self.INTERVAL


if __name__ == "__main__":
    meter = Meter("SM_001")
    try:
        meter.send_data()
    except KeyboardInterrupt:
        print("Stopping meter sending...")
