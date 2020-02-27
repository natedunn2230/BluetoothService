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
* Create File under /etc/systemd/system/{your-service-name.service}
* Enter the following contents:
```
    [Unit]
    Description=Bluetooth Service for Intellisert
    After=bluetooth.service
    StartLimitIntervalSec=0

    [Service]
    Type=simple
    Restart=always
    RestartSec=1
    User={your-user}
    ExecStart=/usr/bin/sudo /usr/bin/python /path/to/BluetoothService/bluetoothServer.py

    [Install]
    WantedBy=multi-user.target
```
* Enable service to start on boot: `sudo systemctl enable {your-service-name}`
* Start up the service: `sudo systemctl start {your-service-name}`
* Check status of the service: `sudo systemctl status {your-service-name}`

### An adaptation and extension of bluetooth service from: http://blog.davidvassallo.me/2014/05/11/android-linux-raspberry-pi-bluetooth-communication/
