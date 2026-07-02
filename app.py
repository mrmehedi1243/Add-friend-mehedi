from flask import Flask, request, jsonify
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import urllib3
import time
import binascii

import my_pb2
import output_pb2

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# ============================================
# CREDIT
# ============================================
CREDIT = "http://t.me/proxaura"

# ============================================
# JWT CACHE
# ============================================
jwt_cache = {}

# ============================================
# AES CONFIG
# ============================================
AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

# ============================================
# ENCRYPT MESSAGE
# ============================================
def encrypt_message(plaintext):

    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)

    padded_message = pad(plaintext, AES.block_size)

    return cipher.encrypt(padded_message)

# ============================================
# GET ACCESS TOKEN + OPEN_ID
# ============================================
def get_access_token(uid, password):

    oauth_url = "https://100067.connect.garena.com/oauth/guest/token/grant"

    payload = {
        'uid': uid,
        'password': password,
        'response_type': "token",
        'client_type': "2",
        'client_secret': "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        'client_id': "100067"
    }

    headers = {
        'User-Agent': "GarenaMSDK/4.0.19P9(SM-M526B ;Android 13;pt;BR;)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip"
    }

    try:

        response = requests.post(
            oauth_url,
            data=payload,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return None, None

        data = response.json()

        access_token = data.get("access_token")
        open_id = data.get("open_id")

        return access_token, open_id

    except Exception:
        return None, None

# ============================================
# GENERATE JWT
# ============================================
def get_jwt(uid, password):

    cache_key = f"{uid}:{password}"

    # CACHE
    if cache_key in jwt_cache:

        cached = jwt_cache[cache_key]

        if time.time() - cached["time"] < 3600:
            return cached["token"]

    access_token, open_id = get_access_token(uid, password)

    if not access_token or not open_id:
        return None

    platforms = [8, 3, 4, 6]

    for platform_type in platforms:

        try:

            game_data = my_pb2.GameData()

            game_data.timestamp = "2024-12-05 18:15:32"
            game_data.game_name = "free fire"
            game_data.game_version = 1
            game_data.version_code = "1.108.3"
            game_data.os_info = "Android OS 9"
            game_data.device_type = "Handheld"
            game_data.network_provider = "Verizon"
            game_data.connection_type = "WIFI"
            game_data.screen_width = 1280
            game_data.screen_height = 960
            game_data.dpi = "240"
            game_data.cpu_info = "ARMv7"
            game_data.total_ram = 5951
            game_data.gpu_name = "Adreno"
            game_data.gpu_version = "OpenGL ES 3.0"
            game_data.user_id = "Google"
            game_data.ip_address = "172.190.111.97"
            game_data.language = "en"

            game_data.open_id = open_id
            game_data.access_token = access_token
            game_data.platform_type = platform_type
            game_data.field_99 = str(platform_type)
            game_data.field_100 = str(platform_type)

            serialized_data = game_data.SerializeToString()

            encrypted_data = encrypt_message(serialized_data)

            hex_data = binascii.hexlify(encrypted_data).decode()

            login_url = "https://loginbp.ggpolarbear.com/MajorLogin"

            headers = {
    "User-Agent": "GarenaMSDK/4.0.19P9(Android 13)",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Unity-Version": "2018.4.11f1",
    "X-GA": "v1 1",
    "ReleaseVersion": "OB54",
}

            response = requests.post(
                login_url,
                data=bytes.fromhex(hex_data),
                headers=headers,
                verify=False,
                timeout=10
            )

            if response.status_code != 200:
                continue

            example_msg = output_pb2.Garena_420()

            example_msg.ParseFromString(response.content)

            data_dict = {
                field.name: getattr(example_msg, field.name)
                for field in example_msg.DESCRIPTOR.fields
            }

            token = data_dict.get("token")

            if token:

                jwt_cache[cache_key] = {
                    "token": token,
                    "time": time.time()
                }

                return token

        except Exception:
            continue

    return None

# ============================================
# UID ENCRYPTION
# ============================================
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

                z = (y - int(y)) * 128

                n = (z - int(z)) * 128

                m = (n - int(n)) * 128

                return (
                    dec[int(m)] +
                    dec[int(n)] +
                    dec[int(z)] +
                    dec[int(y)] +
                    xxx[int(x)]
                )

    return ""

# ============================================
# FRIEND PAYLOAD ENCRYPT
# ============================================
def encrypt_api(plain_text):

    try:
        plain_text = bytes.fromhex(plain_text)
    except:
        return ""

    key = bytes([
        89,103,38,116,99,37,68,69,
        117,104,54,37,90,99,94,56
    ])

    iv = bytes([
        54,111,121,90,68,114,50,50,
        69,51,121,99,104,106,77,37
    ])

    cipher = AES.new(key, AES.MODE_CBC, iv)

    cipher_text = cipher.encrypt(
        pad(plain_text, AES.block_size)
    )

    return cipher_text.hex()

# ============================================
# HOME PAGE
# ============================================
@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "status": "online",

        "credit": CREDIT,

        "endpoints": {

            "add_friend":
            "/add_friend?uid=123456&password=YOUR_PASSWORD&friend_uid=999999",

            "remove_friend":
            "/remove_friend?uid=123456&password=YOUR_PASSWORD&friend_uid=999999"

        }

    })

