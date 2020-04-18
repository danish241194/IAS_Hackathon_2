import json
change=True
name="service-4"

def GetDict(services):
    d={}

    for _ in services:
        d[_]=False

    return d
def ConstructDict(data):
    forward_dict={}
    backward_dict={}
    for _ in data.keys():
        forward_dict[_]=data[_]["servicename"]
    for key,values in forward_dict.items():
        backward_dict[values]=key

    return forward_dict,backward_dict

def Make_Data(username,application_id,service_name,start_time=None,end_time=None,singleinstance=False,day=None,period=None):
    data_dict={"username":username,"application_id":application_id,"service_name":service_name,"singleinstance":singleinstance,"day":day,"start_time":start_time,"end_time":end_time,"period":period}

    return data_dict

def GetServices(data,all_services):
    services=[]
    for _ in all_services:
        if(data[_]["scheduled"]=="True"):
            services.append(_)

    return services

def Convert(data):
    return_data=[]

    username=data["Application"]["username"]
    application_id=data["Application"]["applicationname"]
    all_services=list(data["Application"]["services"].keys())
    services=GetServices(data["Application"]["services"],all_services)
    forward_dict,backward_dict=ConstructDict(data["Application"]["services"])
    # print(forward_dict)
    # print(backward_dict)
    # print(services)
    
    for service in services:
        # if(service!="service-1"):
        #   continue
        bool_dict=GetDict(all_services)
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
                if(not bool_dict[backward_dict[_]]):
                    stack.append(backward_dict[_])
                    bool_dict[backward_dict[_]]=True

        order_dependency=order_dependency[::-1]
        order_dependency.append(service)
        # print(order_dependency)

        if(data["Application"]["services"][service]["period"]!="None"):
            for service_dep in order_dependency:
                return_data.append(Make_Data(username=username,application_id=application_id,service_name=forward_dict[service_dep],singleinstance="False",period=data["Application"]["services"][service]["period"]))
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
                            return_data.append(Make_Data(username=username,application_id=application_id,service_name=forward_dict[service_dep],singleinstance=data["Application"]["services"][service]["singleinstance"],start_time=time[0],end_time=time[1],day=day))
            else:
                for service_dep in order_dependency:
                    for time in times:
                        return_data.append(Make_Data(username=username,application_id=application_id,service_name=forward_dict[service_dep],singleinstance=data["Application"]["services"][service]["singleinstance"],start_time=time[0],end_time=time[1]))

    return return_data

def ChangeData(data,name):
    for _ in data["Application"]["services"].keys():
        if(_ != name):
            data["Application"]["services"][_]["scheduled"]="False"
        else:
            data["Application"]["services"][_]["scheduled"]="True"
            del data["Application"]["services"][_]["days"]
            data["Application"]["services"][_]["time"]["start"]=["NOW"]
            data["Application"]["services"][_]["time"]["end"]=["20:00"]

    return data

file=open("user_config.json","r")
data=json.load(file)
if(change):
    data=ChangeData(data,name)

# print(data)
print(Convert(data))
# Convert(data)