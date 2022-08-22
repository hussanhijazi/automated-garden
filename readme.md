$ pip install esptool
Using esptool.py you can erase the flash with the command:

$ esptool.py --port /dev/ttyUSB0 erase_flash
And then deploy the new firmware using:

esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20170108-v1.8.7.bin
$ ampy --port /dev/ttyUSB0 ls               

$ picocom

https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/
https://www.hackster.io/HARGOVIND/nodemcu-based-iot-project-connecting-yl-69-yl-38-moisture-7cf84a
https://randomnerdtutorials.com/esp32-esp8266-analog-readings-micropython/
https://www.ardumotive.com/how-to-use-the-raindrops-sensor-moduleen.html
https://www.youtube.com/watch?v=x219R5rzRtU 
