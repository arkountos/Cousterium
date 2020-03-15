from flask import Flask, jsonify, request, render_template

import block
import node
import wallet
import transaction

app = Flask(__name__)

# # If you hit that you are setting up yourself to be the bootstrap node
# @app.route('/setup/bootstrap', methods=['GET'])
# def setup_bootstrap_node():
#     # This node private IP Address
#     MY_ADDRESS = '192.168.0.2'

#     # Number of nodes in network
#     NETWORK_SIZE = 5

#     # Create the very first node
#     # The node constructor also creates the Wallet() we need and binds it to the node (I hope)
#     myNode = node.Node(0, MY_ADDRESS)
#     print(myNode)

#     # Create the genesis block with id = 0 and prev_hash = -1
#     genesis_block = block.Block(0, -1)

#     # Need to add the first and only transaction to the genesis block
#     first_transaction = transaction.Transaction(0, MY_ADDRESS, NETWORK_SIZE * 100)
#     genesis_block.add_transaction(first_transaction)

#     # Add the first block to the node's blockchain
#     myNode.chain.append(genesis_block)





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