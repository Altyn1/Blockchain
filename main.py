import hashlib 
import json 
from time import time  
class Block:     
    def __init__(self, index, previous_hash, transactions, timestamp=None):         
        self.index = index         
        self.previous_hash = previous_hash         
        self.timestamp = timestamp or time()         
        self.transactions = transactions         
        self.nonce = 0         
        self.merkle_root = self.calculate_merkle_root()   
        self.hash = self.calculate_hash()  
    def calculate_merkle_root(self):         
            if len(self.transactions) == 0:             
                return hashlib.sha256(b"").hexdigest()         
            transaction_hashes = [hashlib.sha256(json.dumps(tx).encode()).hexdigest() for tx in self.transactions]         
            while len(transaction_hashes) > 1:             
                if len(transaction_hashes) % 2 != 0:                 
                    transaction_hashes.append(transaction_hashes[-1])             
                new_hashes = []             
                for i in range(0, len(transaction_hashes), 2):                 
                        combined_hash = hashlib.sha256((transaction_hashes[i] + transaction_hashes[i + 1]).encode()).hexdigest()                 
                        new_hashes.append(combined_hash)             
                transaction_hashes = new_hashes         
            return transaction_hashes[0]      
                    
    def calculate_hash(self):         
        block_dict = {             
            'index': self.index,             
            'previous_hash': self.previous_hash,             
            'timestamp': self.timestamp,             
            'transactions': self.transactions,             
            'nonce': self.nonce,             
            'merkle_root': self.merkle_root         
            }         
        block_str = json.dumps(block_dict, sort_keys=True)         
        return hashlib.sha256(block_str.encode()).hexdigest()  
    
class Blockchain:     
        def __init__(self):         
            self.chain = []         
            self.mempool = []         
            self.initialize_genesis_block()   

        def initialize_genesis_block(self):         
                genesis_block = Block(             
                    index=0,             
                    previous_hash="0",             
                    transactions=["Genesis Transaction"]         
                    )         
                self.chain.append(genesis_block)      
        
        def is_valid_block(self, block, previous_block):         
                    if block.calculate_hash() != block.hash:             
                        return False         
                    if previous_block.calculate_hash() != block.previous_hash:             
                        return False         
                    return True      
        def is_valid_chain(self):         
            for i in range(1, len(self.chain)):
                     current_block = self.chain[i]            
                     previous_block = self.chain[i - 1]             
                     if not self.is_valid_block(current_block, previous_block):                 
                        return False         
            return True      
        def add_new_block(self, transactions):         
            last_block = self.chain[-1]         
            index = last_block.index + 1         
            previous_hash = last_block.calculate_hash()         
            new_block = Block(             
                index=index,             
                previous_hash=previous_hash,             
                transactions=transactions         
            )         
            self.chain.append(new_block)      
        
        def calculate_hash(self, block):         
                block_string = json.dumps({             
                     'index': block.index,             
                     'previous_hash': block.previous_hash,             
                     'timestamp': block.timestamp,             
                     'transactions': block.transactions,             
                     'nonce': block.nonce,             
                     'merkle_root': block.merkle_root         
                     }, sort_keys=True).encode()         
                return hashlib.sha256(block_string).hexdigest()  
if __name__ == "__main__":     
    blockchain = Blockchain()     
    transaction1 = {'send': 'Bektas', 'get': 'Ergali', 'amount': 10}     
    transaction2 = {'send': 'Ergali', 'get': 'Bektas', 'amount': 5}     
    blockchain.add_new_block([transaction1])     
    blockchain.add_new_block([transaction2])     
    
    is_valid = blockchain.is_valid_chain()     
    print(is_valid)