#!/usr/bin/env python
import web
import switch
import json

urls = (
	'/sw/(.*)', 'sw',
	'/api/open/(\d+)', 'open',
	'/api/close/(\d+)', 'close',
	'/(.*)', 'hello'
)

app = web.application(urls, globals())
render = web.template.render('templates/')
db = web.database(dbn='sqlite', db='railcontroldb')

try:
	switch.setupio(1,0x20)
	devpresent = True
except IOError:
	devpresent = False

class sw:
	def GET(self, iopin):
		if not iopin:
			iopin = '1'
		iopinint = int(iopin)
		if devpresent:
			switch.operatepoint(0x20,0x12,iopinint)
		return render.swtpl(iopin)

class open:
	def GET(self, motorid):
		try:
			motor = db.select('pointmotors', where="id=$motorid", vars=locals())[0]
		
			if devpresent:
				switch.operatepoint(motor.i2caddress,motor.i2cbank,motor.openiopin)

			pyDict = {'motorid':motor.id, 'openiopin':motor.openiopin, 'closeiopin':motor.closeiopin,'i2caddress':motor.i2caddress,'i2cbank':motor.i2cbank,'state':'open'}

			web.header('Content-Type', 'application/json')
			return json.dumps(pyDict)
		except IndexError:
			pyDict = {'error':'No such motor found'}

			web.header('Content-Type', 'application/json')
			return json.dumps(pyDict)

class close:
	def GET(self, motorid):
		try:
			motor = db.select('pointmotors', where="id=$motorid", vars=locals())[0]
			
			if devpresent:
				switch.operatepoint(motor.i2caddress,motor.i2cbank,motor.closeiopin)

			pyDict = {'motorid':motor.id, 'openiopin':motor.openiopin, 'closeiopin':motor.closeiopin,'i2caddress':motor.i2caddress,'i2cbank':motor.i2cbank,'state':'closed'}

			web.header('Content-Type', 'application/json')
			return json.dumps(pyDict)
		except IndexError:
			pyDict = {'error':'No such motor found'}

			web.header('Content-Type', 'application/json')
			return json.dumps(pyDict)


class hello:
	def GET(self, name):
		return render.swtpl(None)

if __name__ == "__main__":
	app.run()
