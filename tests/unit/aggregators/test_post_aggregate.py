from vk_exceptions_screamer import VkExceptionsScreamer
from vk_scripts.aggregators.post_aggregator import PostAggregator
from vk_scripts.senders import JsonKafkaSender
from vk_scripts.vk_client import VkClient


def test_post_aggregate_json_kafka_sender(mocker):
    """ Проверяет работу PostAggregate c vk_client и JsonKafkaSender """

    kafka_producer = mocker.MagicMock()
    kafka_producer.send.return_value = mocker.MagicMock()

    client = VkClient(
        screamer=VkExceptionsScreamer(),
        url="https://api.vk.com/method/",
        token="vk1.a.ItrM6LM8vwBiG3WftcAuNPhwk4naNkaqAt5jmIAMAWXwHLhcoNGH3TZAC9u",
        version="5.1312",
    )
    mocker.patch.object(client, "get_posts_from_groups", return_value=[])

    aggregator = PostAggregator(
        vk_client=client,
        sender=JsonKafkaSender(
            producer=kafka_producer,
            topic="topic"
        )
    )

    aggregator.aggregate(groups=["123"])

    assert kafka_producer.send.called
    assert client.get_posts_from_groups.called
