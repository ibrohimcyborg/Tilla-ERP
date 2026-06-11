from flask import Flask, request, jsonify
from flask_cors import CORS
import win32print
import time
app = Flask(__name__)
CORS(app)
def get_printer_name():
    return 'XP-80C'
def send_to_printer(data: bytes):
    printer_name = get_printer_name()
    hPrinter = win32print.OpenPrinter(printer_name)
    try:
        win32print.StartDocPrinter(hPrinter, 1, ("Receipt", None, "RAW"))
        win32print.StartPagePrinter(hPrinter)
        win32print.WritePrinter(hPrinter, data)
        win32print.EndPagePrinter(hPrinter)
        win32print.EndDocPrinter(hPrinter)
    finally:
        win32print.ClosePrinter(hPrinter)
def safe(text):
    result = []
    for ch in text:
        if ord(ch) < 128:
            result.append(ch)
        else:
            result.append('?')
    return ''.join(result)
@app.route('/print', methods=['POST'])
def print_receipt():
    try:
        body = request.json
        text = body.get('text', '')
        ESC = b'\x1b'
        GS  = b'\x1d'
        cmd = bytearray()
        cmd += ESC + b'@'
        cmd += ESC + b'!\x00'
        cmd += ESC + b'a\x00'
        for line in text.split('\n'):
            cmd += safe(line).encode('ascii', errors='replace') + b'\n'
            time.sleep(0.01)
        cmd += b'\n\n\n'
        cmd += GS + b'V\x41\x03'
        send_to_printer(bytes(cmd))
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
@app.route('/printers', methods=['GET'])
def list_printers():
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    return jsonify({"printers": [p[2] for p in printers], "default": win32print.GetDefaultPrinter()})
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"})
if __name__ == '__main__':
    print("Tilla ERP Print Server ishga tushdi!")
    print("Manzil: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
