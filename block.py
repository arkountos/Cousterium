# Should import blockchain?
# import blockchain
import datetime
from haslib import sha256
import json



class Block:
	def __init__(self, *nonce, previousHash):
		##set
		
		self.previousHash = previousHash
		self.timestamp = datetime.datetime.utcnow()
		self.hash
		if nonce == None:
			self.nonce
		else:
			self.nonce = 0 
		self.listOfTransactions = []
		pass
	
	def myHash():
		block_string = json.dumps(self.__dict__, sort_keys=True)
    	return sha256(block_string.encode()).hexdigest()

	def add_transaction(transaction, blockchain):
		#add a transaction to the block
		pass