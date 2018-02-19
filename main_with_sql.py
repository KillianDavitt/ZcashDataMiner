import psutil
import os
import json
import subprocess

from app import db
from app.models import Transaction, Vin, Vout, VJoinSplit, Script, Nullifier, Commitment, Mac

procs = {p.pid: p.info for p in psutil.process_iter(attrs=['name', 'username'])}
if not 'zcashd' in [p['name'] for p in procs.values()]:
    print("Zcash daemon must be running.....")
    exit(1)


'''
The flow of the data mining starts at block 0 and gets all the
transactions then gets the next block, gets all the transactions and
so on. So, we can save to disk the number of the current block we are
on and resume in the correct place each time
'''



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


def main():
    with open('current_block.txt') as f:
        curr_block = f.read()

    if len(curr_block)<1:
        curr_block = 0
    else:
        curr_block = str(int(curr_block))
    b = get_block(curr_block) # initial block

    for i in range(30000):
        b = get_next_block(b)
        curr_block = str(int(curr_block) +  1)
        txs = b['tx']
        print("Another block: " + str(len(txs)) + " transactions")
        for tx_id in txs:
            tx = get_raw_tx(tx_id)
            tx = decode_raw_tx(tx)
            t = Transaction(tx_id=tx_id)
            vins = []
            vouts = []
            vjoinsplits = []
            for out in tx['vout']:
                
                o = Vout(transaction_id=tx_id)
                t.vouts.append(o)
                db.session.add(o)
                scr = out['scriptPubKey']
                s = Script(vout_id=o.vout_id,
                           transaction_id=tx_id)
                s.asm = scr['asm']
                s.hex_script = scr['hex']
                o.scripts.append(s)
                s.vout = o
                db.session.add(s)

            for vin in tx['vin']:
                v = Vin(transaction_id=tx_id)
                t.vins.append(v)
                db.session.add(v)
            for jsplit in tx['vjoinsplit']:
                joinsplit = VJoinSplit()
                joinsplit.vpub_old = jsplit['vpub_old']
                joinsplit.vpub_new = jsplit['vpub_new']
                joinsplit.anchor = jsplit['anchor']
                joinsplit.onetime_pub_key = jsplit['onetimePubKey']
                joinsplit.random_seed = jsplit['randomSeed']
                joinsplit.proof = jsplit['proof']
                t.vjoinsplits.append(joinsplit)

                for null in jsplit['nullifiers']:
                    n = Nullifier(null=null, js_id=joinsplit.vjoinsplit_id)
                    joinsplit.nullifiers.append(n)
                    db.session.add(n)
                    
                for comm in jsplit['commitments']:
                    c = Commitment(commit=comm, js_id=joinsplit.vjoinsplit_id)
                    joinsplit.commitments.append(c)
                    db.session.add(c)

                for mac in jsplit['macs']:
                    m = Mac(ma=mac, js_id=joinsplit.vjoinsplit_id)
                    joinsplit.macs.append(m)
                    db.session.add(m)
                
                vjoinsplits.append(joinsplit)
                db.session.add(joinsplit)
                
            db.session.add(t)

            db.session.commit()
        if int(curr_block) % 50 ==0:
            print("FINISHED 50 BLOCKS, saving block progress")
            with open('current_block.txt', 'w') as f:
                f.write(curr_block)


if __name__ == '__main__':
    main()
