#from collections import OrderedDict
import collections
import wallet
import node
import binascii
import datetime
import Crypto
import Crypto.Random
from Crypto.Hash import SHA384
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import json
#from hashlib import sha256
import random
import requests
from flask import Flask, jsonify, request, render_template


class Transaction:

    def __init__(self, sender, recipient, amount, inputs, signature=None, index=None):
        ##set

        self.sender = sender
        self.recipient = recipient
        self.amount = amount    
        self.index = index
        self.inputs = inputs 
        #self.transaction_outputs: λίστα από Transaction Output 
        self.signature = signature
        self.outputs = []

    # structure to use all infos as message in signature
    def to_dict(self):
        return collections.OrderedDict({
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'index': self.index})

    def sign_trans(self):
        myhash = SHA384.new(json.dumps(self.to_dict()).encode()).hexdigest()
        p_key = RSA.importKey(sender.wallet.get_private_key())
        signer = PKCS1_v1_5.new(p_key)
        self.index = myhash
        h = SHA384.new(json.dumps(self.to_dict()).encode()).hexdigest()
        self.signature = binascii.hexlify(signer.sign(h)).decode()

    def genesis_transaction(self, mywallet, participants):

        t = Transaction(
            sender = mywallet.get_private_key(), 
            recipient = mywallet.get_private_key(),
            amount = 100*participants,
            inputs = [])
        
        t.sign_trans()
        t.outputs = [{
            'id': t.index,
            'who': t.sender,
            'amount': t.amount
        }]

        wallet.utxos[wallet.get_public_key()] = t.outputs[0]
        
