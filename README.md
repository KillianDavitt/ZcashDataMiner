# ZcashDataMiner
Python script querying zcash-cli to retrieve zcash transaction info


## Install
```bash
git clone https://github.com/KillianDavitt/ZcashDataMiner.git
cd ZcashDataMiner
python3 -m virtualenv venv
venv/bin/pip3 install -r requirements.txt
./db_create.py
./db_migrate.py
./db_upgrade.py
```

### Scraping transactions
Before begining, the zcash node needs to be installed using the instructions here:. https://github.com/zcash/zcash/wiki/1.0-User-Guide

**Important**: Before running zcashd, ensure you add the following line to ~/.zcash/zcash.conf

```
txindex=1
```

This ensures that the database of transactions is properly queryable 

After you run zcashd, it will beging to download and confirm all of the transactions on the zcash blockchain. This may take some time.
It is not a good idea to run this data mining software until all of the transactions have been downloaded.


Once zcashd is ready you can run the data mining software

```bash
venv/bin/python3 main_with_sql.py
```

### Using pre-provided database
If you are using a premade database

Copy the sqlite3 database file to 

```
ZcashDataMiner/transactions.sqlite
```

### Viewing the transaction data

```
venv/bin/python3 run.py
```

Open a browser and visit http://127.0.0.1:5000
