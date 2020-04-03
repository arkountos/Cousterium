import block
#import transaction
#import wallet 

class Blockchain:

    def __init__(self):
        self.chain = []

    def add_block(self, block):

        self.chain.append(block)  
        return True

    def last_block(self):
        return self.chain[-1]


    def print_chain(self):
        i = 0
        for bentry in self.chain:
            print('=======')
            print("Block ", i,)
            print(bentry.previousHash)
            transactions = bentry.listOfTransactions		
            j = 0
            for tentry in transactions:
                print('\t',j,': ',tentry.amount,tentry.index)
                j +=1
            i += 1       

