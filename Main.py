from mcstatus import JavaServer
import threading

from Mysql import *
from Log import Log



#last ip scanned: 104.247.114.12
continue_scanning = True
starting_ip = "116.202.0.0"
ending_ip = "_._.205.255"




class Main:

    def __init__(self, continue_scanning, starting_ip, ending_ip):
        #init mysql connection
        logins = open('../database-login.txt', 'r').readlines()[0].split(';')
        self.connection = create_connection(logins[0], logins[1], logins[2], logins[3])
        if self.connection is None:
            Log.print("Connection failed")
            raise Exception("Connection failed")
        
        #init ip
        if continue_scanning:
            self.ip = open("last_ip_scanned.txt", "r").read()
        else:
            self.ip = starting_ip
        
        split_ip = ending_ip.split(".")
        for i in range(len(split_ip)):
            if split_ip[i] == "_":
                split_ip[i] = starting_ip.split(".")[i]
        ending_ip = ".".join(split_ip)
    
    def run(self):
        run = True
        while run:

            if self.ip == ending_ip:
                run = False
                Log.print("Scanning finished")
            else:
                self.ip = Main.add_ip(self.ip)

            server = JavaServer(self.ip, 25565)
            Log.print("Scanned IP: " + self.ip)
            open("last_ip_scanned.txt", "w").write(self.ip)
            try:
                status = server.status()
            except:
                Log.print("Server not found")
                continue

            Log.print("version : " + status.version.name)
            Log.print("description : " + status.description)
            Log.print("ping : " + str(status.latency))

            self.add_to_database(status)
    
    def scan_ip(self, ip):
        server = JavaServer(ip, 25565)
        Log.print("Scanned IP: " + ip)
        open("last_ip_scanned.txt", "w").write(ip)
        try:
            status = server.status()
        except:
            Log.print("Server not found")
            return

        Log.print("version : " + status.version.name)
        Log.print("description : " + status.description)
        Log.print("ping : " + str(status.latency))

        self.add_to_database(status)
    
    def add_to_database(self, status):
        version = injection_protection(status.version.name)
        description = injection_protection(status.description)
        query = f"INSERT INTO servers_found (ip, version, description) VALUES ('{self.ip}', '{version}', '{description}')"
        execute_query(self.connection, query)
    
    @staticmethod
    def add_ip(ip, add=1):
        ip = ip.split(".")

        if int(ip[3]) + add <= 255:
            ip[3] = str(int(ip[3]) + add)
            return ".".join(ip)
        
        if int(ip[2]) + add <= 255:
            ip[2] = str(int(ip[2]) + add)
            ip[3] = "0"
            return ".".join(ip)
        
        if int(ip[1]) + add <= 255:
            ip[1] = str(int(ip[1]) + add)
            ip[2] = "0"
            ip[3] = "0"
            return ".".join(ip)
        
        if int(ip[0]) + add <= 255:
            ip[0] = str(int(ip[0]) + add)
            ip[1] = "0"
            ip[2] = "0"
            ip[3] = "0"
            return ".".join(ip)
    
    def start_thread(self, ip):
        t = threading.Thread(target=self.scan_ip, args=(ip,))
        t.start()

if __name__ == "__main__":
    Main(continue_scanning, starting_ip, ending_ip).run()