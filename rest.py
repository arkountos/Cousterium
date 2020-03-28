from flask import Flask, jsonify, request, render_template

import jsonpickle
import block
import node
import wallet
import transaction
import socket
import json
import requests
import netifaces
from ip import get_my_ip

# Setup the bootstrap node
def setup_bootstrap_node():
    # Create the very first node
    # The node constructor also creates the Wallet() we need and binds it to the node (I hope)
    myNode = node.Node(0, MY_ADDRESS)
    myNode.ring.append({'ip': get_my_ip(), 'id': 1, 'public_key': myNode.wallet.get_public_key()})
    
    # Create the genesis block with id = 0 and prev_hash = -1
    genesis_block = block.Block(0, -1, [], []) # TODO: we shouldn't have to pass emtpy list as listOfTransactions in constructor, see with peppas

    # Need to add the first and only transaction to the genesis block
    #print("The bootstrap node's wallet private key is ")
    #print(myNode.wallet.get_private_key())
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

    r = requests.get("http://" + SERVER_ADDRESS + ":5000/get_bootstrap_utxo")
    print(r.text)
    my_utxos = jsonpickle.decode(r.text)
    print(type(my_utxos))
    
    print("BEFORE:")
    print(myNode.wallet.utxos)

    for key in my_utxos.keys():
        if key not in myNode.wallet.utxos.keys():
            myNode.wallet.utxos[key] = my_utxos[key]
            #myNode.wallet.utxos = my_utxos.copy()
    
    print("AFTER")
    print(myNode.wallet.utxos)
 
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
    



# A function to broadcast the ring information to all the nodes,
# when every node joins the system.
# This is only run from the bootstrap node
def broadcast_info():
    print("RING: ")
    print(MY_NODE.ring)
    #print("BROADCASTING TO: " +  "http://" + data_line['ip'] + ":5000/test")
    ring_pickle = jsonpickle.encode(MY_NODE.ring)
    for entry in MY_NODE.ring:
        print("TO: ", "http://" + entry['ip'] + ":5000/add_to_client_ring")
        # TODO: ** Maybe we have to jsonpickle? **
        r = requests.post("http://" + entry['ip'] + ":5000/add_to_client_ring", data={'ring':ring_pickle})
        




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
    
    incoming_ring = request.form.to_dict()['ring']
    new_ring = jsonpickle.decode(incoming_ring)
    
    MY_NODE.ring = new_ring
    print("Node with id ")
    print(MY_NODE.id)
    print(" has new ring: ")
    print(MY_NODE.ring)
    #MY_NODE.wallet.utxos[request.form.to_dict()['public_key']] = []
    print("The node's utxos")
    print(MY_NODE.wallet.utxos)
    return("OK!")



@app.route('/setup_myself', methods=['GET'])
def setup_myself():
	setup()
	return("Node setup with id " + MY_NODE.id)

@app.route('/get_bootstrap_utxo', methods=['GET'])
def get_bootstrap_utxo():
    my_utxo = jsonpickle.encode(MY_NODE.wallet.utxos)
    return(my_utxo)


@app.route('/incoming_transaction', methods=['POST'])
def incoming_transaction():
    
    pickle_transaction = request.form.to_dict()['transaction']
    pickle_wallet = request.form.to_dict()['wallet']
    my_transaction = jsonpickle.decode(pickle_transaction)
    incoming_wallet = jsonpickle.decode(pickle_wallet)
    print("WALLET BEFORE")
    print("WHO AM I???")
    print(get_my_ip())
    print(MY_NODE.wallet.utxos)
    if (node.validate_transaction(incoming_wallet, my_transaction, MY_NODE.wallet)):
        #If here we broadcast utxo to everyone
        # Update the sender utxos
        pass
    print("WALLET AFTER")
    print(MY_NODE.wallet.utxos)
    return("OK")


@app.route('/send_money', methods=['POST'])
def send_money():
    print("In send_money()")
    # Create the transaction
    # This runs on the node that sends the money
    
    #TODO: in create_transaction, what is 'recipient'? Is it the object or the public key
    # I use object here..
    for dictionary in MY_NODE.ring:
        print(dictionary['ip'])
        print(request.form.to_dict()['ip'])
        if dictionary['ip'] == request.form.to_dict()['ip']:
            pk = dictionary['public_key']
            print(dictionary)    

 
    my_transaction = transaction.create_transaction(MY_NODE.wallet, pk, int(request.form.to_dict()['amount']))
    MY_NODE.broadcast_transaction(my_transaction)



# Add the calling node to the ring
@app.route('/add_to_ring', methods=['POST'])
def add_to_ring():
    next_id = NODE_IDS.pop() 
    MY_NODE.ring.append({'id': next_id, 'ip':request.remote_addr, 'public_key':request.form.to_dict()['public_key']})
    
    ### GIVE HIM 100 NBC ###
    print("Bootstrap WALLET BEFORE CREATE FIRST TRANSACTION: ")
    print(MY_NODE.wallet.utxos)
    first_transaction = transaction.create_transaction(MY_NODE.wallet, request.form.to_dict()['public_key'], 100)
    
    print("Bootstrap WALLET AFTER FIRST TRANSACTION: ")
    print(MY_NODE.wallet.utxos)
    print("Pickle'ing the first_transaction object")
    transaction_pickle = jsonpickle.encode(first_transaction)
    print(transaction_pickle)

    print("Pickle'ing the wallet")
    wallet_pickle = jsonpickle.encode(MY_NODE.wallet)


    # remote_addr is getting the same transaction twice!(?)
    print("Sending transaction to: ")
    print("http://" + request.remote_addr + ":5000/incoming_transaction")
    #r = requests.post("http://" + request.remote_addr + ":5000/incoming_transaction", data={'transaction': transaction_pickle, 'wallet': wallet_pickle})
    #print("Returned with answer: ")
    #print(r)
    #print(r.text)
    MY_NODE.broadcast_transaction(first_transaction)
    if next_id == NETWORK_SIZE:
        broadcast_info()
        print("Broadcast successful!")
    
    return ("Node added to ring succesfully!")



@app.route('/get_balance', methods=['GET'])
def get_balance():
    result = MY_NODE.wallet.calculate_balance()
    print(result)
    print(type(result))
    return(result)



@app.route('/get_balance', methods=['GET'])
def get_balance():
    result = MY_NODE.wallet.calculate_balance()
    print(result)
    print(type(result))
    return(result)



@app.route('/test', methods=['GET'])
def test():
    print('Address: ' + json.dumps(MY_ADDRESS))
    return('Address: ' + json.dumps(MY_ADDRESS))



if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port
    print("Serving at: ", MY_ADDRESS)
    app.run(host=MY_ADDRESS, port=port)

