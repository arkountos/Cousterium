from flask import Flask, jsonify, request, render_template

import block
import node
import wallet
import transaction
import socket
import json
import requests
import netifaces

# Setup the bootstrap node
def setup_bootstrap_node():
    # Create the very first node
    # The node constructor also creates the Wallet() we need and binds it to the node (I hope)
    myNode = node.Node(0, MY_ADDRESS)
    print(myNode)

    # Create the genesis block with id = 0 and prev_hash = -1
    genesis_block = block.Block(0, -1, [], []) # TODO: we shouldn't have to pass emtpy list as listOfTransactions in constructor, see with peppas

    # Need to add the first and only transaction to the genesis block
    print("The bootstrap node's wallet private key is ")
    print(myNode.wallet.get_private_key())
    first_transaction = transaction.genesis_transaction(myNode.wallet, NETWORK_SIZE)    
    #first_transaction = transaction.Transaction( sender=0, recipient=MY_ADDRESS, amount=NETWORK_SIZE * 100, inputs=[])
    # TODO: Use transaction.genesis_transaction
    genesis_block.add_transaction(first_transaction)

    # Add the first block to the node's blockchain
    myNode.chain.append(genesis_block)
    print("Bootstrap node has: ")
    print(myNode.wallet.calculate_balance())
    # Return the node
    return (myNode)

# Setup a regular participant node
def create_regular_node():
    # Create node and associate with VM via address
    myNode = node.Node(0, MY_ADDRESS)

    print("I RETURN: ")
    print((myNode is None))
    return(myNode)
    
def setup():
    # Our node sends it's publik key (= wallet address = MY_ADDRESS ? )
    # and receives a unique id (0..NETWORK_SIZE) 
    print('http://' + SERVER_ADDRESS + ':5000/add_to_ring')
    r = requests.post('http://' + SERVER_ADDRESS + ':5000/add_to_ring', data = {'public_key':MY_NODE.wallet.get_public_key()})
    print("The answer from the server is: \nr: ")
    print(r)
    print("\nr.text ")
    print(r.text)
    # Set node id to the id you got on the response
    MY_NODE.set_id(r.text)
    #print("MY_NODE IS: ", myNode)

    ### GIVE ME 100 NBC ###
    

# A function to get the VM's private IP (e.g. 192.168.0.4)
def get_my_ip():
    """
    Find my private IP address
    :return:
    """
    iface = netifaces.ifaddresses('eth1').get(netifaces.AF_INET)
    result = iface[0]["addr"]
    print(result)
    return(result)

# A function to broadcast the ring information to all the nodes,
# when every node joins the system.
# This is only run from the bootstrap node
def broadcast_info():
    print("RING: ")
    print(MY_NODE.ring)
    #print("BROADCASTING TO: " +  "http://" + data_line['ip'] + ":5000/test")
    for entry in MY_NODE.ring:
        print("TO: ", "http://" + entry['ip'] + ":5000/add_to_client_ring")
        r = requests.post("http://" + entry['ip'] + ":5000/add_to_client_ring", data=MY_NODE.ring)
        




app = Flask(__name__)

# run it once fore every node

#### IF BOOTSTRAP NODE ####
if (get_my_ip() == '192.168.0.2'):
    print("I'm gonna be the bootstrap!!!")
    MY_ADDRESS = get_my_ip()
    # Number of nodes in network
    NETWORK_SIZE = 5
    #IDs
    NODE_IDS = [5, 4, 3, 2]
    # IP addresses of all nodes in ring
    MY_NODE = setup_bootstrap_node()
    #ADDRESS_BOOK = [{MY_ADDRESS:MY_NODE.wallet.get_public_key()}]
#### IF REGULAR NODE ####
else:
    print("I'm gonna be a client :(")
    MY_ADDRESS = get_my_ip()
    # Bootstrap node address (we suppose it is known to everyone)
    SERVER_ADDRESS = '192.168.0.2'
    MY_NODE = create_regular_node()
    
    #print("We are OK, MY_NODE is " + MY_NODE is None)

@app.route('/add_to_client_ring', methods=['POST', 'GET'])
def add_to_client_ring():
    print("This has to be a dict")
    print(request.form.to_dict())
    MY_NODE.ring.append(request.form.to_dict())
    print("Node with id ")
    print(MY_NODE.id)
    print(" has ring: ")
    print(MY_NODE.ring)
    MY_NODE.wallet.utxos[request.form.to_dict()['public_key']] = []
    print("The node's utxos")
    print(MY_NODE.wallet.utxos)
    return("OK!")

@app.route('/setup_myself', methods=['GET'])
def setup_myself():
	setup()
	return("Node setup with id " + MY_NODE.id)

@app.route('/incoming_transaction')
def incoming_transaction():
    if (node.validate_transaction(request.form.to_dict()['wallet'], request.form.to_dict()['transaction'])):
        pass



# Add the calling node to the ring
@app.route('/add_to_ring', methods=['POST'])
def add_to_ring():
    next_id = NODE_IDS.pop() 
    MY_NODE.ring.append({'id': next_id, 'ip':request.remote_addr, 'public_key':request.form.to_dict()['public_key']})
    
    ### GIVE HIM 100 NBC ###

    first_transaction = transaction.create_transaction(MY_NODE.wallet, request.form.to_dict()['public_key'], 100)
    print("Sending transaction to: ")
    print("http://" + request.remote_addr + ":5000/incoming_transaction")
    r = requests.post("http://" + request.remote_addr + ":5000/incoming_transaction", data={'transaction': first_transaction, 'wallet': MY_NODE.wallet})
    print("Returned with answer: ")
    print(r)
    print(r.text)
    #request.form , request.text
    #requests.get, requests.post


    if next_id == NETWORK_SIZE:
        broadcast_info()
        print("Broadcast successful!")
    
    return ("Node added to ring succesfully!")

@app.route('/test', methods=['GET'])
def test():
    print('Address: ' + json.dumps(MY_ADDRESS))
    return('Address: ' + json.dumps(MY_ADDRESS))

# get all transactions in the blockchain

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    transactions = blockchain.transactions

    response = {'transactions': transactions}
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    print("Serving at: ", MY_ADDRESS)
    app.run(host=MY_ADDRESS, port=port)

