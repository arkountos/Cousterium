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



class Wallet:

	def __init__(self, public_key=None, private_key=None, address, transactions):
		
		self.public_key = public_key
		self.private_key = private_key
		self.address = address
		self.transactions = transactions
		
	def generate_RSA():
		new_keypair = RSA.generate(2048)
		public_key = new_keypair.publickey().exportKey('PEM').decode()
		private_key = new_keypair.exportKey('PEM').decode()

	def balance():
		pass

