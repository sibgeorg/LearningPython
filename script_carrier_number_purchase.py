import requests
import plivo
import argparse
import csv
import time
import xmltodict
import os

parser = argparse.ArgumentParser(description='Number purchase script')
parser.add_argument('country_iso', help='= US/CA : Country ISO2 for number purchase')
args = parser.parse_args()
#coding=utf-8
date = time.strftime("%c")
auth_id = "MANZG5Y2Q0ODGYOGNKZJ"
auth_token = "ODljYmIzNmU0Yjk5NzJkNjRmOWExNjMxYjQ5Njkz"
p = plivo.RestAPI(auth_id, auth_token)
npa_to_purchase = []
if args.country_iso == 'US':
	#US_NPA = ['253','703','520','410','770','559','985','610','406','714','325','949','352','916','415','817','561','360','510','713','978','303','832','281','650','504','318','540']
	US_NPA = ['201', '202', '203', '205', '206', '207', '208', '209', '210', '212', '213', '214', '215', '216', '217', '218', '219', '220', '223', '224', '225', '227', '228', '229', '231', '234', '239', '240', '248', '251', '252', '253', '254', '256', '260', '262', '267', '269', '270', '272', '274', '276', '279', '281', '301', '302', '303', '304', '305', '307', '308', '309', '310', '312', '313', '314', '315', '316', '317', '318', '319', '320', '321', '323', '325', '327', '330', '331', '334', '336', '337', '339', '346', '347', '351', '352', '360', '361', '364', '380', '385', '386', '401', '402', '404', '405', '406', '407', '408', '409', '410', '412', '413', '414', '415', '417', '419', '423', '424', '425', '430', '432', '434', '435', '440', '442', '443', '445', '447', '458', '463', '464', '469', '470', '475', '478', '479', '480', '484', '501', '502', '503', '504', '505', '507', '508', '509', '510', '512', '513', '515', '516', '517', '518', '520', '530', '531', '534', '539', '540', '541', '551', '559', '561', '562', '563', '564', '567', '570', '571', '573', '574', '575', '580', '585', '586', '601', '602', '603', '605', '606', '607', '608', '609', '610', '612', '614', '615', '616', '617', '618', '619', '620', '623', '626', '628', '629', '630', '631', '636', '640', '641', '646', '650', '651', '657', '660', '661', '662', '667', '669', '678', '680', '681', '682', '689', '701', '702', '703', '704', '706', '707', '708', '712', '713', '714', '715', '716', '717', '718', '719', '720', '724', '725', '726', '727', '730', '731', '732', '734', '737', '740', '743', '747', '754', '757', '760', '762', '763', '765', '769', '770', '772', '773', '774', '775', '779', '781', '785', '786', '801', '802', '803', '804', '805', '806', '808', '810', '812', '813', '814', '815', '816', '817', '818', '820', '828', '830', '831', '832', '838', '843', '845', '847', '848', '850', '854', '856', '857', '858', '859', '860', '862', '863', '864', '865', '870', '872', '878', '901', '903', '904', '906', '907', '908', '909', '910', '912', '913', '914', '915', '916', '917', '918', '919', '920', '925', '928', '929', '930', '931', '934', '936', '937', '938', '940', '941', '947', '949', '951', '952', '954', '956', '959', '970', '971', '972', '973', '978', '979', '980', '984', '985', '986', '989']
elif args.country_iso =='CA':
	US_NPA = ['204', '226', '236', '249', '250', '289', '306', '343', '365', '382', '403', '416', '418', '431', '437', '438', '450', '506', '514', '519', '548', '579', '581', '587', '604', '613', '639', '647', '672', '705', '709', '778', '780', '782', '782', '807', '819', '825', '867', '873', '902', '905']
for i in US_NPA:
	params = {
			'country_iso': args.country_iso,  # The ISO code A2 of the country
			'type': 'local',  # The type of number you are looking for. The possible number types are local, national and tollfree.
			'pattern': i,  # Represents the pattern of the number to be searched.
		}
	response = p.search_phone_numbers(params)  # Calling API to get count of numbers for each NPA
	npa_count=(str(response[1]['meta']['total_count']))
	print "The quantity for Plivo "+ args.country_iso + " NPA " + i + " is " + npa_count
	if int(npa_count) < 40:
		npa_to_purchase.append(i)
print "NPAs to purchase", npa_to_purchase

#Writing all the NPAs to purchase to csv
with open('npa_to_purchase.csv', 'wb') as f:
	writer = csv.writer(f)
	for val in npa_to_purchase:
		writer.writerow([val])

