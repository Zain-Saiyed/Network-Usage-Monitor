from  psutil import net_io_counters
from time import sleep
from pandas import DataFrame
from pandas import read_csv
from datetime import datetime
import os 


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

    path="D:\\NetworkUsage_py\\NetworkLogs\\"
    fileName = datetime.now().strftime("%d/%m/%Y %H:%M:%S").split(' ')[0].replace('/','-')+"-Network_Log.csv"
    print(fileName)
    df = read_csv(path+fileName)
    sum_ = df.sum()
    print(f"Summary of {fileName.split('N')[0][:-1]} :")
    print("Total Internet usage : ",round(sum_['Total Usage'],2))
    print("Total Recieved usage : ",round(sum_['MB recieved'],2))
    print("Total   Sent   usage : ",round(sum_['MB sent'],2))
##    choice = input("Do you wish to get the summary of todays network usage?\nChoice :\n1-Yes\n2-No")
