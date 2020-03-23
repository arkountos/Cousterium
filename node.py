import block
import wallet
import Crypto
import Crypto.Random
from Crypto.Hash import SHA384
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import json

class Node:

	# FIVOS
	# Only one node is running on each VM. Each node only has one wallet.

	def __init__(self, address, current_block=None, node_id=0, chain=[], NBC=0, ring=[]):
		##set

		self.chain = chain
		self.id = node_id
		self.NBC = NBC		
		self.address = address # Address is a string
		self.wallet = self.create_wallet()
		self.ring = ring  #here we store information for every node, as its id, its address (ip:port) its public key and its balance 
		self.current_block = current_block

	def set_id(self, id):
		self.id = id

	def create_new_block(self, id, previousHash, capacity, difficulty):
		return block.Block(id, previousHash, capacity, difficulty)		

	def create_wallet(self):
		#create a wallet for this node, with a public key and a private key
		return wallet.Wallet(self.address, []) # TODO Add constructor fields

	def register_node_to_ring(self, id, public_key):
		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs
		self.ring.append({id: public_key})



	def broadcast_transaction():
		pass


	def verify_signature(self, transaction):
		#receiver node verifies signature of sender node
		signature = transaction.signature
		h = SHA384.new(json.dumps(transaction.to_dict()).encode()).hexdigest()
		public_key = transaction.sender
		verifier = PKCS1_v1_5.new(public_key)
		if(verifier.verify(h, signature)):
			return True
		else:
			return False


	def validate_transaction():
		#use of signature and NBCs balance
		pass


	def add_transaction_to_block(self, transaction):
		#if enough transactions  mine, then create new block
		capacity = self.current_block.capacity
		self.current_block.add_transaction(transaction)
		if(len(self.current_block.listOfTransactions) == capacity):
				print("Block is ready for mining")
				self.mine_block(self.current_block)
		self.current_block = self.create_new_block(self.current_block.id + 1, self.current_block.current_hash, self.current_block.capacity, self.current_block.difficulty)
		pass



	def mine_block():
		pass



	def broadcast_block():
		pass


		

	# def valid_proof(.., difficulty=MINING_DIFFICULTY):
	# 	pass




	#concencus functions

	def valid_chain(self, chain):
		#check for the longer chain accroose all nodes
		pass


	def resolve_conflicts(self):
		#resolve correct chain
		pass



