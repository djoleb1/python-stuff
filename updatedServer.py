from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

students_dict ={'1':['John','Doe','8.9'],'2':['Jane','Doe','8.0'],'3':['Bart','Simpson','9.1'],'4':['Homer','Simpson','5.0']}

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.log_message('Incoming GET request...')
        try:  
            student_index=parse_qs(self.path[2:])['index'][0]
        except:
            self.send_response_to_client(404,'Incorrect parameters provided')
            self.log_message('Incorrect parameters provided')
            return
        if student_index in students_dict:
            self.send_response_to_client(200,students_dict[student_index])
        else:
            self.send_response_to_client(400,'Index not found')
            self.log_message('Index not found')

    def do_POST(self):
        self.log_message('Incoming POST request...')
        data=parse_qs(self.path[2:])
        try:
            
            #students_dict[data['index'][0]]=[data['name'][0],data['last_name'][0],data['city'][0]]
            students_dict[data['index'][0]]=[data['name'][0],data['last_name'][0],data['grade'][0]]
            self.send_response_to_client(200,students_dict)
        except KeyError:
            self.send_response_to_client(404,'Incorrect parameters provided')
            self.log_message('Incorrect parameters provided')

    def send_response_to_client(self,status_code,data):
        self.send_response(status_code)
        self.send_header('Content-type','text/plain')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()

        self.wfile.write(str(data).encode())

server_address=('127.0.0.1', 8080)
http_server=HTTPServer(server_address,RequestHandler)
http_server.serve_forever()