# python server which is alwaus running and listening for the client requests on localhost 5000
# performs error checking whether the input is valid or not, valid inputs are positive integers only
# if invalid input, sends error message back and print it out in pretty format
# if valid input, sends the input to the server.py for further processing


from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/sum', methods=['POST'])
def sum():
    number = request.form['number']
    if number.isdigit() and int(number) > 0:
        response = requests.post('http://localhost:5001/sum', data={'number': number})
        return response.text
    else:
        return jsonify({'error': 'Invalid input. Please enter a positive integer.'})
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)
