from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    phn = request.args.get('username')  # Get the 'username' parameter from the URL
    if not phn:
        return jsonify({
            "status": "error",
            "message": "Username parameter is missing.",
            "Dev": "Join @ihc_apis For More Unique Apis"
        })
    
    # Define the URL with GET parameters
    url = f"https://paragon-ihc.vercel.app/?usr={phn}"

    try:
        # Send GET request
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return jsonify({
            "status": "success",
            "info": response.text,
            'dev': "Join @ihc_apis For More Unique Apis"
        })
    except requests.exceptions.RequestException:
        # If the request failed
        return jsonify({
            "status": "error",
            "message": "User not found or failed to retrieve user details.",
            "Dev": "Join @ihc_apis For More Unique Apis"
        })

if __name__ == '__main__':
    app.run(debug=True)
