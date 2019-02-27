#Сервер Франкенштейн
import asyncio
import json
METRICS = {} 

class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = data.decode()
        method, metrics = resp.split(' ', 1)
        metrics = list(metrics[:-1].split(' '))
        if method == 'put':
            answer = put(metrics)
        elif method == 'get':
            answer = get(metrics) 
        else:
            answer = 'error\nwrong command\n\n'
        self.transport.write(answer.encode())

def put(metrics):
    key = metrics[0]
    value = metrics[1]
    timestamp = metrics[2]
    print(key, value, timestamp)
    if key not in METRICS:
        METRICS[key] = []
        METRICS[key].append((timestamp, value))
    else:
        data = METRICS[key]
        print(data, type(data))
        i = 0
        while i < len(data):
            print(timestamp, data[i][0])
            print(value, data[i][1])
            if timestamp == data[i][0] and value == data[i][1]:
                uzhe = True
            else:
                uzhe = False
            i += 1
        if uzhe:
            pass
        else:
            METRICS[key].append((timestamp, value))
    print(METRICS)
    return 'ok\n\n'

def get(key):
    if key[0] == '*':
        ans2 = ''
        for key in METRICS.keys():
            data = METRICS.get(key)
            print(key)
            i, ans1 = 0, ''
            while i < len(data):
                timestamp, value = data[i][0], data[i][1]
                ans = key + ' ' + value + ' ' + timestamp + '\n'
                i += 1
                ans1 += ans
            ans2 +=  ans1
            print(ans2)
        ans = 'ok\n' + ans2 +'\n'
        print(ans)
    else:
        data = METRICS.get(key[0])
        i, ans1 = 0, ''
        if data:
            while i < len(data):
                timestamp, value = data[i][0], data[i][1]
                ans = key[0] + ' ' + value + ' ' + timestamp + '\n'
                ans1 += ans
                i+=1
            ans = 'ok\n' + ans1 +'\n'
        else:
            ans = 'ok\n\n'
    return ans 


def run_server(host='127.0.0.1', port=8888):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == '__main__':
    run_server()
