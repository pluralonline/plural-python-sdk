import requests
import json
import base64

class EMI:

    def __init__(self, pinelabs):
        self.mid = pinelabs.mid
        self.key = pinelabs.key
        self.secret = pinelabs.secret
        self.endpoint = pinelabs.endpoint

    def calculate(self, txn_data, products_details):
        # Calculate EMI for the given payload | body
        try:
            # Endpoint
            endpoint = self.endpoint + 'v2/emi/calculator'

            # Headers
            headers = {
                "Content-Type": "application/json",  # Adjust the content type as needed
            }

            payload = {
                "merchant_data": {
                    "merchant_id": self.mid,
                    "merchant_access_code": self.key,
                },
                "payment_data": {
                    "amount_in_paisa": txn_data.get("amount_in_paisa"),
                },
                "product_details" : products_details
            }

            response = requests.post(endpoint, headers=headers, json=payload)
            response = response.json()

            if response.get("respone_code")  :
                if int(response.get("respone_code")) != 1 :
                    raise Exception(str(response.get("respone_message")))
                
            if  response.get("response_code") :
                if  int(response.get("response_code")) != 1:
                    raise Exception(str(response.get("response_message")))

            return response
        except Exception as e:
            raise Exception(str(e))