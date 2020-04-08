# IAS Hackathon 2
## Components Created: Scheduler & Server Life Cycle Manager
### Submitted by
```
Danish Mukhtar - 2018201016
Jay Krishna - 2019201019
```

## Server Life Cycle Manager
Server Life Cycle Manager module is responsible for allocating server on which service life cycle manager can run an algorithm. 
* Server life cycle manager allocates server instance in such a way that computational load among all the avilable servers remains evenly distributed.
* It also decides whether to bring more server instances if all the serves are under more than threshold load.
* For new server instances the server life cycle manager is responsible to install docker and run machine agent code on the instance.
### Data Flow
1. Service life cycle manager will request for a server instance details on it's REST API.
2. Server life cycle manger will hit the REST API of monitoring module & will receive current statistics of all the servers.
3. Then it will calculate average load per core for previous 1 minute & 5 minutes using formula as shown below:
```
Average Load (1 minute or 5 minutes) / Number of CPU cores
```
4. If average load per core is greater than equal to 0.8 or 0.7 for previous 1 minute or 5 minutes respectively no more algorithms will be run on that server.
5. Now server manager will calculate load factor on each server where higher load factor implies less load, then will select server having highest load factor.

```
Coefficient 1 = 1/[ (3/% free CPU) + (1/% free memory) ]
Coefficient 2 = number of events per second / 10000 + min(2,free memory)/10
Coefficient 3 = 0 if CPU temperature greater than critical temperature else 1

Load Factor = (Coefficient 1) * (Coefficient 2) * (Coefficient 3)
```
6. If no server is available then it will request deatils for free available server & setup evironment along with run machine agent code.
7. Finally it will return server details to service life cycle manager in json format as shown below
```json
{
	"result":"RESPONSE RESULT",
	"ip":"127.0.0.1",
	"username":"root",
	"password":"******",
	"port":22
}

```
