from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from collections import defaultdict
from pubsub_db import add_to_database, download_from_database
from pubsub_broker import broker_publish
import time

def prepare_command_for_broker(payload):
    document = dict()
    payload = defaultdict(lambda: None, payload)
    time = payload['timestamp'][0].split(".")[0]
    document.update({"timestamp" : time,"device_id" : payload['device_id'][0]})
    if payload['lights'] != None:
        document.update({"lights" : payload['lights'][0]})
    if payload['heating'] != None:
        document.update({"heating" : payload['heating'][0]})
    return str(document)

class PostHandlerBroker(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, topic, broker_ip, broker_port, username, password):
        self.topic = topic
        self.broker_ip = broker_ip
        self.broker_port = broker_port
        self.username = username
        self.password = password
        super().__init__(request, client_address, server)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(post_data)
        parsed_data = parse_qs(post_data.decode('utf-8'))
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'POST request received')
        document = prepare_command_for_broker(parsed_data)
        print(document)
        broker_publish(document, self.topic, self.broker_ip, self.broker_port, self.username, self.password)

class PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(post_data)
        parsed_data = parse_qs(post_data.decode('utf-8'))
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'POST request received')
        
        print(parsed_data)

def start_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, PostHandler)
    print('Server running on port', port)
    httpd.serve_forever()

def server_to_broker_init(port, topic, broker_ip, broker_port, username, password):
    server_address = ('', port)
    httpd = HTTPServer(server_address, lambda request, client_address, server: PostHandlerBroker(request, client_address, server, topic, broker_ip, broker_port, username, password))
    print('Server running on port', port)
    return httpd

def server_to_broker_loop(httpd):
    httpd.serve_forever()

def server_to_broker(port, topic, broker_ip, broker_port, username, password):   
    server_address = ('', port)
    httpd = HTTPServer(server_address, lambda request, client_address, server: PostHandlerBroker(request, client_address, server, topic, broker_ip, broker_port, username, password))
    print('Server running on port', port)
    httpd.serve_forever()