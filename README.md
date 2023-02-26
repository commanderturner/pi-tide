# pi-tide

Project to fetch and display high tide info onto a sh1106 display on a pi zero w, based on [luma.oled.device](https://luma-oled.readthedocs.io/en/latest)

currently shows from a json data sheet
have the source as pdf, need to get more data in

## Steps

- [download raspberry pi imager](https://www.raspberrypi.com/software/)
- select from "Raspberry Pi OS (Other)" `Raspberry Pi OS Lite (32 bit)`
- install onto SD Card
- make a `wpa_supplicant.conf` file filled in with your wifi credentials and copy it to the boot of the sd card. This will ensure on first boot you can acess your pizero via another computers terminal.
- we added ssh keys for passwordless access that then enabled the `deploy_all.sh` and `deploy_code.sh` scripts to be able to run to quickly copy code changes across to the pi. Alas we could not test on the development computer because it didn't have pins etc.
- access the booted up pi zero via a terminal session
- make directories for code to sit in

  - `mkdir development`
  - `mkdir development/pi-tide`
  - `mkdir development/pi-tide/fonts`
  - `mkdir development/pi-tide/data`

- install python 3 (various online guides to do this)

## dependencies

requires following libraries to be installed:

## display

- luma.core.interface.serial
- luma.core.render
- luma.oled.device
- PIL (pillow)

- `pip3 install luma.core`
- `pip3 install luma.oled`
- `sudo apt-get install python3 python3-pip python3-pil libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7 libtiff5 -y`
- `sudo apt-get install python3-pil`

## steps to run code once copied to the pi

- `cd development/pi-tide`
- `python3 main.py`

the screen should output stuff now and the button should toggle the display

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

## Pins

see pi-zero-w-gpio-pinout.png

### Display 1.3" OLED IIC

| pin # | cable colour | usage      | destination |
| ----- | ------------ | ---------- | ----------- |
| 01    | red          | 3.3V power | VCC         |
| 03    | yellow       | data       | SDA         |
| 05    | orange       | clock      | SCL         |
| 06    | brown        | ground     | GND         |

### Button

| pin # | cable colour | usage            | destination               |
| ----- | ------------ | ---------------- | ------------------------- |
| 09    | black        | ground           | either of 2 connectors    |
| 11    | green        | GPIO signal (17) | the other of 2 connectors |

## The data

We sourced a pdf from [TideTimes.org.uk](TideTimes.org.uk) for Perranporth tide times for 2023. Alas it wasn't in a format we could automatically import. There was a site with an api that could get the data in a format we could consume directly, however there was a cost associated with this per search.

### adding data to the spreadsheet

We have a google sheets set up with the following 11 columns (plus example row)
| date | low_1_time | low_1_height_m |low_2_time |low_2_height_m | high_1_time | high_1_height_m | high_2_time |high_2_height_m | sunrise | sunset
-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----
2022-09-24|11:24|1.38|23:47|1.13|05:08|6.35|17:22|6.67|07:09|19:14
2022-09-25|11:56|1.06| | |05:40|6.65|17:53|6.92|07:11|19:12
2022-09-26|00:18|0.89|12:28|0.84|06:12|6.88|18:25|7.09|07:12|19:10
2022-09-27|00:49|0.74|13:01|0.72|06:44|7.02|18:58|7.17|07:14|19:08
2022-09-28|01:23|0.7|13:36|0.73|07:16|7.05|19:33|7.14|07:15|19:05

we export as csv into this data folder

then an extension in VSCode (called _"Convert CSV to JSON"_) allows us convert this into a JSON file that python can read from (we do have to do a find/replace on a strange "\r" character code added to the last property of each JSON object, essentially we remove that before saving the file)

## todos

- get more data in (google sheet save as csv, use convert to json add-on in vscode)
