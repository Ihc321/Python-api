from flask import Flask, request, jsonify
import requests
 
app = Flask(__name__)
 
@app.route('/', methods=['GET'])
def get_user():
    phn = request.args.get('username')
    
    # Define the URL with GET parameters
    url = f"https://paragon-ihc.vercel.app/?usr={phn}"
    
    try:
        # Send GET request
        response = requests.get(url)
 
        if response.status_code != 200:
            return jsonify({
                "status": "error",
                "message": "User not found or failed to retrieve user details.",
                "Dev": "Join @ihc_apis For More Unique Apis"
            })
        
        # If request is successful, return the response data
        return jsonify({
            "status": "success",
            "info": response.text,
            "dev": "Join @ihc_apis For More Unique Apis"
        })
 
    except requests.RequestException as e:
        # If there's an error with the request
        return jsonify({
            "status": "error",
            "message": f"Error occurred: {str(e)}",
            "Dev": "Join @ihc_apis For More Unique Apis"
        })
 
if __name__ == '__main__':
    app.run(debug=True)
 
