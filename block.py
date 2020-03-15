# Should import blockchain?
# import blockchain
import datetime
from hashlib import sha256
import json
capacity = 10 

class Block:
	def __init__(self, id, previousHash, listOfTransactions, *nonce):
		##set
		
		self.id = id
		self.previousHash = previousHash
		self.timestamp = datetime.datetime.utcnow()
		#self.hash 
		if nonce == None:
			self.nonce = nonce
		else:
			self.nonce = 0 
		self.listOfTransactions = []

	def myHash(self):
		block_string = str(self.nonce)
		return (sha256(block_string.encode()).hexdigest())

	def add_transaction(self, transaction):
		if len(self.listOfTransactions) < capacity:
			self.listOfTransactions.append(transaction)
		pass

