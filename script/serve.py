"""
Simple HTTP server for local development.

Run this to serve the Wisconsin Realignment Map locally.
"""

import http.server
import socketserver
from pathlib import Path

PORT = 8000
DIRECTORY = Path(__file__).parent.parent

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("=" * 70)
    print("Wisconsin Realignment Map - Local Server")
    print("=" * 70)
    print(f"\nServing at: http://localhost:{PORT}")
    print(f"Directory: {DIRECTORY}")
    print("\nOpen in your browser:")
    print(f"  http://localhost:{PORT}/index.html")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
