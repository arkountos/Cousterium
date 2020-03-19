import block
#import transaction
#import wallet 

class Blockchain:
    difficulty = 5

    def __init__(self):
        self.chain = []

    def create_genesis_block(self):
        genesis_block = Block(0,1,'placeholder',[])
        genesis_block.current_hash = genesis_block.myHash()
        self.chain.append(genesis_block)
        
    def proof_of_work(self, block):
        block.nonce = 0
        current_hash = block.myHash()
        
        while not current_hash.startswith('0'*Blockchain.difficulty):
            block.nonce = +1
            current_hash = block.myHash()
        
        return current_hash

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())

    def add_block(self, block, proof):

        previousHash = self.last_block().previousHash

        if previousHash != block.previousHash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.current_hash = proof
        self.chain.append(block)  
        
        return True   

    def last_block(self):
        return self.chain[-1]
