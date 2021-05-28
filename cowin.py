import requests
import json
import smtplib
import time
from datetime import date

state = "9"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
sender = 'this particular cowin api script thing.'
# specify the receivers' emails below.
receivers = ['email_id_1', 'email_id_2']

def send_email(message):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	# specify the credentials of the gmail account you'll use to send emails.
	server.login('email_id', 'password')
	server.sendmail('email_id', receivers, message)
	server.close()

while True:
	today = date.today().strftime("%d-%m-%Y")
	success = []

	district_url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/%s" % (state)
	districts = requests.get(url = district_url, headers = headers).json()
	list_d = []
	for i in range(len(districts['districts'])):
		id = districts['districts'][i]['district_id']
		list_d.append(str(id))

	for district in list_d:
		appointments_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=%s&date=%s" % (district, today)
		data = requests.get(url = appointments_url, headers = headers).json()
		for i in range(len(data['centers'])):
			for j in range(len(data['centers'][i]['sessions'])):
				match = 1

				#filters
		
				#if data['centers'][i]['sessions'][j]['available_capacity_dose2'] == 0:
					#match = 0

				if data['centers'][i]['sessions'][j]['available_capacity'] == 0:
					match = 0

				#if data['centers'][i]['sessions'][j]['vaccine'] != 'COVAXIN':
					#match = 0

				if data['centers'][i]['sessions'][j]['min_age_limit'] != 18:
					match = 0

				if match == 1:
					success.append(data['centers'][i])

	print("Found " + str(len(success)) + " results.")
	
	if len(success) >= 1:
		send_email(json.dumps(success, indent = 4))

	print(json.dumps(success, indent = 4))
	time.sleep(300)
