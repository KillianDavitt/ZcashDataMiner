
with open('sorted_pub_keys_and_tx.txt') as f:
    lines = f.readlines()

reuse = {}
i=0
current_pub = lines[0].split(',')[0]
reuse[current_pub] = []
for i in range(int(len(lines))):
    split = lines[i].split(',')
    pub = split[0]
    tx = split[1]
    if pub == current_pub:
        reuse[current_pub].append(tx)
    else:
        current_pub = pub
        reuse[current_pub] = []
    
    i+=1



with open('results.txt', 'a') as f:
    for key in sorted(reuse.keys(), key=lambda k: len(reuse[k]), reverse=True):
        val = list(set(reuse[key]))
        if len(val)<2:
            continue
        f.write('-------\n')
        f.write(key)
        f.write('.......\n')
        for v in val:
            f.write(v)


