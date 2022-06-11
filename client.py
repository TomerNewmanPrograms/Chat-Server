import threading
import socket


class Client:

    SERVER_IP='localhost'
    PORT=10000

    def __init__(self,serve_ip=SERVER_IP,port=PORT):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((serve_ip, port))

    def __del__(self):
        self.client.close()

    def close(self):
        """close the client"""
        self.client.close()

    def send_message(self):
        """send message to the server"""
        while True:
            msg = input("")
            self.client.send(f'{nickname}: {msg}'.encode('utf-8'))

    def receive_messages(self):
        """receive a message from the server"""
        while True:
            data = self.client.recv(100)
            msg = data.decode('utf-8')
            if msg == "Nickname":
                self.client.send(f'{nickname}'.encode('utf-8'))
            else:
                print(msg)

    def threads_loop(self):
        """starts the client receiving and sending threads"""
        receiver=threading.Thread(target=self.receive_messages)
        receiver.start()
        sender=threading.Thread(target=self.send_message)
        sender.start()


nickname = input("Please enter your nickname: ")
client=Client()
client.threads_loop()