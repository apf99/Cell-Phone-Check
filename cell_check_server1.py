#!flask/bin/python
from flask import Flask, jsonify, abort, request
import cell_check as cc 

wp_api_key = 'b4201afb43a8e9320cc96e3a49fb39b9'     # andrew@cyberdreaming.net - production key

app = Flask(__name__)

def undecorate(phone_number):
	phone_number.replace('(', '')
	phone_number.replace(')', '')
	phone_number.replace('-', '')
	phone_number.replace(' ', '')
	return phone_number

def default_response(email):
	return {
					'state_match'              :  False,
					'is_mobile'                :  False,
					'is_valid'				   :  False,
					'email'                    :  email, 
					'accept'                   :  False,
					'status'                   :  400,
					'message'                  :  '', 
					}
	
def parse_posted_data():
	return {
			'first_name'    : str(request.json['first_name']).title(),
			'last_name'     : str(request.json['last_name']).title(),
			'home_phone'    : undecorate( str(request.json['home_phone']) ),
			'work_phone'    : undecorate( str(request.json['work_phone']) ),
			'mobile_phone'  : undecorate( str(request.json['mobile_phone']) ),
			'age'           : str(request.json['age']),
			'email'         : str(request.json['email']).lower(),
			'address1'      : str(request.json['address1']),
			'city'          : str(request.json['city']),
			'state'         : str(request.json['state']),
			'zip'           : str(request.json['zip']),
			'business_name' : str(request.json['business_name'])
		}  

def request_handler():
	print '\n\n****** New Lead *******\n'
	# parse the posted data    
 	app = parse_posted_data()
	
	response = default_response(app['email'])

	data = cc.get_data_from_file()

	# get_data_from_api(app['mobile_phone'], wp_api_key)

	r = cc.parse_data(data)
	# examine the whitepages response
	if r: 
		response['status'] = 200
		response['is_valid'] = r['is_valid']
		if r['state'] == app['state']: response['state_match'] = True
		if r['line_type'] == 'mobile': response['is_mobile'] = True

	# score the lead
	if response['is_valid'] and response['is_mobile'] and response['state_match']: 
		response['accept'] = True

	return response

# routes	
@app.route('/check', methods=['POST'])

def check_cell_phone():
	# put in the test responses here
	if str(request.json['email'])  == 'AcceptResponse':		
		response = default_response('AcceptResponse')
		response['message'] = 'ACCEPT: Forced ACCEPT response.'
		response['accept'] = True		
		response['status'] = 200
		print response['message']
		return jsonify(response)
	if str(request.json['email']) == 'RejectResponse':		
		response = default_response('RejectResponse')
		response['message'] = 'REJECT: Forced REJECT response.'
		response['accept'] = False		
		response['status'] = 200
		print response['message']
		return jsonify(response)	
	
	try:
		response = request_handler()
	except:
		response = default_response()
		message = 'ERROR: General exception thrown at the root level.'
		print message
		response['message'] = message  

	return jsonify(response)
			
@app.route('/')

def index():
	return "Hello, World!"


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5002)
