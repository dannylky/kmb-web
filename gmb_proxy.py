#!/usr/bin/env python3
"""GMB CORS Proxy — forwards to data.etagmb.gov.hk with CORS headers."""
import sys, json, http.server, urllib.request, urllib.error, gzip

GMB_BASE = "https://data.etagmb.gov.hk"

class Pxy(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.cors(); self.send_response(200); self.end_headers()
    def do_GET(self):
        u = GMB_BASE + self.path
        try:
            req = urllib.request.Request(u, headers={"Origin":"http://localhost","User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                ct = r.headers.get("Content-Type","application/json")
                d = r.read()
                if "gzip" in r.headers.get("Content-Encoding",""): d = gzip.decompress(d)
            self.send_response(200); self.cors()
            self.send_header("Content-Type",ct); self.send_header("Content-Length",str(len(d)))
            self.end_headers(); self.wfile.write(d)
        except urllib.error.HTTPError as e:
            self.send_response(e.code); self.cors(); self.end_headers()
        except Exception as e:
            self.send_response(500); self.cors()
            self.send_header("Content-Type","application/json"); self.end_headers()
            self.wfile.write(json.dumps({"error":str(e),"path":self.path}).encode())
    def cors(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","GET,OPTIONS")
        self.send_header("Access-Control-Allow-Headers","*")
    def log_message(self,fmt,*a):
        print(f"[GMB] {a[0]} {a[1]} -> {a[2]}")

if __name__ == "__main__":
    p = int(sys.argv[1]) if len(sys.argv)>1 else 8899
    h = http.server.HTTPServer(("0.0.0.0",p),Pxy)
    print(f"GMB CORS Proxy @ http://localhost:{p}")
    h.serve_forever()
