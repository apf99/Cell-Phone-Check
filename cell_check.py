import pickle
import pprint
import pymongo
import datetime

app = {
        'first_name'    : 'Sunshine',
        'last_name'     : 'Jessen',
        'home_phone'    : '3101234567',
        'work_phone'    : '3101234567',
        'mobile_phone'  : '7026120606',
        'age'           : '26',
        'email'         : 'AcceptResponse',
        'address1'      : '23 SHIRLey Lane',
        'city'          : 'Santa Monica',
        'state'         : 'NV',
        'zip'           : '90002',
        'business_name' : 'Fastcash'
}


def connect_to_mongodb():
    connection = 'mongodb://andyf:!Destr0y@cluster0-shard-00-00-fnfrp.mongodb.net:27017,'  
    connection += 'cluster0-shard-00-01-fnfrp.mongodb.net:27017,'                           
    connection += 'cluster0-shard-00-02-fnfrp.mongodb.net:27017/test?'                      
    connection +=  'ssl=true&replicaSet=Cluster0-shard-0&authSource=admin'

    client = pymongo.MongoClient(connection)
    return client.test

def clear_database(db):
    db.test.rem

def time_date_stamp(start):
    now = datetime.datetime.now()
    elapsed_time = now - start
    timeString = '{}'.format( time.strftime('%m-%d-%Y %H:%M:%S') )
    print('\nUpdated: ', timeString)
    print('Elapsed Time: {}s\n'.format(elapsed_time.seconds))
    print('now.timetuple:', now.timetuple)
    print(time.mktime(now.timetuple()))

    return time.mktime(now.timetuple())

def update_database(db, phone_number='7026040606'):
    api_key = '3b20432ffcce4e74b73b0549baa2eff9'
	data = get_data_from_api(phone_number, api_key)
    db.test.insert(data)

def get_data_from_db(db, phone_number, datapoints=1):
	results = db.test.find()
	results = results.sort('time', -1)
	results = results.limit(datapoints)
	
	data = {}   

	for result in results:
		data[phone_number].append((adj_time, value1, value2, spread, percent))
	return data    



def get_data_from_file():
	with open('response_obj1.py', 'rb') as input_file:
		return pickle.load(input_file)

def get_data_from_api(phone_number, key):
	endpoint = 'https://proapi.whitepages.com/3.0/phone?'
	url = endpoint + 'phone=' + phone_number + '&api_key=' + key
	return requests.get(url).json()

def parse_data(data):
	response = {}
	if data:
		if not data['error']:
			if 'is_valid' in data: response['is_valid'] = data['is_valid']
			if 'line_type' in data: response['line_type'] = data['line_type'].lower()
			if 'current_addresses' in data: response['state'] = data['current_addresses'][0]['state_code'].upper()
	if len(response)>0:
		return response
	else:
		return None

def data_age(data):
	time = datetime.datetime.now()

def score_app():
	# data = get_data_from_database()
	# if not data OR data_age(data) > 100*days: data = update_database()

	data = get_data_from_file()
	response = parse_data(data)

	if not response: return False
	if response['is_valid'] and response['line_type'] == 'mobile' and response['state'] == app['state']: 
		return True
	return False

def main():
	isAccepted = score_app()
	db = connect_to_mongodb()

	if isAccepted:
		print 'ACCEPTED'
	else:
		print 'REJECTED'


if __name__ == '__main__':
 	main()


