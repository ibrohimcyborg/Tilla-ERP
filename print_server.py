from flask import Flask, request, jsonify
from flask_cors import CORS
import socket

app = Flask(__name__)
CORS(app)

PRINTER_IP = "192.168.123.100"
PRINTER_PORT = 9100

def send_to_printer(data: bytes):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((PRINTER_IP, PRINTER_PORT))
    s.send(data)
    s.close()

@app.route('/print', methods=['POST'])
def print_receipt():
    try:
        body = request.json
        text = body.get('text', '')

        ESC = b'\x1b'
        GS = b'\x1d'

        commands = bytearray()
        commands += ESC + b'@'           # printer reset
        commands += ESC + b'a\x01'      # center align
        commands += ESC + b'!\x30'      # bold + double size
        commands += "TILLA HISOB\n".encode('utf-8')
        commands += ESC + b'!\x00'      # normal
        commands += b'-' * 32 + b'\n'
        commands += text.encode('utf-8')
        commands += b'\n\n\n'
        commands += GS + b'V\x41\x03'  # cut paper

        send_to_printer(bytes(commands))
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok", "printer": PRINTER_IP})

if __name__ == '__main__':
    print("Tilla ERP Print Server ishga tushdi!")
    print("Manzil: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
