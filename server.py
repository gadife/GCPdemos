import cherrypy
import socket
import base64
import json
import time
import requests
import os

class Root(object):
    PIC_DIRECTORY = "./pics/";

    @cherrypy.expose
    def index(self):
        return """
        <html><body>
            <h2>Upload a file</h2>
            <form action="upload" method="post" enctype="multipart/form-data">
            filename: <input type="file" name="myFile" /><br />
            <input type="submit" />
            </form>
        </body></html>
        """

    @cherrypy.expose    
    def upload(self, myFile):
        out = """<html>
        <head>
            <script src="https://cdn.rawgit.com/google/code-prettify/master/loader/run_prettify.js"></script>
        </head>
        <body>
            <pre class="prettyprint">
 	          %s
            </pre>
        </body>
        </html>"""

        newFile = open(self.PIC_DIRECTORY + str(myFile.filename), 'a+')
        while True:
             data = myFile.file.read()
             if not data:
                 break
             newFile.write(data)
        newFile.close

        image_file = self.PIC_DIRECTORY + str(myFile.filename)
        before_b64 = open(image_file)
        after_b64 = base64.b64encode(before_b64.read())
        timestr = time.strftime("%Y%m%d-%H%M%S")

        file_name = timestr + ".json"
    	my_dict = {                   
    	  'requests': [
    	  {
    	      'image': {
    		'content': after_b64
    		},
    	      'features': [
    	      {
    		'type':"LABEL_DETECTION",
    		'maxResults': 1
    	      },
    	      {
    		'type':"FACE_DETECTION",
    		'maxResults':1
    	      }	
    	      ]
    	  }
    	]
    	}

    	out_file = open(file_name,"w")
    	json.dump(my_dict,out_file, indent=4)
    	out_file.close()

    	data = open(file_name, "rb").read()
    	response = requests.post(url='https://vision.googleapis.com/v1/images:annotate?key=AIzaSyBToFRO9Q4aWzNIjM9J7uxUgPh9sqL6iXs',data=data,headers={'Content-Type': 'application/json'})

        return out % (response.text)

cherrypy.config.update({'server.socket_host': '0.0.0.0'})
cherrypy.tree.mount(Root())
cherrypy.quickstart(Root())