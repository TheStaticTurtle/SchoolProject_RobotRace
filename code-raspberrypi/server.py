from flask import Flask, request
from flask_restful import Resource, Api
from flask.ext.jsonpify import jsonify
import json,thread,time,requests,random,os
import SimpleHTTPServer,SocketServer
import serial

comhost		=	'0.0.0.0'
port_api	=	5002
port_http	=	8888
path_pages	=	'.\static'

groupCodes	=	["132297"	,"75796"  ,"151186"	,"143754"	  ,"148560"	]
groupColors	=	["red"		,"cyan"  ,"blue"			,"pink"	  	,"yellow"	]
groupNames	=	["The nuke"	,"Looser","Les famososss"	,"Atchoum"	,"les caides tookie"	]
groupPlaces	=	[-1	,-1	   ,-1		,-1	  ,-1	]
groupTime	=	[-1	,-1	   ,-1		,-1	  ,-1	]
groupNum	=	5

topColors	=	["white"	,"white"   	,"white"		]
topNames	=	["Non attribuer","Non attribuer","Non attribuer"	]
topTime		=	[-1		,-1		,-1			]

groupCodesDone	=	[]
groupColorsDone	=	[]
isOnline = False

app = Flask(__name__)
api = Api(app)

starttime = time.time()
i=0
lastcode=""

# 132297
# 151186
# 75796
# 148560
# 143754

#Restart 228944

class api_data(Resource):
    def get(self):
		letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZazertyuiopqsdfghjklmwxcvbn"
		exec("letterO = letters[:"+str(groupNum)+"]")
		h=0
		out="{"
		for c in letterO:
				if h != groupNum-1:
						out=out+"\""+c+"\":{\"color\":\""+groupColors[h]+"\",\"name\":\""+groupNames[h]+"\",\"place\":\""+str(groupPlaces[h])+"\",\"time\":\""+str(groupTime[h])+"\"},"
				else:
						out=out+"\""+c+"\":{\"color\":\""+groupColors[h]+"\",\"name\":\""+groupNames[h]+"\",\"place\":\""+str(groupPlaces[h])+"\",\"time\":\""+str(groupTime[h])+"\"}"
				h=h+1
		out=out+"}"
		da = json.loads(out)
		return da

class api_top3(Resource):
    def get(self):
        response = "{\"cars\":{\"a\":{\"time\":\""+str(topTime[0])+"\",\"color\":\"" + topColors[0] + "\",\"group\":\""+topNames[0]+"\"},\"b\":{\"time\":\""+str(topTime[1])+"\",\"color\":\""+topColors[1]+"\",\"group\":\""+topNames[1]+"\"},\"c\":{\"time\":\""+str(topTime[2])+"\",\"color\":\""+topColors[2]+"\",\"group\":\""+topNames[2]+"\"}}}"
        da = json.loads(response)
        return da

class api_online(Resource):
    def get(self):
        response = "{\"online\":"+str(isOnline).lower()+"}"
        da = json.loads(response)
        return da

class api_reset_time(Resource):
    def get(self):
		global starttime
		starttime=time.time()
		response = "{\"done\": true}"
		da = json.loads(response)
		return da

class api_reset_all(Resource):
    def get(self):
	global starttime
	global groupPlaces
	global groupTime
	global topColors
	global topNames
	global topTime
	global groupColorsDone
	global groupCodesDone
	global isOnline
	global i
	global lastcode
	t="["
	for i in range(0,groupNum-1):
		t=t+"-1,"
	t=t+"-1]"
	exec("groupPlacesO = "+t)
	exec("groupTimeO = "+t)
	groupPlaces=groupPlacesO
	groupTime=groupTimeO
	i=0
	lastcode=""
	topColors       =       ["white"        ,"white"        ,"white"                ]
	topNames        =       ["Non attribuer","Non attribuer","Non attribuer"        ]
	topTime         =       [-1             ,-1             ,-1                     ]
	groupColorsDone =       []
	groupCodesDone	=	[]
	isOnline = True
	starttime=time.time()
        response = "{\"done\": true}"
        da = json.loads(response)
        return da


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

@app.route('/api/online/on')
def update_onlineon():
	global isOnline
	isOnline=True
	return jsonify({'out': isOnline})
	

@app.route('/api/online/off')
def update_onlineoff():
	global isOnline
	isOnline=False
	return jsonify({'out': isOnline})

api.add_resource(api_online, '/api/online') # Route_0
api.add_resource(api_data, '/api/data') # Route_1
api.add_resource(api_top3, '/api/top') # Route_2
api.add_resource(api_reset_time, '/api/resettime') # Route_3
api.add_resource(api_reset_all, '/api/resetall') # Route_4

def flaskThread():
	app.run(port=port_api,host=comhost)

def webserverThread():
	Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	web_dir = os.path.join(os.path.dirname(__file__), path_pages)
	Handler.cgi_directories = [web_dir]
	httpd = SocketServer.TCPServer((comhost, port_http), Handler)
	httpd.serve_forever()
	#os.chdir(web_dir)
	#server_address = (comhost, port_http)
	#server = http.server.HTTPServer
	#handler = http.server.CGIHTTPRequestHandler
	#handler.cgi_directories = [web_dir]
	#httpd = server(server_address, handler)
	#httpd.serve_forever()

def genGroups():
	letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	exec("letterO = letters[:"+str(groupNum)+"]")
	i=0
	out="{"
	for c in letterO:
	        if i != groupNum-1:
        	        out=out+"\""+c+"\":{\"color\":\""+groupColors[i]+"\",\"name\":\""+groupNames[i]+"\",\"place\":\""+str(groupPlaces[i])+"\"},"
        	else:
        	        out=out+"\""+c+"\":{\"color\":\""+groupColors[i]+"\",\"name\":\""+groupNames[i]+"\",\"place\":\""+str(groupPlaces[i])+"\"}"
        	i=i+1
	out=out+"}"
	return out


def readRFID():
	line = ser.readline()
	if line:
		rawResponce = line[:-1]
		splitResponce = rawResponce.split(":")
		rawCode = splitResponce[1]
		print rawCode
	

if __name__ == "__main__":
	thread.start_new_thread(flaskThread,())
	thread.start_new_thread(webserverThread,())

os.system("screen -dmS stream '/home/pi/STI2D2_ETT_ROBOT/startStream.sh'")
time.sleep(5)
os.system("chromium-browser --start-maximized http://127.0.0.1:"+str(port_http)+"& sleep 3 && xdotool key F11")

ser = serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
		
while True:
	time.sleep(1)
	if isOnline:
		line = ser.readline()
		if line:
			rawResponce = line[:-1]
			splitResponce = rawResponce.split(":")
			rawCode = splitResponce[1]
			print rawCode
			ch = rawCode
			if not ch in groupCodesDone:
				if lastcode != ch:
					if ch in groupCodes:
						groupCodesDone.append(ch)
						lastcode = ch
						ii = groupCodes.index(ch)
						groupColorsDone.append(groupColors[ii])
						os.system("wget http://127.0.0.1:9000/?action=snapshot -O \""+groupNames[ii]+".jpg\"")
						groupPlaces[ii] = i +1
						groupTime[ii] = round(time.time() - starttime,2)
						if i <= 2:
							topColors[i]	= groupColors[ii]
							topNames[i]	= groupNames[ii]
							topTime[i]	= groupTime[ii]
						i=i+1
						if i==groupNum:
							time.sleep(0.1)
							isOnline = False
				
	else:
		starttime=time.time()

