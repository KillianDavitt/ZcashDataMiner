
with open('asm_list.txt') as f:
    data = f.readlines()

public_keys = []
i=0
data = data[1:]
for script in data:
    asm_tx_split = script.split('|')
    print(len(asm_tx_split))
    tx_id = asm_tx_split[1]
    print(tx_id)
    script_split = asm_tx_split[0].split(' ')
    if len(script_split) != 2:
        print(len(script_split))
        print("Weird")
        continue
    pub_key = (script_split[1], tx_id)
    public_keys.append(pub_key)
    i+=1
    if i%10==0:
        with open('full_public_keys.txt', 'a') as f:
            for key in public_keys:
                f.write(str(key[0])+ ', ' + str(key[1]))

        public_keys = []
        

