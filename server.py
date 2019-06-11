#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import sys
import os
import socketserver

if len(sys.argv) == 4:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    fich_audio = sys.argv[3]

else:
    sys.exit("Usage: python3 server.py IP port audio_file")

class EchoHandler(socketserver.DatagramRequestHandler):
    """ Echo server class """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion")
          while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            linea_decod = line.decode('utf-8').split(" ")
            if (len(linea_decod) != 3 or 'sip:' not in linea_decod[1] or
                    '@' not in linea_decod[1] or
                    'SIP/2.0\r\n\r\n' not in linea_decod[2]):
                        self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
                        break
            metodo = linea_decod[0]
            if metodo == 'INVITE':
                self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n"
                                 + b"SIP/2.0 180 Ringing\r\n\r\n"
                                 + b"SIP/2.0 200 OK\r\n\r\n")
            if metodo == 'ACK':
                ejecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + sys.argv[3]
                print("Vamos a ejecutar", ejecutar)
                os.system(ejecutar)
                self.wfile.write(b"cancion.mp3 enviada")
                break
            if metodo == 'BYE':
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                break
            if method not in ['INVITE', 'BYE', 'ACK']:
                self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n')
                break
            if not line:

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((IP, PORT), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
