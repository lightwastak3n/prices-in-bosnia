from turso_server import Server

server = Server()
conn = server.get_connection()
conn.sync()
