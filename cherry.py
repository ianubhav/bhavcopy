import cherrypy
from jinja2 import Environment, FileSystemLoader
import urllib.request as urllib2,json
import redis
import os
import utils
from datetime import datetime,timedelta
import json

env = Environment(loader=FileSystemLoader('templates'))
conn = redis.Redis('localhost',charset="utf-8", decode_responses=True)
PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')

now = datetime.now() - timedelta(days=1)

date = now.strftime("%d-%m-%y")
#Fetch data
utils.fetch_and_store_data(conn,date)

class Root:
	@cherrypy.expose
	def index(self):
		tmpl = env.get_template('index.html')
		top_stocks = utils.fetch_top_10_stocks(conn)
		return tmpl.render(top_stocks=top_stocks)

	@cherrypy.expose
	@cherrypy.tools.json_out()
	def search(self,word):
		stocks = utils.match_key(conn,word)
		return stocks

config = {
	'/static':{
	'tools.staticdir.on': True,
	'tools.staticdir.dir': PATH
	}
}

cherrypy.tree.mount(Root(), '/', config = config)
cherrypy.config.update({'server.socket_host': '0.0.0.0'})
cherrypy.engine.start()