#Calling Inteliquent API:
try:
	os.remove("IQNTordernumberstoadd.csv")
except OSError:
	print"IQNTordernumberstoadd.csv not found"

headers = {'Content-Type': 'application/x-www-form-urlencoded',  'charset': 'UTF-8'}
data = {'client_id': 'xa2ifOgjzOSKcHSluRIFhIuLpQka', 'client_secret': 'KyXWYDsFxk4IaPkgAvkshfFkZo4a', 'grant_type': 'client_credentials'}
response = requests.post('https://services-token.inteliquent.com/oauth2/token', headers=headers, data=data)  #Getting the Oauth2 key
j = response.json()
token = j['access_token']
print token

headers = {'Authorization': 'Bearer %s' %token, 'content-type': 'application/json'}
iqnt_orderid =[]
npa_unavailable_iqnt = []
for i in npa_to_purchase:
	data = {'privateKey': 'xa2ifOgjzOSKcHSluRIFhIuLpQka', 'tnMask': i+'xxxxxxx', 'quantity': '40'}
	#Searching for number using NPA
	try:
		response = requests.post('https://services.inteliquent.com/Services/1.0.0/tnInventory/', headers=headers, json=data)
		j = response.json()
		#print j
		number_order = {"privateKey": "xa2ifOgjzOSKcHSluRIFhIuLpQka", "tnOrder": {"customerOrderReference": "APIorder", "tnList": {"tnItem": []}}}
		print "Checking IQNT NPA %s" % i
		if (j['statusCode'] == '200'):
			#print len(j['tnResult'])
			if len(j['tnResult']) > 1:  # To check if number search response is empty or not
				for index in j['tnResult']:  # Adding all the numbers to the purchase request body
					num = (index['telephoneNumber'])
					fullnum = '1'+str(num)
					tnumber = {"tn": num, "trunkGroup": "CHCGIL24PVO_1029"}
					number_order['tnOrder']['tnList']['tnItem'].append(tnumber)
					fd_iq = open('IQNTordernumberstoadd.csv', 'a')
					w_iq = csv.writer(fd_iq)
					w_iq.writerow([fullnum, "INT:ON"])
					fd_iq.close()

				response = requests.post('https://services.inteliquent.com/Services/1.0.0/tnOrder', headers=headers, json=number_order)
				j = response.json()
				if (j['status'] == 'Success'):
					print "Order for NPA "+i + " "+str(response.json())

				else:
					print "Non 200 response for "+i + " "+str(response.json())
		elif (j['statusCode'] == '430'):
			print "IQNT NPA %s not available" % i
			npa_unavailable_iqnt.append(i)  # Adding NPAs unavailable with IQNT.
	#time.sleep(1)
	except:
		print "Blank response from API"

print "Total NPAs not available with IQNT ",
print npa_unavailable_iqnt

#Writing NPAs not available with IQNT
with open('npa_unavailable_iqnt.csv', 'wb') as f:
	writer = csv.writer(f)
	for val in npa_unavailable_iqnt:
		writer.writerow([val])

#Calling the Onvoy API
npa_unavailable_onvoy = []
onvoy_list = []
print "Calling Onvoy API"
values = {
  "numbers": [],
  "services": {
	"Origination": {
	  "routeLabelId": "72c6301377754af4bfaaff5d2a07cf4d"
	},
	"SMS": {
			  "inboundType": "SMPP"
			}
  }
}
headers = {
	  'Content-Type': 'application/json'
	}
prefixdata = {
	'prefix':'1'
}

for i in npa_unavailable_iqnt:
	response = requests.post('https://api.layered.com/inventory/search/page/50/direction/property?sessionId=a62f508e023a4f55b74bf5f537316ef6cHJldmlvdXMc8bcfdd5158d47d2bb5a988cba6f39e8&prefix=1'+i, headers=headers)
	j = response.json()
	#print j
	#print len(j['result']['entities'])
	#print type(len(j['result']['entities']))
	onvoycount = len(j['result']['entities'])
	if len(j['result']['entities']) == 0:
		npa_unavailable_onvoy.append(i)  # To save NPAs which Onvoy does not have.
		print "Onvoy NPA %s not available" % i
	else:
		print "Onvoy numbers available for NPA "+i+" are %s" % onvoycount
		for index in j['result']['entities']:
			num = str(index['number'])
			values['numbers'].append(num)
			onvoy_list.append(str(num))

