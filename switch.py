import smbus
import time

__bus__ = None

def setupio(busid,i2caddress):
	global __bus__
	__bus__ = smbus.SMBus(busid)
	address = i2caddress
	__bus__.write_byte_data(address,0x00,0x00)
	__bus__.write_byte_data(address,0x01,0x00)
	__bus__.write_byte_data(address,0x12,255)
	__bus__.write_byte_data(address,0x13,255)

def operatepoint(i2caddress, bank, iopin):
	global __bus__
	iopin = 255 - iopin
	__bus__.write_byte_data(i2caddress,bank,iopin)
	time.sleep(0.1)
	__bus__.write_byte_data(i2caddress,bank,255)
