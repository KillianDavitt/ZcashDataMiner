import psutil
import os
import json
import subprocess
from app import db
from app.models import Transaction
from tinydb import TinyDB, Query

db = TinyDB('db.json')
Transaction = Query()

procs = {p.pid: p.info for p in psutil.process_iter(attrs=['name', 'username'])}
if not 'zcashd' in [p['name'] for p in procs.values()]:
    print("Zcash daemon must be running.....")
    exit(1)





def zcli(cmd):
    process = subprocess.Popen(("zcash-cli " + cmd).split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output

# Gets the block from hash or height
def get_block(block_index):
    raw_block = zcli("getblock " + block_index)
    return(json.loads((raw_block).decode()))

def get_next_block(curr_block):
    next_block_hash = curr_block['nextblockhash']
    next_block = get_block(next_block_hash)
    return next_block


def get_raw_tx(tx_id):
    raw_tx = zcli("getrawtransaction " + tx_id)
    return raw_tx


def decode_raw_tx(tx_blob):
    raw_tx = zcli("decoderawtransaction " + tx_blob.decode())
    return json.loads((raw_tx).decode())


b = get_block("0") # initial block

for i in range(30):
    b = get_next_block(b)
    tx_id = b['tx']
    tx = get_raw_tx(tx_id[0])
    tx = decode_raw_tx(tx)
    db.insert(tx)
    
    
