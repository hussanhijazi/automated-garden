## Install esptool
```$ pip install esptool```

## Erase the entire flash using
```$ esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash```

## And then deploy the new firmware using
```$ esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20220618-v1.19.1.bin```

## Install Ampy
```$ pip install adafruit-ampy```

## Use Ampy to list files
```$ ampy --port /dev/ttyUSB0 ls```             

## Picocom
```$ picocom /dev/ttyUSB0``` 

https://randomnerdtutorials.com/esp8266-pinout-reference-gpios/
https://www.hackster.io/HARGOVIND/nodemcu-based-iot-project-connecting-yl-69-yl-38-moisture-7cf84a
https://randomnerdtutorials.com/esp32-esp8266-analog-readings-micropython/
https://www.ardumotive.com/how-to-use-the-raindrops-sensor-moduleen.html
https://www.youtube.com/watch?v=x219R5rzRtU 
