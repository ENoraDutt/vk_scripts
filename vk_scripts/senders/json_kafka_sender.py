from json import dumps
from typing import List

from kafka import KafkaProducer
from pydantic import BaseModel


class JsonKafkaSender:
    def __init__(self, producer: KafkaProducer, topic: str = ""):
        self.producer = producer
        self.topic = topic

    def __call__(self, data: List[BaseModel]):
        dicts = [d.dict() for d in data]
        self.send_kafka(dumps(dicts))

    def send_kafka(self, data: str):
        data = bytes(data.encode("utf-8"))
        future = self.producer.send(self.topic, data)
        future.get()
