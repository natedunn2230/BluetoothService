
import time
import os
from bluetooth import *
import json


def modify_wpa_sup(ssid, psk):
	current_cred = '';

	file_path = '/etc/wpa_supplicant/wpa_supplicant.conf'

	with open(file_path, 'r') as f:
		current_cred =  f.readlines()
		f.close()

	found_network = False
	out_file = []
	for line in current_cred:
		current_line = line.strip()
		if current_line.startswith('ssid'):
			line = '\tssid="{}"\n'.format(ssid)
		elif current_line.startswith('psk'):
			line = '\tpsk="{}"\n'.format(psk)
		elif current_line.startswith('network'):
			found_network = True
		
		out_file.append(line)

	if not found_network:
		print('no network configurations found yet. Creating default network...')
		
		out_file = ['country=us\n', 'update_config=1\n', 'ctrl_interface=/var/run/wpa_supplicant\n\n', 
		'network={\n', '\tssid="{}"\n\tpsk="{}"\n'.format(ssid, psk), '}\n']

	with open(file_path, 'w') as f:
		for line in out_file:
			f.write(line)
		f.close()

	os.system("wpa_cli -i wlan0 reconfigure")


## Make device discoverable before setting up a server
os.system("sudo hciconfig hci0 piscan")
os.system("sudo hciconfig hci0 name 'Intellisert'")

while True:
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service( server_sock, "AquaPiServer",
                    service_id = uuid,
                    service_classes = [ uuid, SERIAL_PORT_CLASS ],
                    profiles = [ SERIAL_PORT_PROFILE ])
    print("waiting for connection....")

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)
    try:
        while True:
                        
            # response back to client will be in format {"success": bool, "msg": string}
            response = '{"success": true, "message": "successful config"}'
            
            ssid = '';
            password = '';

            data = client_sock.recv(1024)
            if not data:
                break
            
            #data will be in format {"ssid": string, "key": string}
            jsonData  = json.loads(data)
                        
            # parse data keys
            if 'ssid' and 'key' in jsonData:
                ssid = jsonData['ssid']
                password = jsonData['key']
				
                ## modify the wpa_supplicant file to hold new network changes
                modify_wpa_sup(ssid, password)
            else:
                response = '{"success": false, "message": "parameters ssid and key required"}'
					
        client_sock.send(response)
            
    except OSError as e:
        print(e)
        pass
    except BluetoothError as e:
        print(e)
        pass

    print("disconnected")

    client_sock.close()
    server_sock.close()



