from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from twisted.internet import stdio
from twisted.protocols import basic
from twisted.internet.defer import Deferred
from Defination import StateClient, Result, Boolean


class Echo(basic.LineReceiver):
    from os import linesep as delimiter
    delimiter = b'\n'

    def __init__(self,CommandToWrite):
        self.functionToFire = CommandToWrite

    def connectionMade(self):
        self.transport.write(b'>>> ')

    def lineReceived(self, line):
        self.CreateDeferred()
        self.sendLine(line)
        self.transport.write(b'>>> ')
        self.deferred.callback(line)

    def CreateDeferred(self):
        self.deferred = Deferred()
        self.deferred.addCallback(self.functionToFire)

class Greeter(Protocol):

    def __init__(self,ask_user_password):
        self.functionToFire = ask_user_password
        self.State = StateClient.IDLE

    def connectionMade(self):
        self.transport.write('Connection Made with Client'.encode())
        self.Create_deferred_To_command("Username Password ")
        self.State = StateClient.LOGGING

    def sendMessage(self, msg):

        if self.State == StateClient.Request:
            if msg == 'Y' or msg == 'y':
                msg = Boolean.YES
            elif msg == 'N' or msg == 'n':
                msg = Boolean.NO

        strByte = bytes(msg.encode())
        print("Sne")
        self.transport.write(strByte)

    def dataReceived(self, data: bytes):

        if self.State == StateClient.LOGGING:
            if data == Result.OK:
                self.State = StateClient.READY
                self.Create_deferred_To_command("Authentication Succeded ")
                self.sendMessage(Result.OK)

            elif data == Result.FAILED:
                self.Create_deferred_To_command("Authentication Failed ")
                self.Create_deferred_To_command("Username Password ")

        elif self.State == StateClient.READY:
            if data == Result.FAILED:
                self.Create_deferred_To_command("User not found ")

            elif data == Result.OK:
                self.State = StateClient.WAIT

            elif data == Result.REQUEST:
                self.State = StateClient.REQUEST

            else:
                self.Create_deferred_To_command()
                self.Create_deferred_To_command("User Online : ")
                self.Create_deferred_To_command(data)

        elif self.State == StateClient.REQUEST:

            if data == Result.FAILED:
                self.State = StateClient.READY
                self.Create_deferred_To_command("Connection error")

            elif data == Result.OK:
                self.State = StateClient.CHATTING
                self.Create_deferred_To_command("Connected...")

            else:
                self.Create_deferred_To_command("Connection request received From : ")
                self.Create_deferred_To_command(data)
                self.Create_deferred_To_command("Type Y (yes) to accept or N (No) to refuse")

        elif self.State == StateClient.WAIT:

            if data == Result.FAILED:
                self.State == StateClient.READY
                self.Create_deferred_To_command("User refused the invitation")

            elif data == Result.OK:
                self.Create_deferred_To_command("User accepted the invitation")
                self.Create_deferred_To_command("Chatting....")
                self.State == StateClient.CHATTING

        elif self.State == StateClient.CHATTING:
            if data == Result.FAILED:
                self.State == StateClient.READY
                self.Create_deferred_To_command("Chat interrupted...")

            self.Create_deferred_To_command(data)

        print(data)

    def get_Greeter_Deferred(self):
        deferred = Deferred()
        return deferred

    def Create_deferred_To_command(self,line):
        deferred_ask = Deferred()
        deferred_ask.addCallback(self.functionToFire)
        deferred_ask.callback(line)

class ManageConnection():

    def __init__(self):
        self.echo = Echo(self.CommandToWrite)
        stdio.StandardIO(self.echo)
        self.greeter = Greeter(self.write_to_command)
        point = TCP4ClientEndpoint(reactor, "localhost", 1234)
        d = connectProtocol(point, self.greeter)
        reactor.run()

    def CommandToWrite(self,mess):
        self.greeter.sendMessage(mess.decode())

    def write_to_command(self,line):
        self.echo.transport.write(line.encode())


ManageConnection()
