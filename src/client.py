import sys
from time import sleep
import xmlrpc.client
from itertools import product
from threading import Thread, Condition

value_found = False
c = Condition()

class ChallengeThread(Thread):
    def __init__(self, server, port, transaction_id, seed):
        Thread.__init__(self)
        self.server = server
        self.port = port
        self.seed = seed
        self.transaction_id = transaction_id
        self.result = None

    def run(self):
        global value_found

        if value_found:
            return

        try:
            proxy = xmlrpc.client.ServerProxy("http://{}:{}".format(self.server, self.port))
            challenge_result = proxy.submit_challenge(self.transaction_id, self.ident, self.seed)
            if (challenge_result == 1):
                c.acquire()
                value_found = True
                c.notify_all()
                print('Seed found: {}'.format(self.seed))
        except Exception as e:
            print("Error: {}".format(e))
            self.result = False

class ClientApplication:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = xmlrpc.client.ServerProxy('http://{}:{}'.format(host, port))
    
    def _get_transaction_id(self):
        print(self.server.get_transaction_id())

    def _get_challenge(self):
        transaction_id = int(input('Transaction ID: '))
        print(self.server.get_challenge(transaction_id))

    def _get_transaction_status(self):
        transaction_id = int(input('Transaction ID: '))
        print(self.server.get_transaction_status(transaction_id))

    def _get_winner(self):
        transaction_id = int(input('Transaction ID: '))
        print(self.server.get_winner(transaction_id))
    
    def _get_seed(self):
        transaction_id = int(input('Transaction ID: '))
        print(self.server.get_seed(transaction_id))

    def _minerar(self):
        transaction_id = int(input('Transaction ID: '))
        challenge = int(self.server.get_challenge(transaction_id))

        threads = []
        for seed in self._generate_seed(challenge):
            threads.append(ChallengeThread(self.host, self.port, transaction_id, seed))
            threads[-1].start()

    def run(self, command):
        if   command == 'getTransactionId'     : self._get_transaction_id()
        elif command == 'getChallenge'         : self._get_challenge()
        elif command == 'getTransactionStatus' : self._get_transaction_status()
        elif command == 'getWinner'            : self._get_winner()
        elif command == 'getSeed'              : self._get_seed()
        elif command == 'Minerar'              : self._minerar()

    def _generate_seed(self, challenge):
        valid_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        combinations = product(valid_characters, repeat=challenge)
        candidate = next(combinations, None)
        while candidate:
            word = ''.join(candidate)
            candidate = next(combinations, None)
            yield word

n = len(sys.argv)
if n != 4:
    print('Usage: python3 client.py <host> <port> <command>')
    sys.exit(1)

host = sys.argv[1]
port = sys.argv[2]
command = sys.argv[3]

client = ClientApplication(host, port)
client.run(command)