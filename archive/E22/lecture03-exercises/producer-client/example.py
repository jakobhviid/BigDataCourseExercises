from operator import truediv
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='kafka:9092')
exit = False
while not exit:
    input = input()
    if(input == "exit"):
        exit == True
        break
    producer.send('foobar', )
for _ in range(100):
   