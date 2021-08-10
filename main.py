from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
import Defination

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
            "connected_To": self,
            "State": Defination.StateClient.LOGGING
        }
        # Dictionary of client added to the list
        self.ListClients.append(client)
        print("connection made with client")

    def dataReceived(self, data: bytes):
        print(data)

    def sendLine(self,mess):
        self.transport.write(mess)

    def connectionLost(self, reason):
        #client = list(filter(lambda client: client['client'] == self, self.ListClients))
        # Delete the client dictionary from list
        for i in range(len(self.ListClients)):
            if self.ListClients[i]['client'] == self:
                del self.ListClients[i]
                break
         #self.ListClients.remove(list(client))
        print(reason)



class QOTDFactory(Factory):
    # This will be used by the default buildProtocol to create new protocols:
    protocol = QOTD
    def __init__(self, quote):
        self.quote = quote

endpoint = TCP4ServerEndpoint(reactor, 1234)
endpoint.listen(QOTDFactory("configurable quote"))
reactor.run()
