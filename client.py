import pika
import uuid


class ASRRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        # 1. When the Client starts up,
		# it creates an anonymous exclusive callback queue:
        # sends back response in the callback function.
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True) # when the channel receives msg. it directly start the callback queue which sends back the msg to the sender.

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        """
        defines what to do with the msg when the q receives a msg.
        in ASR: on response should gets the body and produce transcription on top.
        """
        # corr_id is the unique if for every request.
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        self.connection.process_data_events(time_limit=None)
        return self.response # rmq is binary protocol


asr_rpc = ASRRpcClient()

print(" [x] Requesting transcribe audio length = 5")
response = asr_rpc.call(5)
print(" [.] Got %r" % response)