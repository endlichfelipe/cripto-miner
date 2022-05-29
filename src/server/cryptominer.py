import random
import hashlib
from abc import ABC, abstractmethod

class CryptoMinerTransaction:
    def __init__(self, challenge):
        self.challenge = challenge
        self.seed = self._generate_seed()
        self.hash = self._generate_hash()

    def get_challenge(self):
        return self._challenge
    def set_challenge(self, challenge):
        assert challenge is not None, 'Challenge must be defined'
        assert type(challenge) == int, 'Challenge must be an integer'
        assert challenge > 0, 'Challenge must be greater than zero'
        assert challenge <= 2**7, 'Challenge must be less than 2**7'
        self._challenge = challenge
    challenge = property(get_challenge, set_challenge)

    def _generate_seed(self):
        return ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for _ in range(self.challenge))

    def _generate_hash(self):
        return hashlib.sha1(self.seed.encode()).hexdigest()

    def solve(self, seed):
        return self.hash == hashlib.sha1(seed.encode()).hexdigest()

class CryptoMiner(ABC):
    def __init__(self):
        self.transactions = []
        self.transactions.append({
            'transaction': CryptoMinerTransaction(1),
            'winner': -1
        })

    @abstractmethod 
    def _generate_transaction(self):
        pass

    def get_transaction_id(self):
        return len(self.transactions) - 1

    def get_challenge(self, transaction_id):
        if transaction_id >= len(self.transactions): return -1
        else: return self.transactions[transaction_id]['transaction'].challenge

    def get_transaction_status(self, transaction_id):
        if transaction_id >= len(self.transactions): return -1
        elif self.transactions[transaction_id]['winner'] == -1: return 1
        else: return 0

    def submit_challenge(self, transaction_id, client_id, seed):
        if transaction_id >= len(self.transactions): return -1
        if self.transactions[transaction_id]['winner'] != -1: return 2
        if self.transactions[transaction_id]['transaction'].solve(seed):
            self.transactions[transaction_id]['winner'] = client_id
            self._generate_transaction()
            return 1
        else: return 0

    def get_winner(self, transaction_id):
        if transaction_id >= len(self.transactions): return -1
        elif self.transactions[transaction_id]['winner'] == -1: return 0
        else: return self.transactions[transaction_id]['winner']

    def get_seed(self, transaction_id): 
        return {
            'transaction_id': transaction_id,
            'seed': self.transactions[transaction_id]['transaction'].seed,
            'status': self.get_transaction_status(transaction_id)
        }

class SequentialCryptoMiner(CryptoMiner):
    def __init__(self):
        super().__init__()

    def _generate_transaction(self):
        challenge = min(self.transactions[-1]['transaction'].challenge + 1, 2**7)
        self.transactions.append({
            'transaction': CryptoMinerTransaction(challenge),
            'winner': -1
        })

class RandomCryptoMiner(CryptoMiner):
    def __init__(self):
        super().__init__()

    def _generate_transaction(self):
        challenge = random.randint(1, 2**7)
        self.transactions.append({
            'transaction': CryptoMinerTransaction(challenge),
            'winner': -1
        })
