from flask import Flask, jsonify, request, render_template

import block
import node
import wallet
import transaction
import socket
import json
import requests

# Setup the bootstrap node
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

    # Return the node
    return (myNode)

# Setup a regular participant node
def setup_regular_node():
    # Create node and associate with VM via address
    myNode = node.Node(0, MY_ADDRESS)
    print(myNode)

    # Our node sends it's publik key (= wallet address = MY_ADDRESS ? )
    # and receives a unique id (0..NETWORK_SIZE) 
    print('http://' + SERVER_ADDRESS + ':5000/add_to_ring')
    r = requests.post('http://' + SERVER_ADDRESS + ':5000/add_to_ring', data = {'public_key':MY_ADDRESS})
    print(r)
    print(r.text)

# A function to get the VM's private IP (e.g. 192.168.0.4)
def get_my_ip():
    """
    Find my IP address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

app = Flask(__name__)

#### IF BOOTSTRAP NODE ####
if (get_my_ip() == '192.168.0.2'):
    MY_ADDRESS = '192.168.0.2'
    # Number of nodes in network
    NETWORK_SIZE = 5
    #IDs
    NODE_IDS = [4, 3, 2, 1]
    # IP addresses of all nodes in ring
    ADDRESS_BOOK = [MY_ADDRESS]
    MY_NODE = setup_bootstrap_node()
#### IF REGULAR NODE ####
else:
    MY_ADDRESS = get_my_ip()
    # Bootstrap node address (we suppose it is known to everyone)
    SERVER_ADDRESS = '192.168.0.2'
    MY_NODE = setup_regular_node()


# Add the calling node to the ring
# 1) Add the node to the ring
# 2) Send back an id
@app.route('/add_to_ring', methods=['POST'])
def add_to_ring():
    next_id = NODE_IDS.pop()
    print("Got it")
    print(request.form.to_dict())
    # 1)
    MY_NODE.chain.append()
    # 2)
    return (next_id)

@app.route('/test')
def test():
    print('Address: ' + json.dumps(MY_ADDRESS))
    return('Address: ' + json.dumps(MY_ADDRESS))

# get all transactions in the blockchain

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    transactions = blockchain.transactions

    response = {'transactions': transactions}
    return jsonify(response), 200


# run it once fore every node

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port)