from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Common headers
headers1 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"
}

headers2 = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows; U; Windows NT 6.2; x64; en-US Trident/5.0)"
}

headers3 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Content-Type": "application/json"
}

def send_request(url, headers, data=None):
    if data is not None:
        response = requests.post(url, headers=headers, json=data)
    else:
        response = requests.get(url, headers=headers)
    return response

@app.route('/api/member/forgot_password', methods=['GET'])
def forgot_password():
    phone = request.args.get("phone")
    if not phone:
        return jsonify({"error": "Phone number is required"}), 400

    # First Request
    url1 = "https://www.jaya9.win/api/member/requestCaptchaCode?captcha_id=af51588d-4287-47a5-ac36-b5bb11946bbb&captcha_code=5204"
    response1 = send_request(url1, headers1)

    # Second Request
    url2 = "https://www.jaya9.win/api/member"
    phn = ltrim(phone, '0')
    data2 = {
        "membercode": "a" + phn,
        "password": phn,
        "currency": "BDT",
        "email": "",
        "registration_site": "desktop",
        "mobile": phn,
        "line": "",
        "referral_code": "",
        "is_early_bird": "0",
        "domain": "https://www.jaya9.win",
        "language": "bd",
        "reg_type": 2,
        "agent_team": "",
        "utm_source": None,
        "utm_medium": None,
        "utm_campaign": None,
        "s2": None,
        "fp": "444dbac87a" + phn + "b5132f89dcf11d1676727a",
        "c_id": None,
        "pid": None,
        "stag": None,
        "tracking_url": None,
        "captcha_id": "6f736b71-8188-4615-bef5-f5a83646d4a8",
        "captcha_code": "1357"
    }
    response2 = send_request(url2, headers2, data2)

    # Third Request
    url3 = "https://www.jaya9.win/api/member/requestCaptchaCode?captcha_id=af51588d-4287-47a5-ac36-b5bb11946bbb&captcha_code=8919"
    response3 = send_request(url3, headers1)

    # Fourth Request
    url4 = "https://www.jaya9.win/api/member/reqFgtPsw"
    data4 = {
        'mobile': phn,
        'prefix': '+880',
        'captcha_id': 'af51588d-4287-47a5-ac36-b5bb11946bbb',
        'captcha_code': '8919'
    }
    response4 = send_request(url4, headers3, data4)

    return jsonify({"response": response4.text, "message": "api owner Mustafizur Rahman"}), 200

def ltrim(str, trim_char) {
    return ltrim($str, $trim_char); 
}

if __name__ == '__main__':
    app.run(debug=True)
