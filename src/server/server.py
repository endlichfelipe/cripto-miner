from xmlrpc.server import SimpleXMLRPCServer
from .cryptominer import SequentialCryptoMiner, RandomCryptoMiner

class CryptoMinerServer:
    def __init__(self, host, port, sequential=True):
        print('CryptoMinerServer: Instantiating XML-RPC server')

        self.host = host
        self.port = port
        self.cryptominer = SequentialCryptoMiner() if sequential else RandomCryptoMiner()
        self.server = SimpleXMLRPCServer((host, port))
        self.server.register_function(self.get_transaction_id, 'getTransactionID')
        self.server.register_function(self.get_challenge, 'getChallenge')
        self.server.register_function(self.get_transaction_status, 'getTransactionStatus')
        self.server.register_function(self.submit_challenge, 'submitChallenge')
        self.server.register_function(self.get_winner, 'getWinner')
        self.server.register_function(self.get_seed, 'getSeed')
        

    def get_transaction_id(self):
        return self.cryptominer.get_transaction_id()

    def get_challenge(self, transaction_id):
        return self.cryptominer.get_challenge(transaction_id)

    def get_transaction_status(self, transaction_id):
        return self.cryptominer.get_transaction_status(transaction_id)

    def submit_challenge(self, transaction_id, client_id, seed):
        return self.cryptominer.submit_challenge(transaction_id, client_id, seed)

    def get_winner(self, transaction_id):
        return self.cryptominer.get_winner(transaction_id)

    def get_seed(self, transaction_id):
        return self.cryptominer.get_seed(transaction_id)

    def run(self):
        print('CryptoMinerServer: Listening for XML-RPC requests on port {}'.format(self.port))
        self.server.serve_forever()