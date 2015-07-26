#!/usr/bin/env python
import web
import switch
import json

urls = (
	'/api/open/(\d+)', 'open',
	'/api/close/(\d+)', 'close',
	'/api/toggle/(\d+)', 'toggle',
	'/(.*)', 'index'
)

app = web.application(urls, globals())
render = web.template.render('templates/')
db = web.database(dbn='sqlite', db='railcontroldb')

try:
	switch.setupio(1,0x20)
	devpresent = True
except IOError:
	devpresent = False

class open:
	def GET(self, motorid):
		try:
			motor = db.select('pointmotors', where="id=$motorid", vars=locals())[0]
		
			if devpresent:
				switch.operatepoint(motor.i2caddress,motor.i2cbank,motor.openiopin)
			db.update('pointmotors', where="id=$motorid", currentstate='open', vars=locals())

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
			db.update('pointmotors', where="id=$motorid", currentstate='closed', vars=locals())

			pyDict = {'motorid':motor.id, 'openiopin':motor.openiopin, 'closeiopin':motor.closeiopin,'i2caddress':motor.i2caddress,'i2cbank':motor.i2cbank,'state':'closed'}

			web.header('Content-Type', 'application/json')
			return json.dumps(pyDict)
		except IndexError:
			pyDict = {'error':'No such motor found'}

			web.header('Content-Type', 'application/json')
			return json.dumps(pyDict)

class toggle:
	def GET(self, motorid):
		try:
			motor = db.select('pointmotors', where="id=$motorid", vars=locals())[0]
			if motor.currentstate == 'open':
				iopin = motor.closeiopin
				newstate = "closed"
			else:
				iopin = motor.openiopin
				newstate = "open"

			if devpresent:
				switch.operatepoint(motor.i2caddress,motor.i2cbank,iopin)
			db.update('pointmotors', where="id=$motorid", currentstate=newstate, vars=locals())

			pyDict = {'motorid':motor.id, 'openiopin':motor.openiopin, 'closeiopin':motor.closeiopin,'i2caddress':motor.i2caddress,'i2cbank':motor.i2cbank,'state':newstate}

			web.header('Content-Type', 'application/json')
			return json.dumps(pyDict)
		except IndexError:
			pyDict = {'error':'No such motor found'}

			web.header('Content-Type', 'application/json')
			return json.dumps(pyDict)


class index:
	def GET(self, name):
		motors = db.select('pointmotors', order='id ASC')
		return render.swtpl(motors)

if __name__ == "__main__":
	app.run()
