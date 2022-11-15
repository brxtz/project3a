'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 
This is where you should add your code to function query the api
'''
import requests
from datetime import datetime
from datetime import date
import pygal


def Get_Stock_API(StockSymbol,TimeSeries):

    #Convert Time Series number into str for api to use
    TimeSeries = int(TimeSeries)
    if(TimeSeries == 1):
        function = "TIME_SERIES_INTRADAY"
    elif(TimeSeries == 2):
        function = "TIME_SERIES_DAILY_ADJUSTED"
    elif(TimeSeries == 3):
        function = "TIME_SERIES_WEEKLY"
    elif(TimeSeries == 4):
        function = "TIME_SERIES_MONTHLY"

    url = "https://www.alphavantage.co/query?function="+function+"&symbol="+StockSymbol+"&outputsize=full&interval=30min&apikey=RZM5VGNEZOCKLLTT"

    r = requests.get(url).json()
    return r

#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

def GenerateChart(symbol,chart_type,time_series,start_date,end_date):
    data = Get_Stock_API(symbol,time_series)

    TimeDateList = []
    OpenList = []
    HighList = []
    LowList = []
    CloseList = []

    if(time_series == '1'): 
        for i in data['Time Series (30min)']:
            current_date = convert_date(i[:10])
            if((current_date>=start_date)&(current_date<=end_date)):
                OpenList.append(float(data['Time Series (30min)'][i]['1. open']))
                HighList.append(float(data['Time Series (30min)'][i]['2. high']))
                LowList.append(float(data['Time Series (30min)'][i]['3. low']))
                CloseList.append(float(data['Time Series (30min)'][i]['4. close']))
                
        '''
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

    if(chart_type == '2'):
        line_chart = pygal.Line()
        line_chart.title = "Stock Data for " + symbol +": " + start_date.strftime("%Y-%m-%d") + " to " + end_date.strftime("%Y-%m-%d")
        line_chart.x_labels = TimeDateList
        line_chart.add("Open", OpenList)
        line_chart.add("High", HighList)
        line_chart.add("Low", LowList)
        line_chart.add("Close", CloseList)
        return line_chart.render_data_uri()
    else:
        bar_chart = pygal.Bar()
        bar_chart.title = "Stock Data for " + symbol +": " + start_date.strftime("%Y-%m-%d") + " to " + end_date.strftime("%Y-%m-%d")
        bar_chart.x_labels = TimeDateList
        bar_chart.add("Open", OpenList)
        bar_chart.add("High", HighList)
        bar_chart.add("Low", LowList)
        bar_chart.add("Close", CloseList)
        return bar_chart.render_data_uri()