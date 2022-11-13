'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
from datetime import datetime
from datetime import date
import pygal


#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

def Get_Stock_API(API,TimeSeries):
    url = "https://www.alphavantage.co/query?function="+TimeSeries+"&symbol="+API+"&outputsize=full&interval=30min&apikey=RZM5VGNEZOCKLLTT"

    r = requests.get(url).json()
    return r

def getStockName():
    while(True):
        try:
            stockName = str(input("What is the stock symbol for the company you would like to visualize?: "))
        except ValueError:
            print("xxx")
        else:
            break
    return stockName

def getTimeSeries():
    while(True):
            try:
                print("Select the Time Series of the chart you want to Generate")
                print("--------------------------------------------------------")
                print("1. Intraday")
                print("2. Daily")
                print("3. Weekly")
                print("4. Monthly")
                timeSeries = int(input("Enter time series option (1, 2, 3, 4): "))
            except ValueError:
                print("The value you entered is invalid. Only numerical values are valid. \n")
            if(timeSeries > 4 or timeSeries < 0):
                print("Please Enter a number between 1 and 4 for selection \n")
            else:
                break
    if(timeSeries == 1):
        return "TIME_SERIES_INTRADAY"
    elif(timeSeries == 2):
        return "TIME_SERIES_DAILY_ADJUSTED"
    elif(timeSeries == 3):
        return "TIME_SERIES_WEEKLY"
    else:
        return "TIME_SERIES_MONTHLY"
def getChartType():
    while(True):
            try:
                print("Chart Types")
                print("-----------")
                print("1. Bar")
                print("2. Line")
                chartType = int(input("Enter the chart type you want: (Bar (1), Line (2)): "))
            except ValueError:
                print("The value you entered is invalid. Only numerical values are valid. \n")
            if(chartType > 2 or chartType < 0):
                print("Please Enter 1 or 2 for selection \n")
            else:
                break
    return chartType
def setDates(dateparams):
    while(True):
        try:
            date1 = input("Enter the start Date (YYYY-MM-DD): ")
            date2 = input("Enter the end Date (YYYY-MM-DD): ")

            broke1 = date1.split('-')
            broke2 = date2.split('-')

            DATE1 = datetime.date(int(broke1[0]),int(broke1[1]),int(broke1[2]))
            DATE2 = datetime.date(int(broke2[0]),int(broke2[1]),int(broke2[2]))
            dateparams = [[date1,date2],[int(broke1[0]),int(broke1[1]),int(broke1[2])],[int(broke2[0]),int(broke2[1]),int(broke2[2])]]
            if(DATE2 < DATE1):
                print("Dates entered incorrectly")
            else:
                #print(dateparams)
                #print(date1+date2)
                return dateparams
        except ValueError:
            print("Dates Entered Incorrectly, Make sure the Format is correct.")

