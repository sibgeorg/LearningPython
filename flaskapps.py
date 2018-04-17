from flask import Flask, request, Response, render_template
from plivo import plivoxml


app=Flask(__name__)

@app.route('/dial/', methods=['GET','POST'])
def dial():

    # When an outbound call is made and then connected different number using Dial element,
    # you can play a custom caller tone using the dialMusic attribute
	response = plivoxml.ResponseElement()
	response.add(plivoxml.DialElement().add(plivoxml.NumberElement('15671234567', send_digits='wwww2410')))
	return response.to_string()

@app.route('/', methods=['GET','POST'])
def default():
	to_number = request.args.get("To")
	print to_number
	return to_number

@app.route('/dialdynamic/', methods=['GET','POST'])
def dialdynamic():
	to_number = request.args.get("To")
	response = plivoxml.ResponseElement()
        response.add(plivoxml.DialElement().add(plivoxml.NumberElement(to_number, send_digits='wwww2410')))
        return response.to_string()

@app.route('/web/', methods=['GET','POST'])
def web():
        return render_template('index.html')

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


if __name__ == "__main__":
    app.run()
