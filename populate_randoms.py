from app import db
from app.models import Signature
import sqlite3
conn = sqlite3.connect('transactions.sqlite')

c = conn.cursor()
n = None
with open('progress.txt') as f:
    n = int(f.read())


# For every vin script
for i in range(100000):
    c.execute('SELECT * FROM "vin_script" WHERE script_id=' + str(n) + ';')
    scr = c.fetchone()

    # Split the script by space
    s_r = scr[2].split(' ')[0]
    #print(s_r)
    structure_value = s_r[0:2] 
    total_length = s_r[2:4] 
    r_integer=s_r[4:6]
    r_length = int(s_r[6:8],16) * 2
    print("R length is: " + str(r_length))
    r = s_r[8:8+r_length]
    print("R is: " + str(r))
    sig = Signature(r=r, tx_id=scr[6])
    db.session.add(sig)
    n = n+1

    ## Save progress once in a while
    if n%1000 == 0:
        db.session.commit()
        print(n)
        with open('progress.txt', 'w') as f:
            f.write(str(n))
