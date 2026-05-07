from flask import Flask, request, jsonify
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# =========================
# JWT CACHE
# =========================
jwt_cache = {}

# =========================
# LOGIN API
# =========================
LOGIN_API = "http://vk-jwt-personal.vercel.app/guest_to_jwt?uid={uid}&password={password}"

# =========================
# GET JWT TOKEN
# =========================
def get_jwt(uid, password):
    key = f"{uid}:{password}"

    if key in jwt_cache:
        cached = jwt_cache[key]
        if time.time() - cached["time"] < 3600:
            return cached["token"]

    try:
        url = LOGIN_API.format(uid=uid, password=password)
        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            return None

        data = res.json()

        token = data.get("jwt_token") or data.get("access_token")

        if not token:
            return None

        jwt_cache[key] = {
            "token": token,
            "time": time.time()
        }

        return token

    except Exception:
        return None


# =========================
# UID ENCRYPTION
# =========================
def Encrypt_ID(x):
    try:
        x = int(x)
    except:
        return ""

    dec = [
        '80','81','82','83','84','85','86','87','88','89','8a','8b','8c','8d','8e','8f',
        '90','91','92','93','94','95','96','97','98','99','9a','9b','9c','9d','9e','9f',
        'a0','a1','a2','a3','a4','a5','a6','a7','a8','a9','aa','ab','ac','ad','ae','af',
        'b0','b1','b2','b3','b4','b5','b6','b7','b8','b9','ba','bb','bc','bd','be','bf',
        'c0','c1','c2','c3','c4','c5','c6','c7','c8','c9','ca','cb','cc','cd','ce','cf',
        'd0','d1','d2','d3','d4','d5','d6','d7','d8','d9','da','db','dc','dd','de','df',
        'e0','e1','e2','e3','e4','e5','e6','e7','e8','e9','ea','eb','ec','ed','ee','ef',
        'f0','f1','f2','f3','f4','f5','f6','f7','f8','f9','fa','fb','fc','fd','fe','ff'
    ]

    xxx = [
        '1','01','02','03','04','05','06','07','08','09','0a','0b','0c','0d','0e','0f',
        '10','11','12','13','14','15','16','17','18','19','1a','1b','1c','1d','1e','1f',
        '20','21','22','23','24','25','26','27','28','29','2a','2b','2c','2d','2e','2f',
        '30','31','32','33','34','35','36','37','38','39','3a','3b','3c','3d','3e','3f',
        '40','41','42','43','44','45','46','47','48','49','4a','4b','4c','4d','4e','4f',
        '50','51','52','53','54','55','56','57','58','59','5a','5b','5c','5d','5e','5f',
        '60','61','62','63','64','65','66','67','68','69','6a','6b','6c','6d','6e','6f',
        '70','71','72','73','74','75','76','77','78','79','7a','7b','7c','7d','7e','7f'
    ]

    x = x / 128

    if x > 128:
        x = x / 128

        if x > 128:
            x = x / 128

            if x > 128:
                x = x / 128

                strx = int(x)
                y = (x - strx) * 128
                stry = int(y)

                z = (y - stry) * 128
                strz = int(z)

                n = (z - strz) * 128
                strn = int(n)

                m = (n - strn) * 128

                return (
                    dec[int(m)] +
                    dec[int(n)] +
                    dec[int(z)] +
                    dec[int(y)] +
                    xxx[int(x)]
                )

    return ""


# =========================
# AES ENCRYPTION
# =========================
def encrypt_api(plain_text):
    try:
        plain_text = bytes.fromhex(plain_text)
    except:
        return ""

    key = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
    iv  = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])

    cipher = AES.new(key, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(pad(plain_text, AES.block_size))

    return cipher_text.hex()


# =========================
# MAIN API
# =========================
@app.route("/", methods=["GET"])
def friend_action():

    uid = request.args.get("uid")
    password = request.args.get("password")
    player_uid = request.args.get("player_uid")
    action = request.args.get("action")

    if not uid or not password:
        return jsonify({"success": False, "message": "uid and password required"}), 400

    if not player_uid:
        return jsonify({"success": False, "message": "player_uid required"}), 400

    if action not in ["add", "remove"]:
        return jsonify({"success": False, "message": "action must be add/remove"}), 400

    token = get_jwt(uid, password)

    if not token:
        return jsonify({"success": False, "message": "Login failed / JWT not found"}), 401

    url = (
        "https://clientbp.ggpolarbear.com/RequestAddingFriend"
        if action == "add"
        else "https://clientbp.ggpolarbear.com/RemoveFriend"
    )

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB51",
        "Host": "clientbp.common.ggbluefox.com",
        "User-Agent": "Free Fire/2019117061",
        "Authorization": f"Bearer {token}",
        "Accept": "*/*"
    }

    encrypted_uid = Encrypt_ID(player_uid)

    if not encrypted_uid:
        return jsonify({"success": False, "message": "UID encryption failed"}), 400

    data0 = "08c8b5cfea1810" + encrypted_uid + "18012008"
    encrypted_payload = encrypt_api(data0)

    if not encrypted_payload:
        return jsonify({"success": False, "message": "Payload encryption failed"}), 500

    payload = bytes.fromhex(encrypted_payload)

    # ✅ FIXED INDENTATION START HERE
    try:
        response = requests.post(
            url,
            headers=headers,
            data=payload,
            verify=False,
            timeout=10
        )

        text = response.text.upper()

        if action == "add":
            if response.status_code == 200:
                message = "Friend added successfully"
            elif "DUPLICATE" in text:
                message = "Already friend"
            else:
                message = "Friend add success"
        else:
            if response.status_code == 200:
                message = "Friend removed successfully"
            else:
                message = "Friend remove failed"

        return jsonify({
            "success": "successfully" in message,
            "message": message
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    print("SERVER STARTED")
    app.run(host="0.0.0.0", port=5000, debug=False)