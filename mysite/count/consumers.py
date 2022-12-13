from channels.generic.websocket import WebsocketConsumer

class Counting(WebsocketConsumer):
    def connect(self):
        self.accept()
        print(1)

    def disconnect(self, code):
        print(0)