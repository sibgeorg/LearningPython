log_matrix = {
	"production-api": ['apiservice', 'apiservice-ui', 'clango', 'jumpbox', 'outproxy', 'plivoapi'],
	"production-sms": ['gotham', 'plivosms', 'sharq'],
	"production-voice": ['jumpbox', 'sharq'],
	"production-zentrunk": ['apiservice', 'apiservice-celery', 'clango', 'zt-mediaserver', 'zt-term-inproxy'],
	"staging-api": ['jumpbox'],
	"staging-sms": ['plivosms'],
	"staging-voice": ['jumpbox'],
	"tata-vpn": ['smsc'],
	"tools": ['apiservice-cron', 'smokeping']
}

for stack_element, items in log_matrix.items():
	for service_element in items:
		f = open(stack_element+"-"+service_element+".conf", "w+")
		f.write("<source>\n")
		f.write("@type tail\n")
		f.write("path /audit-logs/"+stack_element+"/"+service_element+"/*.log\n")
		f.write("pos_file /audit-logs/td-agent/s3/logs/"+stack_element+"/"+service_element+"/"+service_element+"-log.pos\n")
		f.write("format none\n")
		f.write("tag s3."+stack_element+"."+service_element)
		f.write("\n</source>\n\n\n\n")
		f.close()
		print service_element + " " + stack_element, "done"
