from flask import Flask, request, jsonify
from flask_cors import CORS
import win32print
import win32api
import os, tempfile

app = Flask(__name__)
CORS(app)

@app.route('/print', methods=['POST'])
def print_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        printer_name = win32print.GetDefaultPrinter()
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8')
        tmp.write(text)
        tmp.close()
        win32api.ShellExecute(0, 'print', tmp.name, f'/d:"{printer_name}"', '.', 0)
        import threading
        def cleanup():
            import time; time.sleep(5)
            try: os.unlink(tmp.name)
            except: pass
        threading.Thread(target=cleanup, daemon=True).start()
        return jsonify({'ok': True, 'printer': printer_name})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    try:
        printer = win32print.GetDefaultPrinter()
        return jsonify({'ok': True, 'printer': printer})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)})

if __name__ == '__main__':
    print('Printer server ishga tushdi: http://localhost:5000')
    try:
        printer = win32print.GetDefaultPrinter()
        print(f'Printer: {printer}')
    except:
        print('Printer topilmadi!')
    app.run(host='0.0.0.0', port=5000, debug=False)
