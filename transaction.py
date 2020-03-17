from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from hashlib import sha256
import random
import requests
from flask import Flask, jsonify, request, render_template


class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value, transaction_inputs, index=0):

        ##set

        #self.sender_address: To public key του wallet από το οποίο προέρχονται τα χρήματα
        self.sender_address = sender_address

        #self.receiver_address: To public key του wallet στο οποίο θα καταλήξουν τα χρήματα
        self.recipient_address = recipient_address

        #self.amount: το ποσό που θα μεταφερθεί
        self.amount = value
        
        # the index of transaction is a hash value 
        self._index = index
        
        self.transaction_inputs = transaction_inputs 

        #self.transaction_outputs: λίστα από Transaction Output 
        
        #selfSignature


    def to_dict(self):
        pass

    # Getter and setter functions to init id of transaction without passing a specific value
    @property
    def index(self):
        return self._index

    @index.setter
    def index(self):
        rand = random.randint(1,1000000)
        self._index = sha256.new(rand).hexdigest()


    def sign_transaction(self):
        """
        Sign transaction with private key
        """
        pass
       