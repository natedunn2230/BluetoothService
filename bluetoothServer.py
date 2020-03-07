import time
import os
import sys
import subprocess
from bluetooth import *
import json

## Make device discoverable before setting up a server
os.system("sudo hciconfig hci0 piscan")
os.system("sudo hciconfig hci0 name 'Intellisert'")


def very_connection():
	iw_sub = subprocess.Popen(["iwconfig"], stdout=subprocess.PIPE)

	iw_sub.wait()

	(out, err) = iw_sub.communicate()
	essid_idx = out.find("ESSID")
	essid_idx += 6

	return out[essid_idx] == '"'

def modify_wpa_sup(ssid, psk, socket):
	"""
		Modifies the Wireless network's credentials in the wpa_supplicant file. The
		service is then reconfigured to accept the new changes
	"""
	print('attempting to connect to network: {}'.format(ssid))

	WPA_SUP_PATH = '/etc/wpa_supplicant/wpa_supplicant.conf'

	## new information to be passed to the WPA_SUP file
	out_file = ['country=us\n', 'update_config=1\n', 'ctrl_interface=/var/run/wpa_supplicant\n\n', 
	'network={\n', '\tssid="{}"\n\tpsk="{}"\n'.format(ssid, psk), '}\n']

	# write this information to the WPA_SUP file
	with open(WPA_SUP_PATH, 'w') as f:
		for line in out_file:
			f.write(line)
		f.close()
	
	# restart the wlan0 interface to connect to new network and block the rest of the program to wait on result
	sub_proc = subprocess.Popen(["wpa_cli", "-i",  "wlan0", "reconfigure"], stdout=subprocess.PIPE)
	sub_proc.wait()
	time.sleep(10)
	
	(out, err) = sub_proc.communicate()


        if very_connection() and out == 'OK\n':
		return True
	else:
		return False


while True:
	try:
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

		while True:
						
			# response back to client will be in format {"success": bool, "msg": string}
			response = ''
			
			ssid = '';
			password = '';

			data = client_sock.recv(1024)
			if not data:
				break
			
			#data will be in format {"ssid": string, "key": string}
			jsonData  = json.loads(data)
						
			# parse data keys
			try:
				ssid = jsonData['ssid']
				password = jsonData['key']
				
				## modify the wpa_supplicant file to hold new network changes
				wpa_result = modify_wpa_sup(ssid, password, client_sock)
				
				if not wpa_result:
                                        print('Could not connect to network')
					response = '{"success": false, "message": "could not connect to specified network"}'
				else:
                                        print('Connected to network')
					response = '{"success": true, "message": "successfully connected to network"}'
					
			except KeyError as e:
				response = '{"success": false, "message": "parameters ssid and key required"}'

			client_sock.send(response)
	except BluetoothError as e:
		print(e)
	except OSError as e:
		print(e)
	except Exception as e:
		print(e)
	except KeyboardInterrupt as e:
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)

	print("disconnected")

	client_sock.close()
	server_sock.close()
