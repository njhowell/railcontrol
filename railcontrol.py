import web
import switch


urls = (
	'/sw/(.*)', 'sw',
	'/(.*)', 'hello'
)

app = web.application(urls, globals())
render = web.template.render('templates/')
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

class hello:
	def GET(self, name):
		return render.swtpl(None)

if __name__ == "__main__":
	app.run()