#print len(values), " numbers ordered from Onvoy"
response = requests.post('https://api.layered.com/inventory/order?sessionId=a62f508e023a4f55b74bf5f537316ef6cHJldmlvdXMc8bcfdd5158d47d2bb5a988cba6f39e8', headers=headers, json=values)
k = response.json()
print k

#Writing NPAs not available with onvoy
with open('npa_unavailable_onvoy.csv', 'wb') as f:

	writer = csv.writer(f)
	for val in npa_unavailable_onvoy:
		writer.writerow([val])

print "NPAs not available with Onvoy"
print npa_unavailable_onvoy


# # Calling the Bandwidth API:
BWorderidlist = []
npa_unavailable_bw = []
try:
	os.remove("BWordernumbers.csv")
except OSError:
	print"BWordernumbers.csv not found"

for i in npa_unavailable_iqnt:
	response = requests.get('https://dashboard.bandwidth.com/v1.0/accounts/5000041/availableNumbers?areaCode='+i+'&quantity=30', auth=('siby', 'Cloud888'))
	response_text = response.text
	response_dict = xmltodict.parse(response_text)
	#print response_dict
	if response_dict['SearchResult'] is not None:
		if 'Error' in response_dict['SearchResult']:
			print response_dict['SearchResult']['Error']
			npa_unavailable_bw.append(i)
		elif response_dict['SearchResult']['ResultCount'] > 1:
			result_count = int(response_dict['SearchResult']['ResultCount'])
			print "BW count for NPA %s is %d" % (i, result_count)
			#reqeusting for the numbers
			xml = """<Order>
			<SiteId>266</SiteId> <!-- required -->
			<AreaCodeSearchAndOrderType>
			<AreaCode>"""+i+"""</AreaCode>
			<Quantity>"""+str(result_count)+"""</Quantity>
			</AreaCodeSearchAndOrderType>
			</Order>"""
			headers = {'Content-Type': 'application/xml'}
			response = requests.post('https://dashboard.bandwidth.com/v1.0/accounts/5000041/orders/', data=xml, headers=headers, auth=('siby', 'Cloud888'))
			response_text = response.text
			response_dict = xmltodict.parse(response_text)
			BWorderid = response_dict['OrderResponse']['Order']['id']
			BWorderstatus = response_dict['OrderResponse']['OrderStatus']
			BWorderidlist.append(BWorderid)
			print "Status: %s Order ID: %s" % (BWorderstatus, BWorderid)
			fd = open('BWorderids.csv', 'a')
			w = csv.writer(fd)
			w.writerow([BWorderid, date])
			fd.close()
	else:
		print "NPA %s not available" % i
		npa_unavailable_bw.append(i)

print "NPAs not available with BW ", npa_unavailable_bw

#Checking the Bw order IDs
for j in BWorderidlist:
	response = requests.get('https://dashboard.bandwidth.com/v1.0/accounts/5000041/orders/'+j, auth=('siby', 'Cloud888'))
	response_text = response.text
	print j
	response_dict = xmltodict.parse(response_text)
	print response_dict['OrderResponse']['OrderStatus']
	if response_dict['OrderResponse']['OrderStatus'] == 'COMPLETE' or response_dict['OrderResponse']['OrderStatus'] == 'PARTIAL':
		for i in response_dict['OrderResponse']['CompletedNumbers']['TelephoneNumber']:
			try:
				num = str(i['FullNumber'])
				#print i, num
				fd = open('BWordernumbers.csv', 'a')
				w = csv.writer(fd)
				w.writerow([num])
				fd.close()
			except TypeError:
				print "TypeError!!"
				continue

#Writing BW numbers with tnInventory
bw_lrn = {}
bwnumbertier = {}
f = open('BW_LRN.csv')  # BW Coverage - NPANXX mapping
csv_f = csv.reader(f)
for row in csv_f:
	npa_nxx = row[0]
	tier = row[1]
	bw_lrn[npa_nxx] = tier
try:
	f = open('BWordernumbers.csv')  # BW numbers which were purchased part of the order
	csv_f = csv.reader(f)
	for row in csv_f:
		strnum = str(row[0])
		bwnpanxx = strnum[0:6]
		if bwnpanxx in bw_lrn:
			fullnumber = '1'+row[0]
			bwnumbertier[fullnumber] = bw_lrn[bwnpanxx]
		else:
	 		print "NPANXX " + bwnpanxx + " not in BR LRN file." + str(row) + " not added to file."


	#print bwnumbertier
	with open('BWnumberstoadd.csv', 'wb') as csv_file:
		writer = csv.writer(csv_file)
		for key, value in bwnumbertier.items():
			writer.writerow([key, value])
except IOError:
	pass
