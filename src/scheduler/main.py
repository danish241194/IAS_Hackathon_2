import schedule 
import time 
import threading 
from random import randrange
import json
from flask import Flask,request,jsonify
import random
import json
app = Flask(__name__)
class Scheduler:
    def __init__(self):   
        self.job_dict = {}
    def pending_jobs(self):
        while True: 
            schedule.run_pending() 
            time.sleep(10)
            print("running")
    def run(self):
        t1 = threading.Thread(target=self.pending_jobs) 
        t1.start() 
    def exit_service(self,service_instance_id):
        service_instance_id = service_instance_id[0]
        print("send request to service life cycle manager to stop service",service_instance_id)
        #send request to service life cycle manager to cancel service 
        schedule.cancel_job(self.job_dict[service_instance_id])
        
    def run_service(self,service_detail):
        username,application_id,service_name,end,service_instance_id = service_detail[0],service_detail[1],service_detail[2],service_detail[3],service_detail[4]
        print("send request to service life cycle manager to start service ",service_instance_id)
        #send request to service life cycle manager to start service
        job_id = schedule.every().day.at(end).do(self.exit_service,(service_instance_id,)) 
        self.job_dict[service_instance_id]=job_id
        
    def run_service_period(self,service_detail):
        username,application_id,service_name,end,service_instance_id = service_detail[0],service_detail[1],service_detail[2],service_detail[3],service_detail[4]
        print("send request to service life cycle manager to start service ",service_instance_id)
        #send request to service life cycle manager to start service
        job_id = schedule.every().day.at(end).do(self.exit_service,(service_instance_id,)) 
        self.job_dict[service_instance_id]=job_id
        
    def run_service_once(self,service_detail):
        username,application_id,service_name,end,service_instance_id = service_detail[0],service_detail[1],service_detail[2],service_detail[3],service_detail[4]
        print("send request to service life cycle manager to start service ",service_instance_id)

        #send request to service life cycle manager to start service
        job_id =schedule.every().day.at(end).do(self.exit_service,(service_instance_id,)) 
        try:
            if(self.job_dict[service_instance_id]):
                print("here")
                schedule.cancel_job(self.job_dict[service_instance_id])
        except:
            pass
        self.job_dict[service_instance_id]=job_id
    def schedule(self,request_):
        username = request_["username"]
        application_id = request_["application_id"]
        service_name = request_["service_name"]
        single_instance = request_["singleinstance"]
        day = request_["day"]
        start_time = request_["start_time"]
        end = request_["end_time"]
        period = request_["period"]
        service_instance_id=username+application_id+service_name+str(randrange(10000))
        result = "OK"
        
        if(single_instance):
            if(start_time=="NOW"):
                self.run_service_once((username,application_id,service_name,end,service_instance_id))
            elif day is not None:
                job_id = None
                if(day=="monday"):
                    job_id = schedule.every().monday.at(start_time).do( self.run_service_once,((username,application_id,service_name,end,service_instance_id)))
                elif(day=="tuesday"):
                    job_id = schedule.every().tuesday.at(start_time).do( self.run_service_once,((username,application_id,service_name,end,service_instance_id)))
                elif(day=="wednesday"):
                    job_id = schedule.every().wednesday.at(start_time).do( self.run_service_once,((username,application_id,service_name,end,service_instance_id)))
                elif(day=="thursday"):
                    job_id = schedule.every().thursday.at(start_time).do( self.run_service_once,((username,application_id,service_name,end,service_instance_id)))
                elif(day=="friday"):
                    job_id = schedule.every().friday.at(start_time).do( self.run_service_once,((username,application_id,service_name,end,service_instance_id)))
                elif(day=="saturday"):
                    job_id = schedule.every().saturday.at(start_time).do( self.run_service_once,((username,application_id,service_name,end,service_instance_id)))
                else:
                    job_id = schedule.every().sunday.at(start_time).do( self.run_service_once,((username,application_id,service_name,end,service_instance_id)))
                self.job_dict[service_instance_id]=job_id
            else:
                job_id = schedule.every().day.at(start_time).do( self.run_service_once,((username,application_id,service_name,end,service_instance_id)))
            self.job_dict[service_instance_id]=job_id
        elif day is None and period is not None:
            schedule.every(period).days.at(start_time).do( self.run_service_once,((username,application_id,service_name,end,service_instance_id)))
            self.job_dict[service_instance_id]=job_id
        elif day is not None:
                if(day=="monday"):
                    job_id = schedule.every().monday.at(start_time).do( self.run_service,((username,application_id,service_name,end,service_instance_id)))
                elif(day=="tuesday"):
                    job_id = schedule.every().tuesday.at(start_time).do( self.run_service,((username,application_id,service_name,end,service_instance_id)))
                elif(day=="wednesday"):
                    job_id = schedule.every().wednesday.at(start_time).do( self.run_service,((username,application_id,service_name,end,service_instance_id)))
                elif(day=="thursday"):
                    job_id = schedule.every().thursday.at(start_time).do( self.run_service,((username,application_id,service_name,end,service_instance_id)))
                elif(day=="friday"):
                    job_id = schedule.every().friday.at(start_time).do( self.run_service,((username,application_id,service_name,end,service_instance_id)))
                elif(day=="saturday"):
                    job_id = schedule.every().saturday.at(start_time).do( self.run_service,((username,application_id,service_name,end,service_instance_id)))
                else:
                    job_id = schedule.every().sunday.at(start_time).do( self.run_service,((username,application_id,service_name,end,service_instance_id)))
        else:
            result = "ERROR : wrong scheduling format"
        return result,service_instance_id

    
    

    
sch = Scheduler()
sch.run()



def Make_Data(username,application_id,service_name,start_time,end_time,singleinstance=False,day=None,period=None):
	data_dict={"username":username,"application_id":application_id,"service_name":service_name,"singleinstance":singleinstance,"day":day,"start_time":start_time,"end_time":end_time,"period":period}

	return data_dict


def Converter(data):
	return_data=[]

	username=data["username"]
	application_id=data["application_id"]
	service_name=data["service_name"]

	times=[]
	days=[]
	flags=[True,True]

	if "time" in data.keys():
		times=[(s,e) for s,e in zip(data["time"]["start"],data["time"]["end"])]
	else:
		times.append((None,None))
		flags[0]=False

	if "days" in data.keys():
		days=[_ for _ in data["days"]]
	else:
		days.append(None)
		flags[1]=False
		

	if(data["singleinstance"]) or flags[1]:
		for day in days:
			for time in times:
				return_data.append(Make_Data(username=username,application_id=application_id,service_name=service_name,singleinstance=data["singleinstance"],start_time=time[0],end_time=time[1],day=day))
	else:
		for time in times:
			return_data.append(Make_Data(username=username,application_id=application_id,service_name=service_name,singleinstance=data["singleinstance"],start_time=time[0],end_time=time[1],period=data["period"]))

	print(len(return_data))

	return return_data

@app.route('/schedule_service', methods=['GET', 'POST'])
def schedule_service():
    content = request.json
    extracted_requests = Converter(content)
    res = "OK"
    for scheduling_request in extracted_requests:
    	result,service_id = sch.schedule(scheduling_request)
    	if(result!="OK"):
    		res="ERROR : wrong scheduling format"
    return {"result":res}

if __name__ == "__main__":        # on running python app.py
	app.run(debug=True,port=9090) 



