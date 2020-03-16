# Should import blockchain?
# import blockchain
import datetime
from hashlib import sha256
import json
capacity = 10 

class Block:
	def __init__(self, id, previousHash, current_hash, listOfTransactions, nonce=0):
		##set
		
		self.id = id
		self.previousHash = previousHash
		self.timestamp = datetime.datetime.utcnow()
		self.current_hash == current_hash   
		self.nonce = nonce 
		self.listOfTransactions = []

	def dump(self):
		return json.dumps(dict(transactions=self.transactions,nonce=self.nonce,timestamp=self.timestamp), sort_keys=True)

	def myHash(self):
		return (sha256.new(self.dump().encode()).hexdigest())

	def add_transaction(self, transaction):
		if len(self.listOfTransactions) < capacity:
			self.listOfTransactions.append(transaction)
		pass
