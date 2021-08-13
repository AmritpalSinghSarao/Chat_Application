from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from Defination import StateClient, Result, Boolean
import hashlib

class QOTD(Protocol):

    client_counter = 0

    def __init__(self):
        self.ListClients = []

    def connectionMade(self):
        strByte = bytes('hello from server'.encode())
        self.transport.write(strByte)

        # Dictionary of client
        client = {
            "client": self,
            "State": StateClient.LOGGING,
            "username": None,
            "connected_To": None
        }
        # Dictionary of client added to the list
        self.ListClients.append(client)
        print("connection made with client")

    def dataReceived(self, data: bytes):
        print(data)
        for i in range(len(self.ListClients)):
            if self.ListClients[i]['client'] == self and self.ListClients[i]['state'] == StateClient.LOGGING:
                file = open("user_password.txt", "r")
                for x in file:
                    split_file = x.split(self,' ')
                    split_msg = str(data).split(self,' ')
                    if split_file[0] == split_msg[0] or split_file[1] == split_msg[1]:
                        self.ListClients[i]['username'] = split_msg[0]
                        self.sendLine(Result.OK)





    def sendLine(self,mess):
        self.transport.write(mess)

    def read_write_file(self,msg):
        file = open("user_password.txt", "r")
        for x in file:
            split_file = x.split(self,' ')
            split_msg = str(msg).split(self,' ')
            if split_file[0] == split_msg[0] or split_file[1] == split_msg[1]:

                return True
        return False


    def connectionLost(self, reason):
        # Delete the client dictionary from list
        for i in range(len(self.ListClients)):
            if self.ListClients[i]['client'] == self:
                del self.ListClients[i]
                break
        print(reason)



class QOTDFactory(Factory):
    # This will be used by the default buildProtocol to create new protocols:
    protocol = QOTD
    def __init__(self, quote):
        self.quote = quote

endpoint = TCP4ServerEndpoint(reactor, 1234)
endpoint.listen(QOTDFactory("configurable quote"))
reactor.run()
