import os
from plaid import Client
from datetime import date
from flask import Flask, render_template


app = Flask(__name__)


PLAID_CLIENT_ID=os.environ.get('PLAID_CLIENT_ID')
PLAID_SECRET=os.environ.get('PLAID_SECRET')

client = Client(
    client_id=PLAID_CLIENT_ID, 
    secret=PLAID_SECRET, 
    environment='sandbox',
    api_version='2019-05-29')

access_token = 'access-sandbox-c66ddc4a-a813-4189-a238-5b695ba85507'

def get_last_filtered_transactions():
    today = date.today().isoformat()
    response = client.Transactions.get(access_token, start_date='2016-07-12', end_date=today)
    transactions = response['transactions'][-5:]
    filtered_transactions = []
    for transaction in transactions:
        transaction = {'date':transaction['date'],
                        'amount':transaction['amount'],
                        'transaction_id':transaction['transaction_id']
                    }
        filtered_transactions.append(transaction)
    return filtered_transactions

@app.route('/')
def get_transaction():
    trans = get_last_filtered_transactions()
    return render_template('index.html', trans=trans)