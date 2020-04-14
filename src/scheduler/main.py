import schedule 
import time 
import threading 
from random import randrange
import json
from flask import Flask,request,jsonify
import random
import json
import requests
import argparse

app = Flask(__name__)

service_life_cycle_ip = None
service_life_cycle_port = None
Myport = None


class Scheduler:
    def __init__(self):   
        self.job_dict = {}
        self.main_service_id_dict={}
    def pending_jobs(self):
        minutes=0
        while True: 
            schedule.run_pending() 
            time.sleep(10)
            minutes+=1
            if minutes%6==0:
                print("+ Started ",minutes/6," minutes ago")
    def send_request_to_service_life_cyle(self,username,application_id,service_name,service_instance_id,type_):
        response = {"userId":username,"applicationName":application_id,"servicName":service_name,"serviceId":self.main_service_id_dict[service_instance_id]}
        # if type_=="start":
        #     res = requests.post('http://'+service_life_cycle_ip+':'+str(service_life_cycle_port)+'/servicelcm/service/start', json=response)
        # else:
        #     res = requests.post('http://'+service_life_cycle_ip+':'+str(service_life_cycle_port)+'/servicelcm/service/stop', json=response)
        
    def run(self):
        t1 = threading.Thread(target=self.pending_jobs) 
        t1.start() 
    def exit_service(self,service_instance_id):
        service_instance_id,username,application_id,service_name = service_instance_id[0],service_instance_id[1],service_instance_id[2],service_instance_id[3]
        print("send request to service life cycle manager to stop service",service_instance_id)
        #send request to service life cycle manager to cancel service 
        self.send_request_to_service_life_cyle(username,application_id,service_name,service_instance_id,"stop")
        schedule.cancel_job(self.job_dict[service_instance_id])
        
    def run_service(self,service_detail):
        username,application_id,service_name,end,service_instance_id = service_detail[0],service_detail[1],service_detail[2],service_detail[3],service_detail[4]
        print("send request to service life cycle manager to start service ",service_instance_id)
        #send request to service life cycle manager to start service
        self.send_request_to_service_life_cyle(username,application_id,service_name,service_instance_id,"start")
        job_id = schedule.every().day.at(end).do(self.exit_service,((service_instance_id,username,application_id,service_name))) 
        self.job_dict[service_instance_id]=job_id
        
    def run_service_period(self,service_detail):
        username,application_id,service_name,end,service_instance_id = service_detail[0],service_detail[1],service_detail[2],service_detail[3],service_detail[4]
        print("send request to service life cycle manager to start service ",service_instance_id)
        #send request to service life cycle manager to start service
        self.send_request_to_service_life_cyle(username,application_id,service_name,service_instance_id,"start")
        job_id = schedule.every(end).minutes.do(self.exit_service,((service_instance_id,username,application_id,service_name))) 
        self.job_dict[service_instance_id]=job_id
        
    def run_service_once(self,service_detail):
        username,application_id,service_name,end,service_instance_id = service_detail[0],service_detail[1],service_detail[2],service_detail[3],service_detail[4]
        print("send request to service life cycle manager to start service ",service_instance_id)
        #send request to service life cycle manager to start service
        self.send_request_to_service_life_cyle(username,application_id,service_name,service_instance_id,"start")
        job_id = schedule.every().day.at(end).do(self.exit_service,((service_instance_id,username,application_id,service_name))) 
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
        service_instance_id=username+"_"+application_id+"_"+service_name+"_"+str(randrange(10000))
        main_service_id = username+"_"+application_id+"_"+service_name
        self.main_service_id_dict[service_instance_id]=main_service_id
        result = "OK"
        
        if(str(single_instance)=="True"):
            print("single instance ",bool(single_instance))
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
            
            interval = period["interval"]
            end = period["length"]
            job_id = schedule.every(interval).minutes.do( self.run_service_period,((username,application_id,service_name,end,service_instance_id)))
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
        #   continue
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

    return return_data
   
sch = Scheduler()
sch.run()

@app.route('/schedule_service', methods=['GET', 'POST'])
def schedule_service():
    content = request.json
    extracted_requests = Convert(content)
    res = "OK"
    for scheduling_request in extracted_requests:
        print(scheduling_request)
        result,service_id = sch.schedule(scheduling_request)
        if(result!="OK"):
            res="ERROR : wrong scheduling format"
    return {"result":res}

if __name__ == "__main__": 
    ap = argparse.ArgumentParser()
    ap.add_argument("-p","--port",required=True)
    ap.add_argument("-i","--service_life_cycle_ip",required=True)
    ap.add_argument("-x","--service_life_cycle_port",required=True)
    args = vars(ap.parse_args())          
    service_life_cycle_ip = args["service_life_cycle_ip"]
    service_life_cycle_port = int(args["service_life_cycle_port"])
    Myport = args["port"]
    app.run(debug=True,port=int(Myport)) 



