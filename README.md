# BluetoothService
### CEG-4981
### Intellisert
### Group 14
Bluetooth service on device side to accept bluetooth requests

### Setup
1. Install necessary packages: `sudo apt-get install bluez bluez-tools python-bluez pi-bluetooth`
2. Add the following line to  /etc/bluetooth/main.conf: `DisablePlugins = pnat`
3. Under /lib/systemd/system/bluetooth.service, change *ExecStart=/usr/lib/bluetooth/bluetoothd* to *ExecStart=/usr/lib/bluetooth/bluetoothd **-C***
4. Restart the bluetooth system service: `sudo systemctl restart bluetooth`
5. run server: `sudo python path/to/bluetoothService.py`
   * If error occurs saying *no device found*, Restart Raspberry Pi device and then issue the command: `sudo systemctl start hciuart`
  
### Creating service for running on startup
* https://medium.com/@benmorel/creating-a-linux-service-with-systemd-611b5c8b91d6

### An adaptation and extension of bluetooth service from: http://blog.davidvassallo.me/2014/05/11/android-linux-raspberry-pi-bluetooth-communication/
