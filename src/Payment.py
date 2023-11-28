import requests
import json
import base64

class Payment:

    def __init__(self, pinelabs):
        self.mid = pinelabs.mid
        self.key = pinelabs.key
        self.endpoint = pinelabs.endpoint
        self.hash = pinelabs.hash
    
    def create(self, txn_data, customer_data, billing_data, shipping_data, udf_data, payment_mode, products_details):
        # Create order at pinelabs for the given payload | body
        try:
            
            # Endpoint
            endpoint = self.endpoint + 'v2/accept/payment'

            parsed_payment_mode = []

            if payment_mode.get("cards") :
                parsed_payment_mode.append(1)
            if payment_mode.get("netbanking") :
                parsed_payment_mode.append(3)
            if payment_mode.get("emi") :
                parsed_payment_mode.append(4)
            if payment_mode.get("upi") :
                parsed_payment_mode.append(10)
            if payment_mode.get("wallet") :
                parsed_payment_mode.append(11)
            if payment_mode.get("debit_emi") :
                parsed_payment_mode.append(14)
            if payment_mode.get("prebooking") :
                parsed_payment_mode.append(16)
            if payment_mode.get("bnpl") :
                parsed_payment_mode.append(17)
            if payment_mode.get("cardless_emi") :
                parsed_payment_mode.append(19)

            payment_mode = ','.join(map(str, parsed_payment_mode))

            # Payload
            payload = {
                "merchant_data": {
                    "merchant_id": self.mid,
                    "merchant_access_code": self.key,
                    "merchant_return_url": txn_data.get("callback"),
                    "unique_merchant_txn_id": txn_data.get("txn_id"),
                },
                "customer_data": {
                    "customer_id": customer_data.get("customer_id" , ""),
                    "first_name": customer_data.get("first_name" , ""),
                    "last_name": customer_data.get("last_name" , ""),
                    "email_id": customer_data.get("email_id" , ""),
                    "mobile_no": customer_data.get("mobile_no" , ""),
                    "billing_data": {
                        "address1": billing_data.get("address1" , ""),
                        "address2": billing_data.get("address2" , ""),
                        "address3": billing_data.get("address3" , ""),
                        "pincode": billing_data.get("pincode" , ""),
                        "city": billing_data.get("city" , ""),
                        "state": billing_data.get("state" , ""),
                        "country": billing_data.get("country" , "")
                    },
                    "shipping_data": {
                        "first_name": shipping_data.get("first_name" , ""),
                        "last_name": shipping_data.get("last_name" , ""),
                        "mobile_no": shipping_data.get("mobile_no" , ""),
                        "address1": shipping_data.get("address1" , ""),
                        "address2": shipping_data.get("address2" , ""),
                        "address3": shipping_data.get("address3" , ""),
                        "pincode": shipping_data.get("pincode" , ""),
                        "city": shipping_data.get("city" , ""),
                        "state": shipping_data.get("state" , ""),
                        "country": shipping_data.get("country" , "")
                    }
                },
                "payment_data": {
                    "amount_in_paisa": txn_data.get("amount_in_paisa"),
                },
                "txn_data": {
                    "navigation_mode": 2,
                    "payment_mode": payment_mode,
                    "transaction_type": 1
                },
                "udf_data": {
                    "udf_field_1": udf_data.get("udf_field_1", ""),
                    "udf_field_2": udf_data.get("udf_field_2", ""),
                    "udf_field_3": udf_data.get("udf_field_3", ""),
                    "udf_field_4": udf_data.get("udf_field_4", ""),
                    "udf_field_5": udf_data.get("udf_field_5", "")
                },
                "product_details" : products_details
            }

            # Encoding Payload in Base64
            jsonString = json.dumps(payload)
            jsonBytes = jsonString.encode('utf-8')
            encodedPayload = base64.b64encode(jsonBytes).decode('utf-8')

            hash = self.hash.create(encodedPayload)

            # Headers
            headers = {
                "Content-Type": "application/json",  # Adjust the content type as needed
                "X-VERIFY": hash  # Add hash string for the request
            }
            
            # Sending Request to PineLabs
            response = requests.post(endpoint, headers=headers, json={"request": encodedPayload})
            response = response.json()

            if response.get("respone_code")  :
                if int(response.get("respone_code")) != 1 :
                    raise Exception(str(response.get("respone_message")))
                
            if  response.get("response_code") :
                if  int(response.get("response_code")) != 1:
                    raise Exception(str(response.get("response_message")))

            return {
                "status": True,
                "redirect_url": response.get("redirect_url"),
                "token" : response.get("token")
            }
        except Exception as e:
            raise Exception(str(e))

    def fetch(self, txn_id):
        # Fetch order from pinelabs for the given payload | body
        try:
            # Endpoint
            endpoint = self.endpoint + 'PG/V2'

            # Headers
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",  # Adjust the content type as needed
            }

            payload = {
                "ppc_MerchantAccessCode": self.key,
                "ppc_MerchantID": self.mid,
                "ppc_TransactionType": "3",
                "ppc_UniqueMerchantTxnID": txn_id
            }

            # Encode all characters except spaces and forward slashes and ":"
            encodedPayload = '&'.join([f'{key}={self.hash.custom_quote(value)}' for key, value in payload.items()])

            hash = self.hash.create(encodedPayload)

            payload['ppc_DIA_SECRET'] = hash
            payload['ppc_DIA_SECRET_TYPE'] = "sha256"

            response = requests.post(endpoint, headers=headers, data=payload)
            response = response.json()

            if not isinstance(response, dict):
                raise Exception(str(response))
            
            if not response.get("ppc_ParentTxnResponseCode") :
                raise Exception(str(response.get("ppc_TxnResponseMessage")))

            return response
        except Exception as e:
            raise Exception(str(e))
