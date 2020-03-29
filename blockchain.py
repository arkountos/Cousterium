import block
#import transaction
#import wallet 

class Blockchain:
    difficulty = 5

    def __init__(self):
        self.chain = []

      
    def proof_of_work(self, block):
        block.nonce = 0
        current_hash = block.myHash()
        
        while not current_hash.startswith('0'*Blockchain.difficulty):
            block.nonce = +1
            current_hash = block.myHash()
        
        return current_hash

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.compute_hash())

    def add_block(self, block, proof, is_genesis=False):
	

        if (is_genesis == True):
                block.current_hash = block.myHash()
                self.chain.append(block)
                return True

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

    def view_transactions(self):
        #prints the transactions of the last block
        last_transactions = self.last_block().listOfTransactions
        for i in range(len(last_transactions)):
            print(last_transactions[i])
        
    def print_chain(self):
        i = 0
        for bentry in self.chain:
            print('=======')
            print("Block ", i)
            transactions = bentry.listOfTransactions
            j = 0
            print("------------")
            for tentry in transactions:
                print(j,': ',tentry.index)
                j +=1
            i += 1
                    