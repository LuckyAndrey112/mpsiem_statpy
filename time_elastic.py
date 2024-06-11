#!/usr/bin/python
import datetime
import args_parse_elastic

class timelist:
    @staticmethod
    def total_seconds(data:datetime):
        first_date = datetime.datetime(1970, 1, 1)
        time_since = data - first_date
        seconds = int(time_since.total_seconds())
        return seconds

    @staticmethod
    def list_times(absolute=args_parse_elastic.arguments.time,h=1):
        delta=datetime.timedelta(hours=h).total_seconds()
        hours1 = datetime.timedelta(hours=1)
        hours3 = datetime.timedelta(hours=3)
        absolute_delta=datetime.timedelta(days=absolute)
        lst_time=[]
        lst_title_time=[]
        start_sec=__class__.total_seconds(datetime.datetime.now()-absolute_delta-hours1-hours3-hours3)
        iter=start_sec
        now_sec=__class__.total_seconds(datetime.datetime.now()-hours3-hours3)
        while now_sec>iter:
            lst_time.append(datetime.datetime.fromtimestamp(iter+3600).strftime('%Y-%m-%dT%H:%M:%S.000Z'))
            lst_title_time.append(datetime.datetime.fromtimestamp(iter+10800).strftime('%HT%d%b'))
            iter+=delta
        return (lst_time,lst_title_time)

    def __len__(self):
        return len(self.lst)

    def __init__(self):
        spisok=self.list_times()
        self.lst=spisok[0]
        #print(type(self.lst[0]))
        self.title=spisok[1]



#lst=timelist()
#print(lst.lst)
#print(lst.title)
