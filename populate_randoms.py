from app import db
from app.models import Signature
import sqlite3
conn = sqlite3.connect('transactions.sqlite')

c = conn.cursor()
n = None
with open('progress.txt') as f:
    n = int(f.read())


# For every vin script
for i in range(5000000):
    c.execute('SELECT * FROM "vin_script" WHERE script_id=' + str(n) + ';')
    scr = c.fetchone()

    # Split the script by space
    s_r = scr[2].split(' ')[0]
    s = s_r[0:int(len(s_r)/2)]
    r = s_r[int(len(s_r)/2):]
    sig = Signature(r=r, s=s, tx_id=scr[6])
    db.session.add(sig)
    n = n+1

    ## Save progress once in a while
    if n%1000 == 0:
        db.session.commit()
        print(n)
        with open('progress.txt', 'w') as f:
            f.write(str(n))
