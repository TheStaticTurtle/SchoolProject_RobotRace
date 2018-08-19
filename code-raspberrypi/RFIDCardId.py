import serial,time

ser = serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

while True:
	line = ser.readline()
	if line:
		rawResponce = line[:-1]
		splitResponce = rawResponce.split(":")
		rawCode = splitResponce[1]
		print "+"+rawCode+"+"
