from flask import Flask, jsonify, request, render_template

import block
import node
import wallet
import transaction

import json

app = Flask(__name__)

# This node private IP Address
MY_ADDRESS = '127.0.0.1'

# Number of nodes in network
NETWORK_SIZE = 5

# IP addresses of all nodes in ring
ADDRESS_BOOK = [MY_ADDRESS]

def setup_bootstrap_node():
    # Create the very first node
    # The node constructor also creates the Wallet() we need and binds it to the node (I hope)
    myNode = node.Node(0, MY_ADDRESS)
    print(myNode)

    # Create the genesis block with id = 0 and prev_hash = -1
    genesis_block = block.Block(0, -1, []) # TODO: we shouldn't have to pass emtpy list as listOfTransactions in constructor, see with peppas

    # Need to add the first and only transaction to the genesis block
    first_transaction = transaction.Transaction(0, MY_ADDRESS, NETWORK_SIZE * 100)
    genesis_block.add_transaction(first_transaction)

    # Add the first block to the node's blockchain
    myNode.chain.append(genesis_block)

@app.route('/test')
def test():
    print('Address: ' + json.dumps(MY_ADDRESS))
    return('Address: ' + json.dumps(MY_ADDRESS))




if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    setup_bootstrap_node()

    app.run(host=MY_ADDRESS, port=port) # TODO: This will change depending on the VM we run it