#python
import logging
import socket
import ConfigParser
import time

class GregoBot:
    """Bot class"""
    
    settings_file = ""
    connect_host = ""
    connect_port = 0
    connect_nick = ""
    connect_ident = ""
    connect_real_name = ""
    connect_password = ""
    connect_channel_list = []
    sock = socket.socket()
    silent_mode = False
        
    def __init__(self):
        ## Todo - Add a unique instance number to the name.
        self.name='GregoBot'
        logging.info('New class instantiated.')
        
    def talk(self, channel, text):
        self.sock.send("PRIVMSG {} :{}\r\n".format(channel, text))
        
    def connect(self, file):
        # Setup Basic Variables
        self.settings_file = file
        settings = ConfigParser.ConfigParser()
        settings.read(self.settings_file)
        self.connect_host = settings.get('Base', 'ServerHost')
        self.connect_port = settings.getint('Base', 'ServerPort')
        self.connect_nick = settings.get('Base', 'Nick')
        self.connect_ident = settings.get('Base', 'Ident')
        self.connect_real_name = settings.get('Base', 'RealName')
        self.connect_password = settings.get('Base', 'Pass')
        logging.info('Variables set from file {}'.format(self.settings_file))
        
        # Start the connect
        logging.info('Connecting to server {} on port {}.'.format(self.connect_host, self.connect_port))
        self.sock.connect((self.connect_host, self.connect_port))
        logging.info('Server Says {}\n'.format(self.sock.recv(10240)))
        
        logging.info('Sending Nick as {}'.format(self.connect_nick))
        self.sock.send('NICK {}\r\n'.format(self.connect_nick))
        logging.info('Server Says {}\n'.format(self.sock.recv(10240)))
        
        logging.info('Identifying to server {1} as {0} with real name {2} '.format(self.connect_ident, self.connect_host, self.connect_real_name))
        self.sock.send('USER {} {} bla :{}\r\n'.format(self.connect_ident, self.connect_host, self.connect_real_name))
        logging.info('Server Says {}\n'.format(self.sock.recv(10240)))
        
        logging.info('Identifying to NickServ with Nick {}'.format(self.connect_nick))
        self.sock.send('PRIVMSG NICKSERV :IDENTIFY {} {}\r\n'.format(self.connect_nick, self.connect_password))
        logging.info('Server Says {}\n'.format(self.sock.recv(10240)))
       
        logging.info('Connection Complete.')

    def join_channel(self, channel):
        logging.info('Joining Channel {}.'.format(channel))
        self.sock.send('JOIN {}\r\n'.format(channel))
        logging.info('Server Says {}\n'.format(self.sock.recv(10240)))
        if not self.silent_mode:
            self.talk(channel, 'Hello World!')
        
    def pong(self, channel, pingident):
        logging.info('Sending Pong with unique identifier {}.'.format(pingident))
        self.sock.send("PONG {}\r\n".format(pingident))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logging.info('Starting GregoBot using default settings. Logging set to level INFO')
    bot = GregoBot()
    bot.connect('GregoBot_defaults.conf')
    time.sleep(10)
    bot.join_channel('#test1984')