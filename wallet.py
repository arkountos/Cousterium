import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4

utxos = {}

class Wallet:

	def __init__(self, address, transactions, public_key=None, private_key=None):
		
		keys = self.generate_RSA()
		self.public_key = keys[0]
		self.private_key = keys[1]
		self.address = address
		self.transactions = transactions
		self.balance = self.balance()
		self.UTXOs = UTXOs
		
	def generate_RSA(self):
		new_keypair = RSA.generate(2048)
		public_key = new_keypair.publickey().exportKey('PEM').decode()
		private_key = new_keypair.exportKey('PEM').decode()
		# print([public_key, private_key])
		return [public_key, private_key]

	def balance(self, UTXOS):
    	# just a prototype. UTXOS is the list of all uspent transactions
		balance = 0 
		for i in UTXOS:
			balance += i 
		return balance

	def get_private_key(self):
		return self.private_key

	def get_public_key(self):
		return self.public_key

	

