#WORKED
import socket, json, sys
hashrate_total, hashrate, accepted_shares, invalid_shares, miner_uptime, gpu_temp, gpu_fans = [],[],[],[],[],[],[]
api_command = "summary+devs"
api_ip = '192.168.1.21'
api_port = 4028
message = {"command": api_command}

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((api_ip,int(api_port)))
    s.sendall(bytes(json.dumps(message), 'utf-8'))
except Exception as e:
    raise

chunks = []
chunk = 1
try:
    while chunk:
        chunk = s.recv(4096)
        chunks.append(chunk)
except socket.error:
    traceback.print_exc()

s.close()
data = b''.join(chunks)
data = (json.loads(data))
#print(json.dumps(data, indent=4))

#hashrate_total = data['summary']['SUMMARY'][0]['MHS 30s']   #mh/s with 1 decimal
accepted_shares = data['summary']['SUMMARY'][0]['Accepted']
invalid_shares = data['summary']['SUMMARY'][0]['Rejected'] 
miner_uptime = data['summary']['SUMMARY'][0]['Elapsed'] #uptime in seconds

for i in range(0, len(data['devs']['DEVS'])):
    gpu_hashrate = data['devs']['DEVS'][i]['MHS 30s'] #mh/s
    agpu_fan = data['devs']['DEVS'][i]['Fan Percent'] 
    atemp = data['devs']['DEVS'][i]['Temperature'] 
    hashrate.append(gpu_hashrate)
    gpu_temp.append(atemp)
    gpu_fans.append(agpu_fan)
hashrate_total = sum(hashrate)  #mh/s with 2 decimals
