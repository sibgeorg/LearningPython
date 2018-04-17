from flask import Flask, request, Response, render_template
from plivo import plivoxml
import json

app=Flask(__name__)

@app.route('/dial/', methods=['GET','POST'])
def default():
        to_number = request.args.get("To")
        print to_number
        #return to_number
        data = request.data
        print data
        dataDict = json.loads(data)
        print type(dataDict)
        return str(dataDict)

if __name__ == "__main__":
    app.run()
