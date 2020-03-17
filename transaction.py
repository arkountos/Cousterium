#from collections import OrderedDict
import collections
import wallet
import binascii
import datetime
import Crypto
import Crypto.Random
from Crypto.Hash import SHA384
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

#from hashlib import sha256
import random
import requests
from flask import Flask, jsonify, request, render_template


class Transaction:

    def __init__(self, sender_address, sender_private_key, recipient_address, value, transaction_inputs):
        ##set

        self.sender = sender_address
        self.private_key = sender_private_key
        self.recipient = recipient_address
        self.amount = value    
        self.time = datetime.datetime.utcnow()
        self.index = SHA384.new(str(self.time).encode()).hexdigest()
        self.transaction_inputs = transaction_inputs 
        #self.transaction_outputs: λίστα από Transaction Output 
        self.signature = None

    # structure to use all infos as message in signature
    def to_dict(self):
        return collections.OrderedDict({
            'sender': self.sender,
            'recipient': self.recipient,
            'value': self.amount,
            'time' : self.time})

    def signature(self):
        private_key = self.private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA384.new(str(self.to_dict()).encode())
        self.signature = binascii.hexlify(signer.sign(h)).decode()


mywallet = wallet.Wallet(1,[])
mywallet.generate_RSA()
test = Transaction(0,'placeholder',3,10,[])
