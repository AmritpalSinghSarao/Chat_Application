from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

class QOTD(Protocol):

    def connectionMade(self):
        # self.factory was set by the factory's default buildProtocol:
        strByte = bytes('hello from server'.encode())
        self.transport.write(strByte)
        print("connection made with client")
        #self.transport.loseConnection()
    def dataReceived(self, data: bytes):
        print(data)
    def sendLine(self,mess):
        self.transport.write(mess)



class QOTDFactory(Factory):
    # This will be used by the default buildProtocol to create new protocols:
    protocol = QOTD
    def __init__(self, quote=None):
        self.quote = quote or 'An apple a day keeps the doctor away'

endpoint = TCP4ServerEndpoint(reactor, 1234)
endpoint.listen(QOTDFactory("configurable quote"))
reactor.run()
