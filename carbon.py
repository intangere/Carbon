import pyximport 
pyximport.install()
from twisted.web.resource import Resource
import sys
from twisted.web.static import File
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from orbit.server import WSGISiteResource
from core import app

app.debug = True
app.config['DEBUG'] = True
resource = WSGIResource(reactor, reactor.getThreadPool(), app)
static_resource = File(app.static_folder)
root_resource = WSGISiteResource(resource, {'static': static_resource})
site = Site(root_resource)

site.displayTracebacks = True

if __name__ == '__main__':

	print 'Carbon is running'

	reactor.listenTCP(8534, site, interface='0.0.0.0')

	reactor.run()
