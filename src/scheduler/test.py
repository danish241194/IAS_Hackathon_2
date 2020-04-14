import sys
def function_Add(time,minutes_to_add) :
     hr = int(str(time).split(":")[0])
     mn = int(str(time).split(":")[1])
     mn = (mn+minutes_to_add)
     hr = (hr + int(mn/60))%24
     mn=mn%60
     hr = str(hr)
     mn = str(mn)
     if(len(hr)==1):
         hr="0"+hr
     if(len(mn)==1):
         mn="0"+mn
     return hr+":"+mn

print(function_Add(sys.argv[1],int(sys.argv[2])))

