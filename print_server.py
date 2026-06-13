from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))
        text = body.get('text', '')
        try:
            import win32print
            printer = win32print.GetDefaultPrinter()
            hPrinter = win32print.OpenPrinter(printer)
            hJob = win32print.StartDocPrinter(hPrinter, 1, ('chek', None, 'RAW'))
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, text.encode('utf-8', errors='replace'))
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
            win32print.ClosePrinter(hPrinter)
            self._ok('OK')
        except Exception as e:
            self._ok('ERROR: ' + str(e))

    def _ok(self, msg):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({'status': msg}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    print('Print server ishga tushdi: http://localhost:5000')
    HTTPServer(('0.0.0.0', 5000), handler).serve_forever()
