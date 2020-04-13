import json

def GetDict(services):
	d={}

	for _ in services:
		d[_]=False

	return d

def Make_Data(username,application_id,service_name,start_time=None,end_time=None,singleinstance=False,day=None,period=None):
	data_dict={"username":username,"application_id":application_id,"service_name":service_name,"singleinstance":singleinstance,"day":day,"start_time":start_time,"end_time":end_time,"period":period}

	return data_dict

def Convert(data):
	return_data=[]

	username=data["Application"]["username"]
	application_id=data["Application"]["application_id"]
	services=list(data["Application"]["services"].keys())
	# print(services)
	
	for service in services:
		# if(service!="service-1"):
		# 	continue
		bool_dict=GetDict(services)
		bool_dict[service]=True

		order_dependency=[]
		stack=[]
		stack.append(service)

		while(len(stack) > 0):
			# print(order_dependency)
			temp=stack.pop()
			if(temp!=service):
				order_dependency.append(temp)

			curr_dep=data["Application"]["services"][temp]["dependency"]
			for _ in curr_dep:
				if(not bool_dict[_]):
					stack.append(_)
					bool_dict[_]=True

		order_dependency=order_dependency[::-1]
		order_dependency.append(service)
		print(order_dependency)

		if(data["Application"]["services"][service]["period"]!="None"):
			for service_dep in order_dependency:
				return_data.append(Make_Data(username=username,application_id=application_id,service_name=service_dep,singleinstance="False",period=data["Application"]["services"][service]["period"]))
		else:
			times=[]
			days=[]
			flags=[True,True]

			if "time" in data["Application"]["services"][service].keys():
				times=[(s,e) for s,e in zip(data["Application"]["services"][service]["time"]["start"],data["Application"]["services"][service]["time"]["end"])]
			else:
				times.append((None,None))
				flags[0]=False

			if "days" in data["Application"]["services"][service].keys():
				days=[_ for _ in data["Application"]["services"][service]["days"]]
			else:
				days.append(None)
				flags[1]=False
				
			if(data["Application"]["services"][service]["singleinstance"]) or flags[1]:
				for service_dep in order_dependency:
					for day in days:
						for time in times:
							return_data.append(Make_Data(username=username,application_id=application_id,service_name=service_dep,singleinstance=data["Application"]["services"][service]["singleinstance"],start_time=time[0],end_time=time[1],day=day))
			else:
				for service_dep in order_dependency:
					for time in times:
						return_data.append(Make_Data(username=username,application_id=application_id,service_name=service_dep,singleinstance=data["Application"]["services"][service]["singleinstance"],start_time=time[0],end_time=time[1]))

	print(return_data)



file=open("user_config.json","r")
data=json.load(file)
Convert(data)