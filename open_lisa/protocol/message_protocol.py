class MessageProtocol:
    def disconnect(self):
        raise NotImplementedError("Please Implement this method: disconnect")

    def send_msg(self, msg, encode=True):
        raise NotImplementedError("Please Implement this method: send_msg")

    def receive_msg(self, decode=True):
        raise NotImplementedError("Please Implement this method: receive_msg")

    def __recvall(self, n):
        raise NotImplementedError("Please Implement this method: __recvall")
