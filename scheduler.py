# scheduler listens for input on port 5001 and computes the sum of numbers from 1 to the input number in a for loop and displays the result on the browser


import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sum', methods=['POST'])
def sum():
    number = int(request.form['number'])
    total = 0
    for i in range(1, number + 1):
        total += i

    return jsonify({'result': total})

if __name__ == '__main__':
    app.run(port=5001, debug=True)