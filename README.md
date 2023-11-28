# PineLabs Python SDK

This SDK offers simple to use api for integrating PineLabs api in your python applications. It provide several easy
methods for creating, fetching orders and calculate EMIs and verify hash.

## Installation

In order to use this SDK locally from a folder you'll need to copy the `sdk` folder in your project and import it in your python file.
```javascript
from src.pinelabs import Pinelabs
```

---

## Usage For SDK

### Create Instance of PineLabs SDK

Import pinelabs sdk and create object of Pinelabs class. It takes 4 parameters which are as follows:

1. merchant_id (string) : Merchant ID provided by PineLabs
2. access_code (string) : Merchant Access Code Provided by PineLabs
3. secret (string) : Merchant Secret
4. is_test (boolean) : If using test mode then set this to `true`

```javascript
const pinelabs = Pinelabs("{merchant_id}", "{access_code}", "{secret}", is_test) 
```

---

### Create Order

This section explains how to create order for payment processing. There are a couple of things required in order to
create an order.

### Parameters  Required & Optional

```javascript
// Transaction Data ( Mandatory )
const txn_data = {
    txn_id: "", // String
    callback: "", // String
    amount_in_paisa: "1000", // String
}
```

```javascript
// Customer Data ( Optional )
const customer_data = {
    email_id: "", // String
    first_name: "", // String
    last_name: "", // String
    mobile_no: "", // String
    customer_id: "", // String
}
```

```javascript
// Billing Data ( Optional )
const billing_data = {
    address1: "", // String
    address2: "", // String
    address3: "", // String
    pincode: "", // String
    city: "", // String
    state: "", // String
    country: "", // String
}
```

```javascript
// Shipping Data ( Optional )
const shipping_data = {
    first_name: "", // String
    last_name: "", // String
    mobile_no: "", // String
    address1: "", // String
    address2: "", // String
    address3: "", // String
    pincode: "", // String
    city: "", // String
    state: "", // String
    country: "", // String
}
```

```javascript
// UDF data ( Optional )
const udf_data = {
    udf_field_1: "", // String
    udf_field_2: "", // String
    udf_field_3: "", // String
    udf_field_4: "", // String
    udf_field_5: "", // String
}
```

```javascript
// Payment Modes That Needs To Be Shown ( Mandatory )
const payment_mode = {
    netbanking: true, // Boolean
    cards: true, // Boolean
    emi: true, // Boolean
    upi: true, // Boolean
    cardless_emi: true, // Boolean
    wallet: true, // Boolean
    debit_emi: true, // Boolean
    prebooking: true, // Boolean
    bnpl: true, // Boolean
    paybypoints: false, // Boolean
}
```

```javascript
// Product Details ( Optional, Required For Multicart )
const product_details = [
    {
        "product_code": "testSKU1", // String
        "product_amount": 500000 // Integer
    },
    {
        "product_code": "testSKU1", // String
        "product_amount": 500000 // Integer
    }
]
```

---

### Order Creation

Using the instance of the SDK we created above we will call the `.create()` method on the `payment` interface for
creating an order with the provided parameters. It takes the following positional arguments

1. Transaction Data
2. Customer Data
3. Billing Data
4. Shipping Data
5. UDF Data
6. Payment Modes
7. Product Details

The `create()` method returns a promise with the response or else throws an error if something went wrong.

```javascript
// Create Order
try :
    orderCreateResponse = pinelabs.payment.create(txn_data, customer_data, billing_data, shipping_data, udf_data, payment_mode, products_details)
    print(orderCreateResponse)
except Exception as e:
    print("Exception : " , e)
```

---

#### Success Response

```json
{
  "status": true,
  "redirect_url": "https://uat.pinepg.in/pinepg/v2/process/payment?token=S01wPSlIH%2bopelRVif7m7e4SgrTRIcKYx25YDYfmgtbPOE%3d",
  "token": "S01wPSlIH%2bopelRVif7m7e4SgrTRIcKYx25YDYfmgtbPOE%3d"
}
```

#### Failure Response

```text
Exception : DUPLICATE TRANSACTION ID RECEIVED FROM MERCHANT
```

---

### Fetch Order

Using the instance of the SDK we created above we will call the `.fetch()` method on the `payment` interface for
fetching
an order details with the provided transaction id and transaction type. It takes the following positional arguments

1. Transaction ID

```javascript
// Fetch Order
try :
    orderFetchResponse = pinelabs.payment.fetch("650acb67d3752")
    print({"response":orderFetchResponse})
except Exception as e:
    print("Exception : " , e)
```

---

#### Success Response

