import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 3000
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print("=" * 60)
        print(f" Web Bluetooth Dashboard is running at:")
        print(f" {url}")
        print("=" * 60)
        print("Press Ctrl + C to stop the server.")
        
        # Open in default browser (Chrome / Edge)
        try:
            webbrowser.open(url)
        except Exception:
            pass

        httpd.serve_forever()

if __name__ == "__main__":
    start_server()
