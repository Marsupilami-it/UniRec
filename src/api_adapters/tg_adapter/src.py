from kafka import KafkaConsumer

print('Hello, world')

consumer = KafkaConsumer('my_favorite_topic')
for msg in consumer:
    print(msg)
