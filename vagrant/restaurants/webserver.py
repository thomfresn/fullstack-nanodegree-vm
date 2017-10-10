#Web server code using https://docs.python.org/2/library/basehttpserver.html

from http.server import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

import cgi

#Will process reauest from http://localhost:8080/hello
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html', )
                self.end_headers()
                output = ""
                output += "<html><body>"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += "<div>"
                    output += "<a href='editRestaurant'>"
                    output += restaurant.name
                    output += "</a>"
                    output += "</div>"
                output += "</body></html>"
                self.wfile.write(output.encode("utf-8"))
                print(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html', )
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Enter a new restaurant!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>New restaurant name</h2><input name="restaurantName" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output.encode("utf-8"))
                print(output)
                return

        except IOError:
            self.send_error(404, "File not found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                fields = cgi.parse_multipart(self.rfile, pdict)
                restaurantName = fields.get('restaurantName')[0].decode('utf-8')
                newRestaurant = Restaurant(name = restaurantName)
                session.add(newRestaurant)
                session.commit()

                output = ''
                output += '<html><body>'
                output += '<h2> New restaurant created: </h2>'
                output += '<h1> %s </h1>' % restaurantName
                output += '</html></body>'
                self.wfile.write(output.encode('utf-8'))
                print(output)
        except:
                pass

def main():
    try:
        port = 8080
        print("Starting web server")
        server = HTTPServer(('', port), webserverHandler)
        print("Web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, stopping web server ...")
        server.socker.close()

if __name__ == '__main__':
    main()