```json
{
  "ppc_MerchantID": "106600",
  "ppc_MerchantAccessCode": "bcf441be-411b-46a1-aa88-c6e852a7d68c",
  "ppc_PinePGTxnStatus": "7",
  "ppc_TransactionCompletionDateTime": "20\/09\/2023 04:07:52 PM",
  "ppc_UniqueMerchantTxnID": "650acb67d3752",
  "ppc_Amount": "1000",
  "ppc_TxnResponseCode": "1",
  "ppc_TxnResponseMessage": "SUCCESS",
  "ppc_PinePGTransactionID": "12069839",
  "ppc_CapturedAmount": "1000",
  "ppc_RefundedAmount": "0",
  "ppc_AcquirerName": "BILLDESK",
  "ppc_DIA_SECRET": "D640CFF0FCB8D42B74B1AFD19D97A375DAF174CCBE9555E40CC6236964928896",
  "ppc_DIA_SECRET_TYPE": "SHA256",
  "ppc_PaymentMode": "3",
  "ppc_Parent_TxnStatus": "4",
  "ppc_ParentTxnResponseCode": "1",
  "ppc_ParentTxnResponseMessage": "SUCCESS",
  "ppc_CustomerMobile": "7737291210",
  "ppc_UdfField1": "",
  "ppc_UdfField2": "",
  "ppc_UdfField3": "",
  "ppc_UdfField4": "",
  "ppc_AcquirerResponseCode": "0300",
  "ppc_AcquirerResponseMessage": "NA"
}
```

#### Failure Response

```textmate
Exception : Invalid Data
```

---

### EMI Calculator

Using the instance of the SDK we created above we will call the `.calculate()` method on the `emi` interface for
fetching
offers for EMI with the provided product details. It takes the following positional arguments

1. Transaction Data
2. Product Details

```javascript
// Emi Calculation
const txn_data = {
    amount_in_paisa: "1000",
}

const products_details = [
    {
        "product_code": "testproduct02",
        "product_amount": "10000"
    }
];

try :
    orderEmiResponse = pinelabs.emi.calculate(txn_data, products_details)
    print(orderEmiResponse)
except Exception as e:
    print("Exception : " , e)
```

---

#### Success Response

```json
{
  "issuer": [
    {
      "list_emi_tenure": [
        {
          "offer_scheme": {
            "product_details": [
              {
                "schemes": [],
                "product_code": "testproduct02",
                "product_amount": 10000,
                "subvention_cashback_discount": 0,
                "product_discount": 0,
                "subvention_cashback_discount_percentage": 0,
                "product_discount_percentage": 0,
                "subvention_type": 3,
                "bank_interest_rate_percentage": 150000,
                "bank_interest_rate": 251
              }
            ],
            "emi_scheme": {
              "scheme_id": 48040,
              "program_type": 105,
              "is_scheme_valid": true
            }
          },
          "tenure_id": "3",
          "tenure_in_month": "3",
          "monthly_installment": 3417,
          "bank_interest_rate": 150000,
          "interest_pay_to_bank": 251,
          "total_offerred_discount_cashback_amount": 0,
          "loan_amount": 10000,
          "auth_amount": 10000
        },
        {
          "offer_scheme": {
            "product_details": [
              {
                "schemes": [],
                "product_code": "testproduct02",
                "product_amount": 10000,
                "subvention_cashback_discount": 0,
                "product_discount": 0,
                "subvention_cashback_discount_percentage": 0,
                "product_discount_percentage": 0,
                "subvention_type": 3,
                "bank_interest_rate_percentage": 150000,
                "bank_interest_rate": 440
              }
            ],
            "emi_scheme": {
              "scheme_id": 48040,
              "program_type": 105,
              "is_scheme_valid": true
            }
          },
          "tenure_id": "6",
          "tenure_in_month": "6",
          "monthly_installment": 1740,
          "bank_interest_rate": 150000,
          "interest_pay_to_bank": 440,
          "total_offerred_discount_cashback_amount": 0,
          "loan_amount": 10000,
          "auth_amount": 10000
        }
      ],
      "issuer_name": "HDFC",
      "is_debit_emi_issuer": false
    }
  ],
  "response_code": 1,
  "response_message": "SUCCESS"
}
```

#### Failure Response

```text
Exception : INVALID DATA,MISMATCH_IN_TOTAL_CART_AMOUNT_AND_TOTAL_PRODUCT_AMOUNT
```

---

### Verify Hash

Using the instance of the SDK we created above we will call the `.verify()` method on the `hash` interface for
verifying
a hash received in the response of callback and webhooks. It takes the following positional arguments

1. Hash Received in Response ( `ppc_DIA_SECRET` )
2. Response Received ( Not including `ppc_DIA_SECRET` and `ppc_DIA_SECRET_TYPE` )

```javascript
// Verify Hash
try :
    hash = orderResponse["ppc_DIA_SECRET"]

    keys_to_remove = ["ppc_DIA_SECRET", "ppc_DIA_SECRET_TYPE"]

    for key in keys_to_remove:
        orderResponse.pop(key, None)

    isVerified = pinelabs.hash.verify(hash, orderResponse)
    print(isVerified)
except Exception as e:
    print("Exception : " , e)
```
