# Should import blockchain?
# import blockchain
import datetime
from hashlib import sha256
import json
capacity = 10 

class Block:
	def __init__(self, id, previousHash, capacity, difficulty, listOfTransactions=[], current_hash=None, nonce=0):
		##set
		# nonce = 0 only if we dont give any argument 
		self.id = id
		self.previousHash = previousHash
		self.timestamp = datetime.datetime.utcnow()
		self.current_hash = current_hash   
		self.nonce = nonce 
		self.capacity = capacity
		self.difficulty = difficulty
		self.listOfTransactions = listOfTransactions

	def myHash(self):
		return (sha256.new(self.dump().encode()).hexdigest())

	def add_transaction(self, transaction):
		if len(self.listOfTransactions) < capacity:
			self.listOfTransactions.append(transaction)
		pass

	def dump(self):
		# Structure with trans, nonce, timestamp to use them in calculation of hash
		return json.dumps(dict(transactions=self.transactions,nonce=self.nonce,timestamp=self.timestamp), sort_keys=True)

