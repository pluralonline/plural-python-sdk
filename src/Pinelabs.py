from .Payment import Payment
from .EMI import EMI
from .Hash import Hash

class Pinelabs:

    def __init__(self, merchant_id, access_code, secret, is_test=False):
        self.mid = merchant_id
        self.key = access_code
        self.secret = secret
        self.endpoint = 'https://uat.pinepg.in/api/' if is_test else 'https://pinepg.in/api/'
        self.hash = Hash(self)
        self.emi = EMI(self)
        self.payment = Payment(self)