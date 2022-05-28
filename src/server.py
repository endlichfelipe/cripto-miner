from xmlrpc.server import SimpleXMLRPCServer

class CryptoMinerServer:
    def __init__(self, host, port):
        print('CryptoMinerServer: Instantiating XML-RPC server')

        self.host = host
        self.port = port
        self.server = SimpleXMLRPCServer((host, port))
        self.server.register_function(self.get_transaction_id, 'getTransactionID')
        self.server.register_function(self.get_challenge, 'getChallenge')
        self.server.register_function(self.get_transaction_status, 'getTransactionStatus')
        self.server.register_function(self.submit_challenge, 'submitChallenge')
        self.server.register_function(self.get_winner, 'getWinner')
        self.server.register_function(self.get_seed, 'getSeed')
        

    def get_transaction_id(self):
        # Retorna o valor atual <int> da transação com desafio ainda pendente de solução.
        pass

    def get_challenge(self, transaction_id):
        """
            Se transactionID for válido, retorne o valor do desafio associado a ele.
            Se não, retorne -1.
        """
        pass

    def get_transaction_status(self, transaction_id):
        """
            Se transactionID for válido, retorne 0 se o
            desafio associado a essa transação já foi
            resolvido, retorne 1 caso a transação ainda
            possua desafio pendente. Retorne -1 se a
            transactionID for inválida.
        """
        pass

    def submit_challenge(self, transaction_id, client_id, seed):
        """
            Submete uma semente (seed) para o hashing
            SHA-1 que resolve o desafio proposto para a
            referida transactionID. Retorne 1 se a seed
            para o desafio for válido, 0 se for inválido, 2
            se o desafio já foi solucionado, e -1 se a
            transactionID for inválida.
        """
        pass

    def get_winner(self, transaction_id):
        """
            Retorna o clientID do vencedor da transação
            transactionID. Retorne 0 se transactionID
            ainda não tem vencedor e -1 se transactionID
            for inválida.
        """
        pass

    def get_seed(self, transaction_id):
        """
            Retorna uma estrutura de dados (ou uma
            tupla) com o status, a seed e o desafio
            associado à transactionID.
        """
        pass

    def run(self):
        print('CryptoMinerServer: Listening for XML-RPC requests on port {}'.format(self.port))
        self.server.serve_forever()