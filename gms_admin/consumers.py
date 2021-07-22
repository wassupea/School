from channels.consumer import SyncConsumer

class EchoConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('connencted')

    def websocket_receive(self, event):
        print("received")
        print(event)