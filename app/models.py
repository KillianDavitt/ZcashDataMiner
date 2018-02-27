from app import db


class Transaction(db.Model):
    tx_id = db.Column(db.String(64), primary_key=True)
    vins = db.relationship('Vin', backref='transaction', lazy=True)
    vouts = db.relationship('Vout', backref='transaction', lazy=True)
    vjoinsplits = db.relationship('VJoinSplit', backref='transaction', lazy=True)


class Vin(db.Model):
    vin_id = db.Column(db.Integer, primary_key=True)
    coinbase = db.Column(db.Integer)
    sequence = db.Column(db.Integer)
    scripts = db.relationship('VinScript', backref='vin', lazy=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.tx_id'), nullable=False)

    
class Vout(db.Model):
    vout_id = db.Column(db.Integer, primary_key=True)
    n = db.Column(db.Integer)
    value = db.Column(db.Float)
    value_zat = db.Column(db.Integer)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.tx_id'), nullable=False)
    scripts = db.relationship('Script', backref='vout', lazy=True)


class Script(db.Model):
    script_id = db.Column(db.Integer, primary_key=True)
    addresses = db.relationship('Address', backref='script', lazy=True)
    vout_id = db.Column(db.Integer, db.ForeignKey('vout.vout_id'), nullable=False)
    asm = db.Column(db.String())
    hex_script = db.Column(db.String())
    req_sigs = db.Column(db.Integer)
    type_script = db.Column(db.String)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.tx_id'), nullable=False)

class VinScript(db.Model):
    script_id = db.Column(db.Integer, primary_key=True)
    vin_id = db.Column(db.Integer, db.ForeignKey('vin.vin_id'), nullable=False)
    asm = db.Column(db.String())
    hex_script = db.Column(db.String())
    req_sigs = db.Column(db.Integer)
    type_script = db.Column(db.String)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.tx_id'), nullable=False)

class VJoinSplit(db.Model):
    vjoinsplit_id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer,
                               db.ForeignKey('transaction.tx_id'),
                               nullable=False)
    vpub_old = db.Column(db.String(), nullable=False)
    vpub_new = db.Column(db.String(), nullable=False)
    anchor = db.Column(db.String(), nullable=False)
    nullifiers = db.relationship('Nullifier', backref='vjoin2split', lazy=True)
    commitments = db.relationship('Commitment', backref='vjoinsplit', lazy=True)
    onetime_pub_key = db.Column(db.String(), nullable=False)
    random_seed = db.Column(db.String(), nullable=False)
    macs = db.relationship('Mac', backref='vjoinsplit', lazy=True)
    proof = db.Column(db.String(140), nullable=False)


class Nullifier(db.Model):
    nullifier_id = db.Column(db.Integer, primary_key=True)
    null = db.Column(db.String())
    js_id = db.Column(db.Integer, db.ForeignKey('v_join_split.vjoinsplit_id'), nullable=False)
    
class Mac(db.Model):
    mac_id = db.Column(db.Integer, primary_key=True)
    ma = db.Column(db.String())
    js_id = db.Column(db.Integer, db.ForeignKey('v_join_split.vjoinsplit_id'), nullable=False)

class Commitment(db.Model):
    commitment_id = db.Column(db.Integer, primary_key=True)
    commit = db.Column(db.String())
    js_id = db.Column(db.Integer,
                      db.ForeignKey('v_join_split.vjoinsplit_id'),
                      nullable=False)
    
    
class Address(db.Model):
    add = db.Column(db.String(38), primary_key=True)
    script_id = db.Column(db.Integer, db.ForeignKey('script.script_id'), nullable=False)

    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.tx_id'), nullable=False)

class Signature(db.Model):
    sig_id = db.Column(db.Integer, primary_key=True)
    r = db.Column(db.String(80))
    s = db.Column(db.String(80))
    tx_id = db.Column(db.String())
