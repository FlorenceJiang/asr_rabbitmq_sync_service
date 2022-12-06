import pika
import numpy as np

from models import ASR


SAMPLING_RATE = 16000
model = ASR()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')


def on_request(ch, method, props, body):
    audio_length = int(body)

    print(f" [.] audio length={audio_length}")
    dummy_input = np.random.randn(SAMPLING_RATE * audio_length) # TODO: put real audio here. should turn bytes into array.
    response = model.transcribe(dummy_input)
    response += 'dummy transcription' # add dummy transcription in purpose, cuz random response would be empty string.

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()