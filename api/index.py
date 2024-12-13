from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_instagram_info():
    user = request.args.get('user')
    if not user:
        return jsonify({"error": "User parameter is missing"}), 400

    url = f"https://instagram-scraper-2022.p.rapidapi.com/ig/info_username/?user={user}"

    headers = {
        "X-RapidAPI-Host": "instagram-scraper-2022.p.rapidapi.com",
        "X-RapidAPI-Key": "1ada1dca31msh859f6cf42873fa7p132780jsn3b8c1cea2f84"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        user_data = data.get("user", {})

        info = {
            "profile": user_data.get("profile_pic_url"),
            "name": user_data.get("full_name"),
            "username": user_data.get("username"),
            "is_private": user_data.get("is_private"),
            "follower": user_data.get("follower_count"),
            "following": user_data.get("following_count"),
            "is_business": user_data.get("is_business"),
            "bio": user_data.get("biography"),
            "is_verified": user_data.get("is_verified"),
            "dev": "Join @ihc_apis For More Unique Apis"
        }

        return jsonify(info)

    except requests.exceptions.RequestException as err:
        return jsonify({"error": f"Request error: {str(err)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
