import sys
import socket
import string
import time
import ConfigParser
import random

config = ConfigParser.ConfigParser()
config.read('gregobo.conf')

HOST=config.get('Base','ServerHost')
PORT=config.getint('Base','ServerPort')
NICK=config.get('Base','Nick')
IDENT=config.get('Base','Ident')
REALNAME=config.get('Base','RealName')
MASTER=config.get('Base','Master')
PASSWORD=config.get('Base','Pass')
INITCHANNEL=config.get('Base','InitChannel')
QUOTEFILE='./lines/pratchett.quote'
s=socket.socket( )

def connect():
    print "-----------Entering Connect-----------\n"
    s.connect((HOST, PORT))
    print s.recv(1024)
    s.send("NICK %s\r\n" % NICK)
    print s.recv(1024)
    s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
    print s.recv(1024)
    s.send("PRIVMSG NICKSERV :IDENTIFY %s %s\r\n" % (NICK, PASSWORD))
    print s.recv(1024)
....
def joinchannel(channel):
    print "-----------Entering JoinChannel---------\n"
    s.send("JOIN %s\r\n" % channel)
    s.send("PRIVMSG %s :At the entrance, my bare feet on the dirt floor, Here, gusts of heat; at my back, white clouds. I stare and stare. It seems I was called for this: To gl#

def pingpong(channel, line):
    print "-----------Entering PingPong----------\n"
    s.send("PONG %s\r\n" % line[1])
    s.send("PRIVMSG %s :PONG!! %s\r\n" % (channel, line[1]))


def getQuote(channel):
    print "-----------Entering GetQuote-----------\n"
    count=0
    f = open(QUOTEFILE, 'r')
    for line in f:
        if line == '%\n':
            count+=1
    quotenum = random.randrange(1,count)
    count=0
    f.seek(0)
    for line in f:
        if (count == quotenum - 1) and line != '%\n':
            s.send("PRIVMSG %s :%s\r\n" % (channel, line))
        if line == '%\n':
            count += 1
    f.close()


def main():.
    readbuffer = ''
    connect()
    joinchannel(INITCHANNEL)
    print "--------------Starting Loop------------\n"
    while 1:
        readbuffer=readbuffer+s.recv(1024)
        temp=string.split(readbuffer, "\n")
        readbuffer=temp.pop( )
        for line in temp:
            line=string.rstrip(line)
            print "GreGoBo :::: " + line
            line=string.split(line)
            if(line[0]=="PING"):
                pingpong(INITCHANNEL, line)
            if(line.count(':Quote')==1):
                print "GreGoBo :::: QUOTING"
                getQuote(INITCHANNEL)
            if(line.count('Pai')==1 or line.count(':Pai')==1):
                s.send("PRIVMSG %s :Pai sucks!\r\n" % (INITCHANNEL))


main()
