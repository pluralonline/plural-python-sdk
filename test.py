from src.Pinelabs import Pinelabs

merchantId = '' # Merchant ID
accessCode = '' # Access Code
secret = '' # Secret Key

pinelabs = Pinelabs(merchantId, accessCode, secret, isTest=True)

txn_data =  {
    "txn_id" : "650acb67d3752",
    "callback" : "http://httpbin.org/post/",
    "amount_in_paisa" : "10000"
}

customer_data = {
    "email_id": "vipinra@gmail.com",
    "first_name" : "vipin",
    "last_name" : "raj",
    "mobile_no" : "9876543210",
    "customer_id" : "CUSTOMER20393",
}

billing_data = {
    "address1" : "House no 1, Vikas nagar",
    "address2" : "Rewari",
    "address3" : "Rewari, haryana",
    "pincode" : "123401",
    "city" : "Gurgaon",
    "state" : "Haryana",
    "country" : "India"
}

shipping_data = {
    "first_name" : "vipin",
    "last_name" : "raj",
    "mobile_no" : "9876543210",
    "address1" : "House no 1, Vikas nagar",
    "address2" : "Rewari",
    "address3" : "Rewari, haryana",
    "pincode" : "123401",
    "city" : "Gurgaon",
    "state" : "Haryana",
    "country" : "India"
}

udf_data = {
    "udf_field_1" : "",
    "udf_field_2" : "",
    'udf_field_3' : "",
    "udf_field_4" : "",
    "udf_field_5" : ""
}

payment_mode = {
    "cards": True,
    "netbanking": True,
    "wallet": True,
    "upi": True,
    "emi": True,
    "debit_emi": True,
    "cardless_emi": True,
    "bnpl": True,
    "prebooking": True,
}

products_details = [
    {
        "product_code" : "testproduct02",
        "product_amount" : "10000",
    }
]



# Order Create
try :
    orderCreateResponse = pinelabs.payment.create(txn_data, customer_data, billing_data, shipping_data, udf_data, payment_mode, products_details)
    print(orderCreateResponse)
except Exception as e:
    print("Exception : " , e)




# Order Fetch
try :
    orderFetchResponse = pinelabs.payment.fetch(txn_data["txn_id"])
    print({"response":orderFetchResponse})
except Exception as e:
    print("Exception : " , e)



# Hash Verification
try :
    orderFetchResponse = pinelabs.payment.fetch(txn_data["txn_id"])

    hash = orderFetchResponse["ppc_DIA_SECRET"]

    keys_to_remove = ['ppc_DIA_SECRET', 'ppc_DIA_SECRET_TYPE']

    for key in keys_to_remove:
        orderFetchResponse.pop(key, None)

    verifyHashResponse = pinelabs.hash.verify(hash, orderFetchResponse)
    print(verifyHashResponse)
except Exception as e:
    print("Exception : " , e)



# Order EMI Calculation
try :
    orderEmiResponse = pinelabs.emi.calculate(txn_data, products_details)
    print(orderEmiResponse)
except Exception as e:
    print("Exception : " , e)