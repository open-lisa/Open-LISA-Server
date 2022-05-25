class MessageProtocol:
    def __del__(self, connection):
        raise NotImplementedError("Please Implement this method: destructor")

    def send_msg(self, msg, encode=True):
        raise NotImplementedError("Please Implement this method: send_msg")

    def receive_msg(self, decode=True):
        raise NotImplementedError("Please Implement this method: receive_msg")

    def __recvall(self, n):
        raise NotImplementedError("Please Implement this method: __recvall")
