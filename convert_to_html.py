with open('results_very_reduced.txt') as f:
    data = f.read()

split = data.split('-------')

t_string = 'https://zcash.blockexplorer.com/tx/'

with open('results_very_reduced.html', 'w') as f:
    f.write('<html><head><title>Reused Public keys on the Zcash blockchain</title></head><h2>Reused public keys on the Zcash blockchain</h2><h3>Killian Davitt</h3>')
    f.write('<p>This is a subset of the millions of public keys reused on the zcash blockchain. The full list of repeated public keys has a filesize of approx 2GB and cannot be converted into any usable html file. This file has 237 public keys and approx 500,000 transaction id\'s which use them. It is approx 32MB raw data and 90MB of html data.</p>\n')
    for s in split[1:]:
        f_split = s.split('.......')
        tx_s = f_split[1].split('\n')
        tx_s = [x for x in tx_s if len(x)>3]
        f.write('\n<div>\n')
        f.write('<strong>Public Key: ' + f_split[0] + ' (used ' + str(len(tx_s)) + ' times)</strong><br>')
        for tx in tx_s:
            f.write('<a href="' + t_string + tx.strip() + '">' + tx + '</a>\n<br>')
        f.write('\n</div>\n<br>')
