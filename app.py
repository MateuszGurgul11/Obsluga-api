import requests
import csv
from flask import Flask, render_template, request
import math

app = Flask(__name__)

response = requests.get("https://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

rates = data[0]['rates']

def import_data_to_csv():
    with open('rates.txt', 'w', newline='') as csvfile:
        fieldnames = ["currency", "code", "bid", "ask"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()
        
        for rate in rates:
            writer.writerow(rate)

import_data_to_csv()

def calculate_curency(curency_amount, curency_type):
    cost = 0
    with open('rates.txt', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if row['code'] == curency_type:
                cost = math.ceil(float(row['bid']) * float(curency_amount))
                break
    return cost


@app.route("/", methods = ['POST', 'GET'])
def rate_form():
    cost = None
    if request.method == 'POST':
        data = request.form
        curency_type = data.get('curency_type')
        curency_amount = data.get('curency_amount')
        cost = calculate_curency(curency_amount, curency_type)
    return render_template('index.html', cost=cost)

if __name__ == '__main__':
    app.run(debug=True)
