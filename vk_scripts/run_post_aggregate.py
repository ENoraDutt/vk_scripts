import argparse

from kafka import KafkaProducer

from config import settings
from vk_exceptions_screamer import VkExceptionsScreamer
from vk_scripts.aggregators.post_aggregator import PostAggregator
from vk_scripts.senders import JsonKafkaSender
from vk_scripts.vk_client import VkClient

VK_CLIENT = VkClient(**settings.vk_client, screamer=VkExceptionsScreamer())
kafka_producer = KafkaProducer(
    bootstrap_servers=f'{settings.kafka.bootstrap_servers}:{settings.kafka.port}',
)

aggregator = PostAggregator(
    vk_client=VK_CLIENT,
    sender=JsonKafkaSender(
        producer=kafka_producer,
        topic=settings.kafka.topic
    )
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('groups', type=str, default="default_groups_list")
    return parser.parse_args()


with open("default_groups_list") as file:
    GROUPS = file.read().strip().split("\n")
    if GROUPS == []:
        raise Exception("File with groups id is empty. Please fill it out")


def main():
    print(aggregator.aggregate(GROUPS))


main()
