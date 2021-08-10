from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import stdio
from twisted.protocols import basic
from twisted.internet.defer import Deferred
import Defination
"""
module_name, package_name, ClassName, method_name, ExceptionName, function_name,
GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name, local_var_name.
"""



class Echo(basic.LineReceiver):
    from os import linesep as delimiter
    delimiter = b'\n'

    def __init__(self,CommandToWrite):
        self.functionToFire = CommandToWrite
        self.state = Defination.StateClient.IDLE


    def connectionMade(self):
        self.transport.write(b'>>> ')
        strByte = bytes('>>>'.encode())
        self.transport.write(strByte)

    def lineReceived(self, line):
        self.CreateDeferred()
        self.sendLine(line)
        self.transport.write(b'>>> ')
        self.deferred.callback(line)

    def CreateDeferred(self):
        self.deferred = Deferred()
        self.deferred.addCallback(self.functionToFire)


class Greeter(Protocol):

    def connectionMade(self):
        self.transport.write('Connection Ma+de with Client olghhgvh'.encode())
        self.sendMessage("hello")

    def sendMessage(self, msg):
        strByte = bytes(msg.encode())
        print("Sne")
        self.transport.write(strByte)

    def dataReceived(self, data: bytes):
        print(data)


    def get_Greeter_Deferred(self):
        self.deferred = Deferred()
        return self.deferred


class ManageConnection():

    def __init__(self):
        echo = Echo(self.CommandToWrite)
        stdio.StandardIO(echo)
        self.greeter = Greeter()
        point = TCP4ClientEndpoint(reactor, "localhost", 1234)
        d = connectProtocol(point, self.greeter)
        reactor.run()

    def CommandToWrite(self,mess):
        self.greeter.sendMessage(mess.decode())
        print(mess)


ManageConnection()
