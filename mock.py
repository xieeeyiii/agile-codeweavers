from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# 模拟接口数据
map_data = {"layout": [[1,1,1],[1,0,1],[1,1,1]]}
player_status = {"hp": 100, "bag": ["钥匙"]}

class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        if "/api/map" in self.path:
            self.wfile.write(json.dumps(map_data).encode())
        elif "/api/player/status" in self.path:
            self.wfile.write(json.dumps(player_status).encode())

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"result": "success"}).encode())

# 启动服务
server = HTTPServer(("localhost", 4010), MockHandler)
print("Mock 服务运行: http://localhost:4010")
server.serve_forever()