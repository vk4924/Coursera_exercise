import socket
import time


class ClientError(Exception):
    pass
    
class Client:
    def __init__(self, host, port, timeout=None ):
        try:
            self.sock = socket.create_connection((host, port), timeout)
        except socket.timeout:
            print('send data timeout')
        except socket.error as ex:
            print('send data error:', ex)

    def read(self):
        data = b''
        while not data.endswith(b'\n\n'):
            data += self.sock.recv(1024)            
        answer, results = data.decode().split('\n', 1)
        if answer == 'error':
            raise ClientError('send data error')
        return results.strip()

    def put(self, key, value, timestamp=None):
        timestamp = timestamp or int(time.time())
        try:
            self.sock.sendall(
                    f'put {key} {value} {timestamp}\n'.encode('utf8')
                    )  
        except socket.error as err:
            raise ClientError('send data error:', err)
        self.read()
 
    def get(self, key):
        try:
            self.sock.sendall(
                    f'get {key}\n'.encode()
                    )
        except socket.error as err:
            raise ClientError('send data error:', err)

        results = self.read()
        data = {}
        if results == '':
            return data
        
        for row in results.split('\n'):
            key, value, timestamp = row.split()
            if key not in data:
                data[key] = []
            data[key].append((int(timestamp), float(value)))
        
        return data

if __name__=='__main__':
    client = Client('127.0.0.1', 8888)
    client.put("test", 0.5, timestamp=1)
    client.put("test", 2.0, timestamp=2)
    client.put("test", 0.5, timestamp=3)
    client.put("load", 3, timestamp=4)
    client.put("load", 4, timestamp=5)
    print(client.get("*"))
    print(client.get("load"))

