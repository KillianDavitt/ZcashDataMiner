import psutil
import os
import json
import subprocess
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

b = get_block("0") # initial block

for i in range(3000):
    b = get_next_block(b)
    if len(b['tx']) > 1:
        print(b['tx'])
