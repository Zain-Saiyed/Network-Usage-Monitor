from  psutil import net_io_counters
from time import sleep
from pandas import DataFrame
from pandas import read_csv
from datetime import datetime
from os import mkdir
import getopt, sys 

def log_result(curr_time,sent,recieved,network_usage):
    columns=["DateTime","MB sent","MB recieved","Total Usage"]
    path="D:\\NetworkUsage_py\\NetworkLogs\\"
    try:
        mkdir(path)
    except:
        pass
    try:
        df = read_csv(path+curr_time.split(' ')[0].replace('/','-')+"-Network_Log.csv")
    except:
        print("** LOG FILE DOES NOT EXIST CREATING...")
        curr_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        df = DataFrame([[curr_time,0,0,0]],columns=columns)
        df.to_csv(path+curr_time.split(' ')[0].replace('/','-')+"-Network_Log.csv")
    if "Unnamed: 0" in df.columns:
        df = df.drop(['Unnamed: 0'], axis = 1)
    df = df.append([{'DateTime':curr_time, 'MB sent':sent, 'MB recieved':recieved,'Total Usage':network_usage}])
    df.to_csv(path+curr_time.split(' ')[0].replace('/','-')+"-Network_Log.csv")


if __name__ == "__main__" :

    argumentList = sys.argv[1:]
    options = "hd:u:n:o:"
    long_options = ["Help", "Duration", "Unit","NetworkUnit","OutputFile"]
    duration = 30
    unit='sec'
    Nunit=1000 # "KB"
    try: 
        # Parsing argument 
        arguments, values = getopt.getopt(argumentList, options, long_options) 
          
        # checking each argument 
        for currentArgument, currentValue in arguments: 
      
            if currentArgument in ("-h", "--Help"): 
                help_msg = '''\nArguments Description:\n
--Duration / -d : [int value]

This argument specifies the interval in which the the network values are to be saved based on the selected units.
Default Duration = 30 
                
--Units    / -u : [string value]

This argument specifies the unit of the duration specified.
Possible values = [ 'sec' , 'min' , 'hr']
Default unit = sec

--NetworkUnit / -n : [string value]

This argument specifies the Send and Recieve Network unit.
Possible values = [ 'KB' , 'MB' ]
Default unit = KB'''
                print(help_msg)
                sys.exit()
                  
            elif currentArgument in ("-d", "--Duration"): 
##                print("Selected Duration :", currentValue)
                duration = currentValue.strip()
                if not any(c.isalpha() for c in duration) :
                    duration = int(duration)
                else:
                    raise Exception("Invalid Duration value provided. Please Enter a valid Integer duration.")
                    
            elif currentArgument in ("-u", "--Unit"): 
##                print("Selected Unit     :",currentValue)
                unit = currentValue.strip()
                if not unit.lower() in ["sec","min","hr"] :
                    raise Exception("Invalid Duration value provided. Please Enter a valid Time Unit.")
            elif currentArgument in ("-n", "--NetworkUnit"): 
##                print("Selected Network Unit :",currentValue)
                Nunit = currentValue.strip()
                if not Nunit in [ 'KB' , 'MB' ] :
                    raise Exception("Invalid Duration value provided. Please Enter a valid Network Unit.")
                else:
                    if Nunit == 'KB' :
                        Nunit = 1000
                    elif Nunit == 'MB':
                        Nunit = 1e+6
            elif currentArgument in ("-o", "--OutputFile"): 
##                print("Selected Unit     :",currentValue)
                unit = currentValue.strip()
                if not unit.lower() in ["sec","min","hr"] :
                    raise Exception("Invalid Duration value provided. Please Enter a valid Time Unit.")
            

                        
    except Exception as err:
        print("Invalid Argument Passed! \n\nError message : ",str(err))
          

    # Get Duration in given units :
    duration = ((duration,'sec') if unit=='sec' else ( (duration*60,'min') if unit=='min' else (duration*60*60,'hour')))
    
    print("Selected Duration : ",duration[0]," , ",duration[1])
    print("Selected NUnit    : ",Nunit)
    
    prev_sent = net_io_counters().bytes_sent
    prev_recv = net_io_counters().bytes_recv
    ##    print("--PREV : sent -", prev_sent ," recv -",prev_recv)
    TOTAL_VALUE=0
    try:
        while True :
            sleep(duration[0])
            sent = net_io_counters().bytes_sent
            recv = net_io_counters().bytes_recv
        ##    print("--CURR : sent -", sent ," recv -",recv)
            actual_sent = (sent-prev_sent)/Nunit
            actual_recv = (recv-prev_recv)/Nunit
            actual_total= actual_sent+actual_recv
        ##    TOTAL_VALUE += actual_total
            curr_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log_result(curr_time,actual_sent,actual_recv,actual_total)
            print()
            print(f"{curr_time.split(' ')[1]} : Sent= {actual_sent}, Recv= {actual_recv}, Total= {actual_total}")

            prev_sent = sent
            prev_recv = recv
    ##    print("--PREV : sent -", prev_sent ," recv -",prev_recv)
    except Exception as e:
        print(e)
        print(e.__doc__)
        print('User exit prompt!')
