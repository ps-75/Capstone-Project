from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import sys

# Set up professional logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HEALTHY_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Live App - Healthy</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 50px; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); text-align: center; max-width: 500px; width: 100%; }
        .icon { font-size: 60px; margin: 0; }
        h1 { color: #2c3e50; margin-bottom: 10px; }
        p { color: #7f8c8d; line-height: 1.6; }
        .status { margin: 20px 0; padding: 10px; background: #e8f8f5; color: #1abc9c; border-radius: 5px; font-weight: bold; border: 1px solid #1abc9c; }
        .btn { display: inline-block; margin-top: 20px; padding: 12px 25px; background: #e74c3c; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; transition: 0.3s; box-shadow: 0 4px 6px rgba(231, 76, 60, 0.3); }
        .btn:hover { background: #c0392b; transform: translateY(-2px); }
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">Hello</div>
        <h1>System Online</h1>
        <p>Welcome to the Python Web Application. The system is currently running smoothly and all services are operational.</p>
        <div class="status">Status Code: 200 OK</div>
        <a href="/crash" class="btn">Simulate Critical Crash</a>
    </div>
</body>
</html>
"""

CRASH_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>500 - System Crash</title>
    <style>
        body { font-family: 'Courier New', Courier, monospace; background-color: #c0392b; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { text-align: center; max-width: 600px; padding: 30px; }
        h1 { font-size: 80px; margin: 0; text-shadow: 2px 2px 0px #000; }
        h2 { font-size: 24px; letter-spacing: 2px; margin-bottom: 20px; }
        p { font-size: 18px; margin-bottom: 30px; }
        .terminal { background: #111; color: #e74c3c; padding: 20px; border-radius: 8px; text-align: left; font-size: 14px; line-height: 1.5; border: 1px solid #333; box-shadow: inset 0 0 10px rgba(0,0,0,0.8); }
        .terminal span { color: #2ecc71; }
    </style>
</head>
<body>
    <div class="container">
        <h1>500</h1>
        <h2>INTERNAL SERVER ERROR</h2>
        <p>The application has encountered a fatal memory exception and has been terminated.</p>
        <div class="terminal">
            <span>root@server:~#</span> ERROR: Memory limit exceeded.<br>
            <span>root@server:~#</span> CRITICAL - FATAL EXCEPTION: System crashing now!<br>
            <span>root@server:~#</span> Connection dropped.
        </div>
    </div>
</body>
</html>
"""

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/crash':
            logging.critical("FATAL EXCEPTION: Memory overload! System crashing now!")
            
            # 2. Send the beautiful Red Error UI to the browser
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(CRASH_HTML.encode('utf-8'))
            
            sys.exit(1) 
        else:
            # Normal healthy behavior
            logging.info(f"Healthy request received for page: {self.path}")
            
            # Send the beautiful Green UI to the browser
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HEALTHY_HTML.encode('utf-8'))

# Start the server
server = HTTPServer(('0.0.0.0', 8000), MyHandler)
logging.info("Live Python Application Booted Successfully on port 8000.")
server.serve_forever()