def main():
    while(True):
        dateparams = [[],[],[]]
        
        dateparams = setDates(dateparams)
        #print(dateparams)
        API = getStockName()
        ChartType = getChartType()
        TimeSeries = getTimeSeries()
        data = Get_Stock_API(API, TimeSeries)
        #print(data)
        #print(data['Time Series (5min)']['2022-10-24 20:00:00'])
        DateTimeList = []
        TimeDateList = []
        DateFilter=[]
        Timelist = []
        OpenList = []
        HighList = []
        LowList = []
        CloseList = []
        count=0
        if(TimeSeries == "TIME_SERIES_INTRADAY"): 
            for i in data['Time Series (30min)']:
                DateFilter.append(i.split(' ')[0])
                year = (int(DateFilter[count].split('-')[0]))
                month =(int(DateFilter[count].split('-')[1]))
                day =(int(DateFilter[count].split('-')[2]))
                count+=1
                ParamStart = datetime.date(int(dateparams[1][0]),int(dateparams[1][1]),int(dateparams[1][2]))
                ParamEnd = datetime.date(int(dateparams[2][0]),int(dateparams[2][1]),int(dateparams[2][2]))
                CurrentDate =datetime.date(year,month,day)
                if((CurrentDate>=ParamStart)&(CurrentDate<=ParamEnd)):
                    Timelist.append(i)
                    DateTimeList.append(i.split(' ')[0])
                    TimeDateList.append(i.split(' ')[1])
            for t in Timelist:
                OpenList.append(float(data['Time Series (30min)'][t]['1. open']))
                HighList.append(float(data['Time Series (30min)'][t]['2. high']))
                LowList.append(float(data['Time Series (30min)'][t]['3. low']))
                CloseList.append(float(data['Time Series (30min)'][t]['4. close']))
        elif(TimeSeries == "TIME_SERIES_DAILY"):
            for i in data['Time Series (Daily)']:
                DateFilter.append(i.split(' ')[0])
                year = (int(DateFilter[count].split('-')[0]))
                month =(int(DateFilter[count].split('-')[1]))
                day =(int(DateFilter[count].split('-')[2]))
                count+=1
                ParamStart = datetime.date(int(dateparams[1][0]),int(dateparams[1][1]),int(dateparams[1][2]))
                ParamEnd = datetime.date(int(dateparams[2][0]),int(dateparams[2][1]),int(dateparams[2][2]))
                CurrentDate =datetime.date(year,month,day)
                if((CurrentDate>=ParamStart)&(CurrentDate<=ParamEnd)):
                    Timelist.append(i)
                    TimeDateList.append(i.split(' ')[0])
            for t in Timelist:
                OpenList.append(float(data['Time Series (Daily)'][t]['1. open']))
                HighList.append(float(data['Time Series (Daily)'][t]['2. high']))
                LowList.append(float(data['Time Series (Daily)'][t]['3. low']))
                CloseList.append(float(data['Time Series (Daily)'][t]['4. close']))
        elif(TimeSeries == "TIME_SERIES_WEEKLY"):
            for i in data['Weekly Time Series']:
                DateFilter.append(i.split(' ')[0])
                year = (int(DateFilter[count].split('-')[0]))
                month =(int(DateFilter[count].split('-')[1]))
                day =(int(DateFilter[count].split('-')[2]))
                count+=1
                ParamStart = datetime.date(int(dateparams[1][0]),int(dateparams[1][1]),int(dateparams[1][2]))
                ParamEnd = datetime.date(int(dateparams[2][0]),int(dateparams[2][1]),int(dateparams[2][2]))
                CurrentDate =datetime.date(year,month,day)
                if((CurrentDate>=ParamStart)&(CurrentDate<=ParamEnd)):
                    Timelist.append(i)
                    TimeDateList.append(i.split(' ')[0])
            for t in Timelist:
                OpenList.append(float(data['Weekly Time Series'][t]['1. open']))
                HighList.append(float(data['Weekly Time Series'][t]['2. high']))
                LowList.append(float(data['Weekly Time Series'][t]['3. low']))
                CloseList.append(float(data['Weekly Time Series'][t]['4. close']))
        else:
            for i in data['Monthly Time Series']:
                DateFilter.append(i.split(' ')[0])
                year = (int(DateFilter[count].split('-')[0]))
                month =(int(DateFilter[count].split('-')[1]))
                day =(int(DateFilter[count].split('-')[2]))
                count+=1
                ParamStart = datetime.date(int(dateparams[1][0]),int(dateparams[1][1]),int(dateparams[1][2]))
                ParamEnd = datetime.date(int(dateparams[2][0]),int(dateparams[2][1]),int(dateparams[2][2]))
                CurrentDate =datetime.date(year,month,day)
                if((CurrentDate>=ParamStart)&(CurrentDate<=ParamEnd)):
                    Timelist.append(i)
                    TimeDateList.append(i.split(' ')[0])
            for t in Timelist:
                OpenList.append(float(data['Monthly Time Series'][t]['1. open']))
                HighList.append(float(data['Monthly Time Series'][t]['2. high']))
                LowList.append(float(data['Monthly Time Series'][t]['3. low']))
                CloseList.append(float(data['Monthly Time Series'][t]['4. close']))        
        '''
        DateList = [None]*(len(Timelist)-1)
        for w in range(len(Timelist)-1):
            year = (int(DateTimeList[w].split('-')[0]))
            month =(int(DateTimeList[w].split('-')[1]))
            day =(int(DateTimeList[w].split('-')[2]))
            hour = (int(TimeDateList[w].split(':')[0]))
            mins = (int(TimeDateList[w].split(':')[1]))
            x = datetime.datetime(year,month,day,hour,mins)
            DateList[w] = x
        '''
        '''
        print("OPEN")
        print(OpenList)

        print("\n HIGH")
        print(HighList)

        print("\n LOW")
        print(LowList)

        print("\n CLOSE")
        print(CloseList)  
        '''
        if(ChartType == 2):
            line_chart = pygal.Line()
            line_chart.title = "Stock Data for " + API +": " + dateparams[0][1] + " to " + dateparams[0][0]
            line_chart.x_labels = TimeDateList
            line_chart.add("Open", OpenList)
            line_chart.add("High", HighList)
            line_chart.add("Low", LowList)
            line_chart.add("Close", CloseList)
            line_chart.render_in_browser()
        else:
            bar_chart = pygal.Bar()
            bar_chart.title = "Stock Data for " + API +": " + dateparams[0][1] + " to " + dateparams[0][0]
            bar_chart.x_labels = TimeDateList
            bar_chart.add("Open", OpenList)
            bar_chart.add("High", HighList)
            bar_chart.add("Low", LowList)
            bar_chart.add("Close", CloseList)
            bar_chart.render_in_browser()


        ending = str(input("Would you like to continue? Enter y or n: \n"))
        if ending == "y":
            continue
        else:
            break    

main()
