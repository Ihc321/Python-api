from flask import Flask, request, jsonify
import random
import requests
import json
import time

app = Flask(__name__)

def generate_seed():
    return random.randint(0, 3999999999)

seed_value = generate_seed()

def fetch_url(url, user_agent):
    headers = {
        "Host": "www.decohere.ai",
        "User-Agent": user_agent,
        "Accept": "*/*",
        "X-Requested-With": "mark.via",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.decohere.ai/create",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    }
    response = requests.get(url, headers=headers)
    decoded_response = response.json()
    return decoded_response.get('turboToken')

def fetch_with_auth(url, data, authorization, user_agent):
    headers = {
        "Host": "turbo.decohere.ai",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {authorization}",
        "User-Agent": user_agent,
        "Accept": "*/*",
        "Origin": "https://www.decohere.ai",
        "X-Requested-With": "mark.via",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.decohere.ai/create",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    }
    response = requests.post(url, headers=headers, json=data)
    return {
        'response': response.text,
        'http_code': response.status_code
    }

def fetch_and_display_images(prompt, image_number, turboToken, user_agent):
    url_generate_turbo = "https://turbo.decohere.ai/generate/turbo"
    images = []

    for i in range(image_number):
        data = {
            "prompt": prompt,
            #"seed": 18332673 + i, # Incrementing seed for different images
            "seed": seed_value + i,
            "width": 576,
            "height": 1024,
            "steps": 4,
            "safety_filter": True,
            "enhance": True,
            "submission_time": int(time.time()),
            "customer_id": "not_signed_in"
        }

        result = fetch_with_auth(url_generate_turbo, data, turboToken, user_agent)

        if result['http_code'] == 200:
            response_data = json.loads(result['response'])
            image_data = response_data.get('image', '')
            images.append(image_data)
        else:
            return {
                'error': f"Error: HTTP status code {result['http_code']}"
            }

    return images

@app.route('/generate-images', methods=['POST'])
def generate_images():
    data = request.get_json()
    if 'prompt' in data and 'image' in data:
        prompt = data['prompt']
        image_number = int(data['image'])

        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        ]
        random_user_agent = user_agents[random.randint(0, len(user_agents) - 1)]

        url_account_details = "https://www.decohere.ai/api/accountDetails?token=turbo"
        turboToken = fetch_url(url_account_details, random_user_agent)

        if not turboToken:
            return jsonify({'error': 'Error fetching turboToken.'}), 500

        images = fetch_and_display_images(prompt, image_number, turboToken, random_user_agent)
        if 'error' in images:
            return jsonify(images), 500
        else:
            return jsonify(images), 200
    else:
        return jsonify({'error': 'Invalid parameters.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