# ============================================
# ADD FRIEND
# ============================================
@app.route("/add_friend", methods=["GET"])
def add_friend():

    return handle_friend_action("add")

# ============================================
# REMOVE FRIEND
# ============================================
@app.route("/remove_friend", methods=["GET"])
def remove_friend():

    return handle_friend_action("remove")

# ============================================
# MAIN FRIEND FUNCTION
# ============================================
def handle_friend_action(action):

    uid = request.args.get("uid")

    password = request.args.get("password")

    friend_uid = request.args.get("friend_uid")

    if not uid or not password:

        return jsonify({
            "success": False,
            "credit": CREDIT,
            "message": "uid and password required"
        }), 400

    if not friend_uid:

        return jsonify({
            "success": False,
            "credit": CREDIT,
            "message": "friend_uid required"
        }), 400

    token = get_jwt(uid, password)

    if not token:

        return jsonify({
            "success": False,
            "credit": CREDIT,
            "message": "JWT generation failed"
        }), 401

    url = (
        "https://clientbp.ggpolarbear.com/RequestAddingFriend"
        if action == "add"
        else "https://clientbp.ggpolarbear.com/RemoveFriend"
    )

    headers = {
            "User-Agent": "fadai/1.0 (Linux; Android 13; SM-S918B Build/TP1A.220.624.014)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/x-www-form-urlencoded",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': "OB54"
        }

    encrypted_uid = Encrypt_ID(friend_uid)

    if not encrypted_uid:

        return jsonify({
            "success": False,
            "credit": CREDIT,
            "message": "UID encryption failed"
        }), 400

    data0 = "08c8b5cfea1810" + encrypted_uid + "18012008"

    encrypted_payload = encrypt_api(data0)

    if not encrypted_payload:

        return jsonify({
            "success": False,
            "credit": CREDIT,
            "message": "Payload encryption failed"
        }), 500

    payload = bytes.fromhex(encrypted_payload)

    try:
        response = requests.post(
            url,
            headers=headers,
            data=payload,
            verify=False,
            timeout=10
        )

        print("Status:", response.status_code)
        print("Text:", response.text)
        print("Hex:", response.content.hex())

        if action == "add":
            if response.status_code == 200:
                message = "Friend added successfully"
            else:
                message = "Friend add failed"
        else:
            if response.status_code == 200:
                message = "Friend removed successfully"
            else:
                message = "Friend remove failed"

        return jsonify({
            "success": response.status_code == 200,
            "credit": CREDIT,
            "action": action,
            "friend_uid": friend_uid,
            "message": message,
            "status_code": response.status_code
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "credit": CREDIT,
            "message": str(e)
        }), 500
# ============================================
# START SERVER
# ============================================
if __name__ == "__main__":

    print("===================================")
    print("      FRIEND API STARTED")
    print("===================================")
    print("CREDIT :", CREDIT)
    print("ADD    : /add_friend")
    print("REMOVE : /remove_friend")
    print("===================================")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )