from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
import Defination

class QOTD(Protocol):

    def __init__(self):
        self.ListClients= []

    def connectionMade(self):
        strByte = bytes('hello from server'.encode())
        self.transport.write(strByte)
        self.ListClients.append(self)
        print("connection made with client")

    def dataReceived(self, data: bytes):
        print(data)
    def sendLine(self,mess):
        self.transport.write(mess)

    def connectionLost(self, reason):
        print(reason)



class QOTDFactory(Factory):
    # This will be used by the default buildProtocol to create new protocols:
    protocol = QOTD
    def __init__(self, quote):
        self.quote = quote

endpoint = TCP4ServerEndpoint(reactor, 1234)
endpoint.listen(QOTDFactory("configurable quote"))
reactor.run()
