from flask import Flask, jsonify
from flask_cors import CORS  # Import CORS
from py5paisa import FivePaisaClient

# Initialize Flask app
app = Flask(__name__)
CORS(app) 

# Credentials
cred = {
    "APP_NAME": "5P50717413",
    "APP_SOURCE": "22827",
    "USER_ID": "0RopzYZhuYt",
    "PASSWORD": "GZvvC53n4SR",
    "USER_KEY": "Ms8eIWStIrUwGclyknZHKysXkGIbp8ii",
    "ENCRYPTION_KEY": "A68cE68jo4dOwJbaylx6JDcIQQLnao6h"
}

# Initialize FivePaisaClient
client = FivePaisaClient(cred=cred)

# TOTP Authentication
client.get_totp_session('50717413', '082739', '231216')

# Obtain Access Token
access_token = client.get_access_token()

if access_token:
    print("Logged in!!")

# Function to fetch expiry dates for Nifty 50
def get_expiry():
    return {
        "nifty50": client.get_expiry("N", "NIFTY"),
    }

@app.route('/api/option_chain')
def option_chain():
    # Get expiry data using get_expiry() function
    expiry_data = get_expiry().get("nifty50", {}).get("Expiry", [])
    
    if len(expiry_data) > 0:
        # Extract the first expiry timestamp
        first_expiry_timestamp = int(expiry_data[0]["ExpiryDate"][6:-7])
        
        # Get the option chain using the first expiry timestamp
        option_chain_data = client.get_option_chain("N", "NIFTY", first_expiry_timestamp)

        # Print the option chain data
        print("Option chain data:", option_chain_data)

        # Return the option chain data
        return jsonify(option_chain_data)
    else:
        return jsonify({"error": "No expiry data found"})

# Other routes remain the same...

# Function to fetch holdings
def get_holdings():
    return client.holdings()

# Function to fetch margin
def get_margin():
    return client.margin()

# Function to fetch positions
def get_positions():
    return client.positions()

# Function to fetch order book
def get_order_book():
    return client.order_book()

# Function to fetch tradebook
def get_tradebook():
    return client.get_tradebook()

# Function to fetch historical data
def get_historical_data():
    df = client.historical_data('N', 'C', 1660, '15m', '2021-05-25', '2021-06-16')
    data_dict = df.to_dict(orient='records')
    return data_dict

# Define routes
@app.route('/api/holdings')
def holdings():
    data = get_holdings()
    return jsonify(data)

@app.route('/api/margin')
def margin():
    data = get_margin()
    return jsonify(data)

@app.route('/api/positions')
def positions():
    data = get_positions()
    return jsonify(data)

@app.route('/api/order_book')
def order_book():
    data = get_order_book()
    return jsonify(data)

@app.route('/api/tradebook')
def tradebook():
    data = get_tradebook()
    return jsonify(data)

@app.route('/api/expiry')
def expiry():
    data = get_expiry()
    return jsonify(data)


@app.route('/api/historical_data')
def historical_data():
    data = get_historical_data()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
