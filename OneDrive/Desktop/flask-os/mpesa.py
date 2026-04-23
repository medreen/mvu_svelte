import time
import math
import base64
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
SAF_SHORT_CODE = os.getenv("SAF_SHORT_CODE")
SAF_STK_PUSH_URL = os.getenv("SAF_STK_PUSH_URL")
SAF_TOKEN_URL = os.getenv("SAF_TOKEN_URL")
SAF_PASSKEY = os.getenv("SAF_PASSKEY")
my_call_url = os.getenv("my_call_url")


# time will be sent to the stk push
# request is for sending http like axios
# math is for converting into an integer
# base64 is used for hashing for security
# httpbasicauth is for getting token for authentication

def get_mpesa_access_token():
    try:
        res = requests.get(
            SAF_TOKEN_URL,
            auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET),
        )
        token = res.json()['access_token']

    except Exception as e:
        print(str(e), "error getting access token")
        raise e

    return token

mytoken=get_mpesa_access_token()
print(mytoken)

timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

headers = {
            "Authorization": f"Bearer {mytoken}",
            "Content-Type": "application/json"
        }

def generate_password():
        password_str = SAF_SHORT_CODE + SAF_PASSKEY + timestamp
        password_bytes = password_str.encode()

        return base64.b64encode(password_bytes).decode("utf-8")

password = generate_password()
print(password)

def make_stk_push(payload):
        print("paylod:-----------------")
        amount = payload['amount']
        phone_number = payload['phone_number']
        push_data = {
            "BusinessShortCode": SAF_SHORT_CODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": math.ceil(float(amount)),
            "PartyA": phone_number,
            "PartyB": SAF_SHORT_CODE,
            "PhoneNumber": phone_number,
            "CallBackURL": my_call_url,
            "AccountReference": "Whatever you call your app",
            "TransactionDesc": "description of the transaction",
        }

        response = requests.post(
            SAF_STK_PUSH_URL,
            json=push_data,
            headers=headers)

        response_data = response.json()
        print("response:------",response_data)

        return response_data

# stk = make_stk_push({"amount":"1","phone_number":"254717824020"})
# print(stk)