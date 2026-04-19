from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_html_template(title, content):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{title} - Admin Portal</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; margin: 0; display: flex; height: 100vh; color: #333; }}
            .sidebar {{ width: 260px; background-color: #1e293b; color: white; padding-top: 20px; box-shadow: 2px 0 5px rgba(0,0,0,0.1); }}
            .sidebar h2 {{ text-align: center; margin-bottom: 30px; font-weight: 600; font-size: 22px; letter-spacing: 1px; color: #f8fafc; border-bottom: 1px solid #334155; padding-bottom: 20px; }}
            .sidebar a {{ display: block; color: #cbd5e1; padding: 15px 25px; text-decoration: none; font-size: 15px; transition: 0.2s; border-left: 4px solid transparent; }}
            .sidebar a:hover {{ background-color: #334155; color: white; border-left: 4px solid #3b82f6; }}
            .content-area {{ flex: 1; padding: 40px; overflow-y: auto; }}
            .header {{ margin-bottom: 30px; border-bottom: 1px solid #e2e8f0; padding-bottom: 15px; }}
            .header h1 {{ margin: 0; color: #0f172a; font-size: 26px; }}
            
            /* Card Grid for Metrics */
            .card-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
            .card {{ background: white; padding: 25px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }}
            .card h3 {{ margin-top: 0; color: #64748b; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }}
            .card .value {{ font-size: 32px; font-weight: bold; color: #0f172a; margin: 10px 0; }}
            
            /* Table Styles */
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
            th {{ background-color: #f8fafc; color: #475569; font-weight: 600; font-size: 14px; }}
            td {{ font-size: 14px; color: #334155; }}
            .status-active {{ color: #059669; background: #d1fae5; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
            
            /* Settings Panel Styles */
            .setting-row {{ display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-bottom: 1px solid #e2e8f0; }}
            .setting-row:last-child {{ border-bottom: none; }}
            .setting-info strong {{ font-size: 16px; color: #0f172a; }}
            .setting-info p {{ margin: 5px 0 0; font-size: 14px; color: #64748b; }}
            
            /* Buttons */
            .btn {{ padding: 8px 16px; background-color: #f1f5f9; color: #334155; border: 1px solid #cbd5e1; border-radius: 6px; cursor: pointer; text-decoration: none; font-size: 14px; font-weight: 500; transition: 0.2s; }}
            .btn:hover {{ background-color: #e2e8f0; }}
            .btn-primary {{ background-color: #3b82f6; color: white; border: none; }}
            .btn-primary:hover {{ background-color: #2563eb; }}
            .btn-danger-outline {{ background-color: white; color: #dc2626; border: 1px solid #dc2626; }}
            .btn-danger-outline:hover {{ background-color: #fef2f2; }}
        </style>
    </head>
    <body>
        <div class="sidebar">
            <h2>SystemOS</h2>
            <a href="/">Dashboard Overview</a>
            <a href="/users">User Management</a>
            <a href="/analytics">System Analytics</a>
            <a href="/settings">Server Configuration</a>
        </div>
        <div class="content-area">
            <div class="header">
                <h1>{title}</h1>
            </div>
            {content}
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
        body { font-family: 'Courier New', monospace; background-color: #900; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .terminal { background: #111; padding: 30px; border-radius: 5px; box-shadow: 0 0 20px rgba(0,0,0,0.8); width: 600px; }
        h1 { margin-top: 0; color: #ff4444; }
        span { color: #0f0; }
    </style>
</head>
<body>
    <div class="terminal">
        <h1>[ FATAL ERROR 500 ]</h1>
        <p><span>root@server:~#</span> Exception in thread "main" java.lang.OutOfMemoryError</p>
        <p><span>root@server:~#</span> CRITICAL: Memory pool exhausted. Forcing system shutdown...</p>
        <p><span>root@server:~#</span> Connection to database lost.</p>
        <p><span>root@server:~#</span> Goodbye.</p>
    </div>
</body>
</html>
"""

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. HOME PAGE
        if self.path == '/' or self.path == '/home':
            logging.info("Traffic Event: User visited the Home Dashboard.")
            content = """
                <div class="card-grid">
                    <div class="card">
                        <h3>Server Uptime</h3>
                        <div class="value">99.98%</div>
                        <span style="color: #059669; font-size: 14px; font-weight: 500;">↑ System Stable</span>
                    </div>
                    <div class="card">
                        <h3>Active Connections</h3>
                        <div class="value">1,243</div>
                        <span style="color: #059669; font-size: 14px; font-weight: 500;">↑ Normal Traffic</span>
                    </div>
                    <div class="card">
                        <h3>CPU Load</h3>
                        <div class="value">14.2%</div>
                        <span style="color: #64748b; font-size: 14px;">Optimal</span>
                    </div>
                </div>
            """
            self.send_html_response(get_html_template("Dashboard Overview", content))

        # 2. USERS PAGE
        elif self.path == '/users':
            logging.info("Traffic Event: User loaded the User Directory.")
            content = """
                <div class="card">
                    <table>
                        <tr><th>Name</th><th>Email Address</th><th>Role</th><th>Status</th></tr>
                        <tr><td>Alice Smith</td><td>alice.s@company.internal</td><td>Administrator</td><td><span class="status-active">Active</span></td></tr>
                        <tr><td>Robert Chen</td><td>robert.c@company.internal</td><td>Developer</td><td><span class="status-active">Active</span></td></tr>
                        <tr><td>Maria Garcia</td><td>maria.g@company.internal</td><td>Data Analyst</td><td><span class="status-active">Active</span></td></tr>
                        <tr><td>James Wilson</td><td>james.w@company.internal</td><td>Viewer</td><td><span class="status-active">Active</span></td></tr>
                    </table>
                </div>
            """
            self.send_html_response(get_html_template("User Management", content))

        # 3. ANALYTICS PAGE
        elif self.path == '/analytics':
            logging.info("Traffic Event: User requested Analytics data.")
            content = """
                <div class="card">
                    <h3>Database Performance</h3>
                    <p style="color: #475569; line-height: 1.6;">Average query latency is currently 42ms. No bottlenecks detected in the last 24 hours. Cache hit ratio is stable at 89%.</p>
                </div>
            """
            self.send_html_response(get_html_template("System Analytics", content))

        # 4. SETTINGS PAGE (The realistic trap!)
        elif self.path == '/settings':
            logging.info("Traffic Event: User accessed the Settings panel.")
            content = """
                <div class="card">
                    <div class="setting-row">
                        <div class="setting-info">
                            <strong>Automated Cloud Backups</strong>
                            <p>Daily synchronization to AWS S3 storage.</p>
                        </div>
                        <button class="btn btn-primary">Enabled</button>
                    </div>
                    <div class="setting-row">
                        <div class="setting-info">
                            <strong>Maintenance Mode</strong>
                            <p>Take the application offline and show a holding page to users.</p>
                        </div>
                        <button class="btn">Disabled</button>
                    </div>
                    <div class="setting-row">
                        <div class="setting-info">
                            <strong>Clear Memory Cache</strong>
                            <p>Flushes temporary Redis data to free up server RAM.</p>
                        </div>
                        <a href="/crash" class="btn btn-danger-outline">Purge Cache</a>
                    </div>
                </div>
            """
            self.send_html_response(get_html_template("Server Configuration", content))

        # 5. THE CRASH ROUTE
        elif self.path == '/crash':
            logging.critical("CRITICAL - FATAL EXCEPTION: Memory overload! System crashing now!")
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(CRASH_HTML.encode('utf-8'))
            sys.exit(1) 

        # 404 CATCH-ALL
        else:
            logging.warning(f"404 Warning: User tried to access missing page: {self.path}")
            self.send_response(404)
            self.end_headers()

    def send_html_response(self, html_string):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_string.encode('utf-8'))

# Start the server
server = HTTPServer(('0.0.0.0', 8000), MyHandler)
logging.info("Web Application Booted Successfully on port 8000.")
server.serve_forever()
