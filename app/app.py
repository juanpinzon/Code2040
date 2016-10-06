import json
import requests
from flask import make_response
from flask import Response
from flask import jsonify
import datetime


from flask import Flask, render_template
app = Flask(__name__)

#Common data
url = "http://challenge.code2040.org/api/"
token = "" #Put the token here
post_data = {"token":token}

#Home
@app.route('/home')
def home():
	return render_template('home.html')


#Step 1
@app.route('/step1')
def step1():
	post_url = url + "register"
	post_data = {"token":token, "github":"https://github.com/juanpinzon/Code2040"}
	post_response = requests.post(post_url, json = post_data)
	if post_response.status_code==200:
		return "Registered"


#Step 2
@app.route('/step2')
def step2():
	#Initial request for the input data
	post_url = url + "reverse"
	post_response = requests.post(post_url, json = post_data)
	
	#if successful HTTP requests. 
	if post_response.status_code==200:
		#Reversed string
		backwards = post_response.content[::-1]

		#Send the results
		result_data = {"token":token, "string":backwards}
		result_url = url + "reverse/validate"
		requests.post(result_url, json = result_data)
	
	#Display result on the browser		
	return jsonify(result_data)


@app.route('/step3')
def step3():
	#Initial request for the input data
	post_url = url + "haystack"	
	post_response = requests.post(post_url, json = post_data)

	#if successful HTTP requests. 
	if post_response.status_code==200:
		#Get the data
		data = json.loads(post_response.content)
		needle = data["needle"]
		haystack = data["haystack"]

		#check if needle is on the haystaclk
		if needle in haystack:
			index = haystack.index(needle)

			#Send the results
			result_data = {"token":token, "needle":index}
			result_url = url + "haystack/validate"
			requests.post(result_url, json = result_data)
	
	#Display result on the browser
	return jsonify(result_data)


@app.route('/step4')
def step4():
	#Initial request for the input data
	post_url = url + "prefix"	
	post_response = requests.post(post_url, json = post_data)

	#if successful HTTP requests. 
	if post_response.status_code==200:
		#Get the data
		data = json.loads(post_response.content)		
		prefix = data["prefix"]
		array = data["array"]				

		#Traverses the array checking for element that starts with prefix
		solution = []
		for str in array:			
			if not str.startswith(prefix):
				solution.append(str)
				
		#Send the results				
		result_data = {"token":token, "array":solution}
		result_url = url + "prefix/validate"
		requests.post(result_url, json = result_data)
	
	#Display result on the browser
	return jsonify(result_data)


@app.route('/step5')
def step5():
	#Initial request for the input data
	post_url = url + "dating"	
	post_response = requests.post(post_url, json = post_data)

	#if successful HTTP requests. 
	if post_response.status_code==200:
		#Get the data
		data = json.loads(post_response.content)		
		datestamp = data["datestamp"]
		interval = data["interval"]				

		#Converts Strings ISO 8601 into python datestamp. 
		date = datetime.datetime.strptime(datestamp, "%Y-%m-%dT%H:%M:%SZ")
		#Add seconds to the date
		new_date = date + datetime.timedelta(seconds=interval)	
		#Converts 
		solution = new_date.strftime("%Y-%m-%dT%H:%M:%SZ")	
			
		#Converts python datestamp into Strings. Send the results	
		result_data = {"token":token, "datestamp":solution}
		result_url = url + "dating/validate"
		requests.post(result_url, json = result_data)

	#Display result on the browser
	return jsonify(result_data)


@app.route('/about')
def about():
	return render_template('about.html')

@app.route("/ass")
def hello():
	return "Hello to Assignment1!!"

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0')
