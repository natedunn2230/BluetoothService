
import time
import os
from bluetooth import *
import json

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
					   profiles = [ SERIAL_PORT_PROFILE ], 
	#                   protocols = [ OBEX_UUID ] 
						)
	print("waiting for connection....")

	client_sock, client_info = server_sock.accept()
	print("Accepted connection from", client_info)
	try:
		while True:
			data = client_sock.recv(1024)
			if not data:
				break
			print("Received", data)
			#data will be in format {ssid: ..., key...}
			parsedData = json.loads(data)
			print("ssid: " + parsedData['ssid'])
			print("password: " + parsedData['key'])
			client_sock.send(data)
	except OSError as e:
		print(e)
		pass
	except BluetoothError as e:
		print(e)
		pass

	print("disconnected")

	client_sock.close()
	server_sock.close()



