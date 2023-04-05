import sys
from http.server import HTTPServer, BaseHTTPRequestHandler;
import MolDisplay
import molsql
import urllib
import json
import io

public_files = ['/style.css', '/script.js', '/index.html', '/add-molecules.html', '/add-molecules.js', '/view-molecules.html', '/add-elements.html', '/add-elements.js', '/view-elements.html', '/view-elements.js', '/elements.json', '/logo.png']

# Subclass of BaseHTTPRequestHandler, used to run python webserver
class MyHandler(BaseHTTPRequestHandler):

    db = molsql.Database(False)
    db.create_tables()

    # Presents the web-form
    def do_GET(self):
        # Display of web-page
        if self.path in public_files:
            self.send_response(200) 

            if self.path.endswith(".html"):
                self.send_header("Content-type", "text/html")

                fp = open (self.path[1:])
                page = fp.read()
                fp.close()

                self.send_header("Content-length", len(page))
                self.end_headers()

                self.wfile.write(bytes(page, "utf-8"))

            elif self.path.endswith(".js"):
                self.send_header("Content-type", "text/javascript")

                script = open (self.path[1:], "rb")
                script_data = script.read()
                script.close()

                self.send_header("Content-length", len(script_data))
                self.end_headers()

                self.wfile.write(bytes(script_data))

            elif self.path.endswith(".json"):
                self.send_header("Content-type", "application/json")

                script = open (self.path[1:], "rb")
                script_data = script.read()
                script.close()

                self.send_header("Content-length", len(script_data))
                self.end_headers()

                self.wfile.write(bytes(script_data))

            elif self.path.endswith(".png"):
                self.send_header("Content-type", "image/png")

                image = open (self.path[1:], "rb")
                image_data = image.read()
                image.close()

                self.send_header("Content-length", len(image_data))
                self.end_headers()

                self.wfile.write(bytes(image_data))


                # elements_file = open("elements.json", "w")
                # elements_file.write(table)
                # elements_file.close()

        elif self.path == "/add-elements-to-table.html":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')

            self.end_headers()

            cursor = self.db.conn.cursor()
            cursor.execute(f'''SELECT * FROM ELEMENTS;''')
            elements = cursor.fetchall()

            # table = '[\n'
            # for i in elements:
            #     table += ('\t{')
            #     table += (f'"number":{i[0]}, "code":"{i[1]}", "name":"{i[2]}", "color1":"#{i[3]}", "color2":"#{i[4]}", "color3":"#{i[5]}", "radius":{i[6]}')
            #     table += ('},\n')
            # table += (']')

            # print (table)

            current_dict = []

            for i in elements:
                current_dict.append({'number': i[0], 'code': i[1], 'name': i[2], 'color1': f'#{i[3]}', 'color2': f'#{i[4]}', 'color3': f'#{i[5]}', 'radius': i[6]})
                #self.wfile.writelines(json.dumps({"number":i[0], "code":i[1], "name":i[2], "color1":f'#{i[3]}', "color2":f'#{i[4]}', "color3":f'#{i[5]}', "radius":i[6]}))

            print(current_dict)
            json_dict = json.dumps(current_dict).encode()
            self.wfile.write(json_dict)
            self.send_header('Content-length', len(json_dict))


        else:
            # 404 error
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))

    # Sends an svg file to the client
    def do_POST(self):
        if self.path == "/molecule-add-handler.html":
            header_read = self.rfile.read(int(self.headers['content-length']))

            postvars = urllib.parse.parse_qs(header_read.decode('utf-8'))
            
            self.db.add_molecule(postvars.get('name')[0], io.StringIO(postvars.get('file')[0]))

        elif self.path == "/element-add-handler.html":
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length)

            postvars = urllib.parse.parse_qs(body.decode('utf-8'))
            
            self.db['Elements'] = (int(postvars.get('number')[0]), postvars.get('code')[0], postvars.get('name')[0], postvars.get('color1')[0][1:], postvars.get('color2')[0][1:], postvars.get('color3')[0][1:], int(postvars.get('radius')[0]))

        elif self.path == "/delete-element.html":
            header_read = self.rfile.read(int(self.headers['content-length']))

            postvars = urllib.parse.parse_qs(header_read.decode('utf-8'))
            element_id = postvars.get('mol_id')[0]

            self.db.conn.execute(f'''DELETE FROM Elements
                                    WHERE ELEMENT_NO={element_id}''')

        else:
            # 404 error
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes("404: not found", "utf-8"))


httpd = HTTPServer(('localhost', int(sys.argv[1])), MyHandler)

# Try except statement is to get rid of the messy message that shows
# when the user uses Ctrl+C to shut down the webserver
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print('')

httpd.server_close()
