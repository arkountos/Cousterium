import transaction
import block
import wallet
import blockchain
import Crypto
import Crypto.Random
from Crypto.Hash import SHA384
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import json
import jsonpickle
import requests


def verify_signature(my_transaction):
	#receiver node verifies signature of sender node
	signature = my_transaction.signature
	h = SHA384.new(json.dumps(my_transaction.to_dict()).encode()).hexdigest()
	public_key = my_transaction.sender
	verifier = PKCS1_v1_5.new(public_key)
	
	# TODO: FOR NOW, RETURN TRUE (see below)
	return True

	# TODO: There's an error inside if, fix!
	#if(verifier.verify(h, signature)):
	#	return True
	#else:
	#	return False


def validate_transaction(sender_wallet,my_transaction, my_wallet):
	# sender_wallet : Is a wallet Object
	# my_transaction : The transaction to be validated
	# use of signature and NBCs balance
	print("My_wallet at start of validate is: ")
	print(my_wallet.utxos)
	print("my_transaction is: ")
	print(my_transaction)
	t = my_transaction
	print("t is ")
	print(t)
	#w = sender_wallet
	if not verify_signature(t):
		raise Exception('Verification failure')
	
	#This was:
	#sender_utxos = sender_wallet.utxos[w.get_public_key()].copy()
	# And i changed it to:
	sender_utxos = sender_wallet.utxos[sender_wallet.get_public_key()].copy()
	balance = sender_wallet.calculate_balance()

	if balance < t.amount:
		raise Exception('Ftwxe')

	#Check if inputs are utxos
	for tid in t.inputs:
		print("tid is: ")
		print(tid)
		# tid = {'a': hs, ...}
		c = False
		for utxo in sender_utxos:
			#sender_utxo = {[], []}
			print("sender_utxo is: ")
			print(sender_utxos)
			print("utxo is")
			print(utxo)
			print("utxo['who']")
			print(utxo['who'])
			print("t.sender is: ")
			print(t.sender)
			#if tid['id'] == utxo['id'] and utxo['who'] == t.sender:
			if tid['id'] == utxo['id']:
				c = True
				print("my_wallet.utxos is:")
				print(my_wallet.utxos)
				my_wallet.utxos[t.sender].remove(utxo)
				break

	if not c:
		raise Exception('Input not utxo')

	t.outputs = [{
		'id': t.index,
		'who': t.sender,
		'amount': balance - t.amount
	},{
		'id': t.index,
		'who': t.recipient,
		'amount': t.amount
	}]

	if t.recipient not in my_wallet.utxos.keys():	
		my_wallet.utxos[t.recipient] = [t.outputs[1]]
	else:
		my_wallet.utxos[t.recipient].append(t.outputs[1])
	my_wallet.utxos[t.sender].append(t.outputs[0])
	#sender_wallet.utxos[t.recipient].append(t.outputs[1])
	my_wallet.transactions.append(t)
	
	# send back 'sender.wallet.utxos'	
	
	return True




class Node:

	# FIVOS
	# Only one node is running on each VM. Each node only has one wallet.

	def __init__(self, address, chain, current_block=None, node_id=0, NBC=0, ring=[]):
		##set

		self.chain = blockchain.Blockchain()
		self.id = node_id
		self.NBC = NBC		
		self.address = address # Address is a string
		self.wallet = self.create_wallet()
		self.ring = ring  #here we store information for every node, as its id, its address (ip:port) its public key and its balance 
		self.current_block = current_block
		self.block_ids = 1

	def set_id(self, myid):
		self.id = myid

	def create_genesis_block(self):
		genesis_block = block.Block(0, -1)
		genesis_block.current_hash = genesis_block.myHash() 
		

	def create_new_block(self, prevHash=0):
		myid = self.block_ids
		result = block.Block(myid, prevHash)
		self.block_ids += 1
		return(result)

	def create_wallet(self):
		#create a wallet for this node, with a public key and a private key
		return wallet.Wallet(self.address, []) # TODO Add constructor fields

	def register_node_to_ring(self, id, public_key):
		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs
		self.ring.append({id: public_key})



	def broadcast_transaction(self, my_transaction):
		print("In broadcast_transaction")
		print("SELF.RING: ##############")
		print(self.ring)
		my_transaction_pickle = jsonpickle.encode(my_transaction)
		my_wallet_pickle = jsonpickle.encode(self.wallet)
		for dictionary in self.ring:
			# Send the transaction to every ip in node.ring
			print("SENDING TO (FROM BROADCAST_TRANSACTION)")
			print(dictionary['ip'])
			url = "http://" + dictionary['ip'] + ":5000/incoming_transaction"
			print("BROADCASTING TRANSACTION TO: ")
			print(url)
			print("WALLET IN BROADCAST BEFORE POST")
			print(self.wallet.utxos)
			r = requests.post(url, data = {'transaction': my_transaction_pickle, 'wallet': my_wallet_pickle})
			print(r)


	def add_transaction_to_block(self, transaction):
		#if enough transactions  mine, then create new block
		print("current block in add_trans_to_block")
		print(self.current_block)
		capacity = self.current_block.capacity
		print(self.current_block.listOfTransactions)
		self.current_block.add_transaction(transaction)
		if(len(self.current_block.listOfTransactions) == capacity):
			print("Block is ready for mining")
			temp_current_block = self.current_block
			self.current_block = self.create_new_block()
			#self.mine_block(self.current_block)
			#self.current_block = self.create_new_block(self.current_block.id + 1, self.current_block.current_hash, self.current_block.capacity, self.current_block.difficulty)



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



