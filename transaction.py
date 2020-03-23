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


def genesis_transaction(mywallet, participants):

    t = Transaction(
        sender = 0,
        sender_private_key = mywallet.get_private_key(), 
        recipient = mywallet.get_public_key(),
        amount = 100*participants,
        inputs = [])
    
    t.sign_trans()
    t.outputs = [{
        'id': t.index,
        'who': t.sender,
        'amount': t.amount
    }]

    wallet.utxos[mywallet.get_public_key()] = t.outputs[0]
    print("WHAT MOEY DO I HAVE???")
    print(wallet.utxos[mywallet.get_public_key()])
    mywallet.transactions.append(t)

    return True


# possible use of copy for dicitonaries  
def create_transaction(mywallet, recipient, amount):
    
    inputs = wallet.utxos[mywallet.get_public_key()].copy()
    balance = mywallet.balance
    if balance < amount:
        raise Exception('not enough money')

    t = Transaction(
        sender = mywallet.get_public_key(),
	sender_private_key = mywallet.get_private_key(),
        recipient = recipient,
        amount = amount,
        inputs = inputs
    )
    t.sign()
    t.outputs = [{
        'id': t.index,
        'who': t.sender,
        'amount': balance - amount
    },{
        'id': t.index,
        'who': t.recipient,
        'amount': amount           
    }]

    wallet.utxos[mywallet.sender] = t.outputs[0]
    wallet.utxos[recipient].append(t.outputs[1])

    wallet.mywallet.transactions.append(t) 

    return t

class Transaction:

    def __init__(self, sender, sender_private_key, recipient, amount, inputs, signature=None, index=None):
        ##set

        self.sender = sender
        self.sender_private_key = sender_private_key
        self.recipient = recipient
        self.amount = amount    
        self.index = index
        self.inputs = inputs  
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
        p_key = RSA.importKey(self.sender_private_key)
        signer = PKCS1_v1_5.new(p_key)
        self.index = myhash
        h = SHA384.new(json.dumps(self.to_dict()).encode()).hexdigest()
        # TODO: Fix!
        #self.signature = binascii.hexlify(signer.sign(h)).decode()





