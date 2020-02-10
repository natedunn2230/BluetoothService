# BluetoothService
Bluetooth service for Intellisert Device

### Setup
1. Install necessary packages: `sudo apt-get install bluez python-bluez`
2. Add the following line to  /etc/bluetooth/main.conf: `DisablePlugins = pnat`
3. Under /lib/systemd/system/bluetooth.service, change *ExecStart=/usr/lib/bluetooth/bluetoothd* to *ExecStart=/usr/lib/bluetooth/bluetoothd **-C***
4. Restart the bluetooth system service: `sudo systemctl restart bluetooth`
4. run server: `sudo python path/to/bluetoothService.py`

### Thanks to http://blog.davidvassallo.me/2014/05/11/android-linux-raspberry-pi-bluetooth-communication/
