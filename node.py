import block
import wallet

class Node:

	# FIVOS
	# Only one node is running on each VM. Each node only has one wallet.

	def __init__(self, node_id, address, chain=[], NBC=0, ring=[]):
		##set

		self.chain = chain
		self.id = node_id
		self.NBC = NBC		
		self.address = address # Address is a string
		self.wallet = self.create_wallet()
		self.ring = ring  #here we store information for every node, as its id, its address (ip:port) its public key and its balance 




	def create_new_block():
		pass

	def create_wallet(self):
		#create a wallet for this node, with a public key and a private key
		return wallet.Wallet(self.address, []) # TODO Add constructor fields

	def register_node_to_ring():
		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs
		pass


	def create_transaction(sender, receiver, signature):
		#remember to broadcast it
		pass


	def broadcast_transaction():
		pass





	def validdate_transaction():
		#use of signature and NBCs balance
		pass


	def add_transaction_to_block():
		#if enough transactions  mine
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



