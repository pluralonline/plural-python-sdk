from flask import Flask, render_template, request, redirect
from src.Pinelabs import Pinelabs

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/submit', methods=['POST'])
def submit():

    merchantId = request.form.get('merchant_id')
    apiAccessCode = request.form.get('access_code')
    secret = request.form.get('secret')
    isTestMode = request.form.get('pg_mode')
    
    txn_id = request.form.get('txn_id')
    callback = request.form.get('callback_url')
    amount_in_paisa = request.form.get('amount_in_paisa')

    pinelabs = Pinelabs(merchantId, apiAccessCode, secret, isTestMode)

    txn_data =  {
        "txn_id" : txn_id,
        "callback" : callback,
        "amount_in_paisa" : amount_in_paisa
    }
    
    products_data = [
        {
            "product_code" : request.form.get('product_code'),
            "product_amount" : request.form.get('product_amount')
        }
    ]

    selected_payment_modes = request.form.getlist('payment_modes')

    payment_modes = {
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

    for mode in selected_payment_modes:
        if mode in payment_modes:
            payment_modes[mode] = True
    
    customer_data = {
        'customer_id' : request.form.get('customer_id'),
        'first_name' : request.form.get('first_name'),
        'last_name' : request.form.get('last_name'),
        'email_id' : request.form.get('email'),
        'mobile_no' : request.form.get('phone')
    }

    billing_data = {
        'address1' : request.form.get('billing_address1'),
        'address2' : request.form.get('billing_address2'),
        'address3' : request.form.get('billing_address3'),
        'pincode' : request.form.get('billing_pincode'),
        'city' : request.form.get('billing_city'),
        'state' : request.form.get('billing_state'),
        'country' : request.form.get('billing_country'),
    }

    shipping_data = {
        'first_name' : request.form.get('shipping_first_name'),
        'last_name' : request.form.get('shipping_last_name'),
        'mobile_no' : request.form.get('shipping_phone'),
        'address1' : request.form.get('shipping_address1'),
        'address2' : request.form.get('shipping_address2'),
        'address3' : request.form.get('shipping_address3'),
        'pincode' : request.form.get('shipping_pincode'),
        'city' : request.form.get('shipping_city'),
        'state' : request.form.get('shipping_state'),
        'country' : request.form.get('shipping_country'),
    }

    udf_data = {
        'udf_field_1' : request.form.get('udf1'),
        'udf_field_2' : request.form.get('udf2'),
        'udf_field_3' : request.form.get('udf3'),
        'udf_field_4' : request.form.get('udf4'),
        'udf_field_5' : request.form.get('udf5'),
    }

    # Order Create
    try :
        orderCreateResponse = pinelabs.payment.create(txn_data, customer_data, billing_data, shipping_data, udf_data, payment_modes, products_data)
        if 'redirect_url' in orderCreateResponse:
            redirect_url = orderCreateResponse['redirect_url']
            return redirect(redirect_url)
        else:
            return "Redirect URL not found in the API response."
    except Exception as e:
        return f'Exception : {e}'


if __name__ == '__main__':
    app.run(debug=True)