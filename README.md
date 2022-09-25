# pi-tide

Project to fetch and display high tide info onto a sh1106 display on a pi zero w, based on [luma.oled.device](https://luma-oled.readthedocs.io/en/latest)

currently shows from a json data sheet
have the source as pdf, need to get more data in

## todos

- check date every 10mins, if different refetch the data
- get more data in (google sheet save as csv, use convert to json add-on in vscode)
- run on startup automatically as service without mac triggering - done I think
- have a button to go forward by day
- have a button to go back by day
- then have a button to go to todays date
- expose the sunrise/sunset data if we want
- could add weather on a display toggle button if we wanted

## steps to make service

have created a systemd service in root but file specifies to run as pi user
which was the user where pip3 python commands were run and the python files exist

- `sudo loginctl enable-linger pi`
- `nano /etc/systemd/system/pi-tide.service`

### /etc/systemd/system/pi-tide.service

```
[Unit]
Description=Display tide times for Newquay
After=multi-user.target

[Service]
Type=simple
WorkingDirectory=/home/pi/development/pi-tide
ExecStart=/usr/bin/python3 /home/pi/development/pi-tide/main.py --autologin pi %I
Restart=on-abort
User=pi

[Install]
WantedBy=multi-user.target
```

- `chmod 644 /etc/systemd/system/pi-tide.service`
- `chmod +x ~/development/pi-tide/main.py`

- `systemctl daemon-reload`
- `systemctl enable pi-tide`
- `systemctl start --pi pi-tide`

see https://askubuntu.com/questions/676007/how-do-i-make-my-systemd-service-run-via-specific-user-and-start-on-boot

and

https://github.com/thagrol/Guides/blob/main/boot.pdf

also for auto login pi user use `sudo raspi-config` under system boot can select autologin console
