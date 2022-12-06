# ASR service using RabbitMQ

A simple ASR service written by RabbitMQ.

## Usage
1. download and install rabbitmq. [To have it running in a container](https://www.rabbitmq.com/download.html):
```
# latest RabbitMQ 3.11
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management
```
2. installation
```
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```
3. Run the server
```
python server.py
```
4. Open nother terminal window, and run the client
```
python client.py
```

## Reference
1. [How to write RPC style service using RabbitMQ?](https://www.rabbitmq.com/tutorials/tutorial-six-python.html)
2. [Run simple inference using Hidden-Unit BERT Model](https://huggingface.co/transformers/v4.11.3/model_doc/hubert.html)
