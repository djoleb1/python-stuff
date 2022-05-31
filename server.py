from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
names_dict = [{'id':'1','name':'john','surname':'doe','avg_grade':'7.1'},
                {'id':'2','name':'mike','surname':'dane','avg_grade':'8.0'},
                {'id':'3','name':'jane','surname':'doe','avg_grade':'9.0'}]
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.log_message("Incoming GET request...")
        try:
            id = parse_qs(self.path[2:])['name'][0]
            id = int(id)
            ind = id-1
        except:
            self.send_response_to_client(404, 'Incorrect parameters provided')
            self.log_message("Incorrect parameters provided")
            return
        if int(id) <= len(names_dict):
            self.send_response_to_client(200, names_dict[ind])
            self.log_message("GET method was successful")
        else:
            self.send_response_to_client(400, 'Name not found')
            self.log_message("Name not found")
     
    def do_POST(self):
        self.log_message('Incoming POST request...')
        data = parse_qs(self.path[2:])
        try:
            names_dict[data['name'][0]] = data['last_name'][0]
            self.send_response_to_client(200, names_dict)
        except KeyError:
            self.send_response_to_client(404, 'Incorrect parameters provided')
            self.log_message("Incorrect parameters provided")
             
    def send_response_to_client(self, status_code, data):
        # Send OK status
        self.send_response(status_code)
        # Send headers
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
     
        # Send the response
        self.wfile.write(str(data).encode())
 
server_address = ('127.0.0.1', 8080)
http_server = HTTPServer(server_address, RequestHandler)
http_server.serve_forever()
