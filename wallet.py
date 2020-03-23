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

		utxos[self.public_key] = []

		self.address = address
		self.transactions = transactions
		self.balance = self.calculate_balance()

	def generate_RSA(self):
		new_keypair = RSA.generate(2048)
		public_key = new_keypair.publickey().exportKey('PEM').decode()
		private_key = new_keypair.exportKey('PEM').decode()
		# print([public_key, private_key])
		return [public_key, private_key]

	def calculate_balance(self):
		print("In balance")
		print("NEAT UTXO")
		print(utxos)
		print("utxos[self.public_key], where self.public_key is:")
		print(self.public_key + "\n")
		print(utxos[self.public_key])
		# myutxo is a list []
		

	def get_private_key(self):
		return self.private_key

	def get_public_key(self):
		return self.public_key

	

