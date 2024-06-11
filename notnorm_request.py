import requests
import json
import datetime

class notnorm_request:
    def __init__(self,url,time_from,time_to):
        self.time_from=time_from
        self.time_to=time_to
        self.Request={"query":{"bool":{"filter":[{"bool":{"must":[{"range":{"time":{"gte":self.time_from}}},{"range":{"time":{"lt":self.time_to}}}],"must_not":[{"term":{"normalized":True}}]}}]}},"aggs":{"@tag":{"terms":{"field":"tag","size":500000,"order":{"_key":"asc"}},"aggs":{"@recv_ipv4":{"terms":{"field":"recv_ipv4","size":500000,"order":{"@count.value":"desc"}},"aggs":{"@count":{"value_count":{"script":"true"}}}},"#m@recv_ipv4":{"missing":{"field":"recv_ipv4"},"aggs":{"@count":{"value_count":{"script":"true"}}}}}},"#m@tag":{"missing":{"field":"tag"},"aggs":{"@recv_ipv4":{"terms":{"field":"recv_ipv4","size":500000,"order":{"@count.value":"desc"}},"aggs":{"@count":{"value_count":{"script":"true"}}}},"#m@recv_ipv4":{"missing":{"field":"recv_ipv4"},"aggs":{"@count":{"value_count":{"script":"true"}}}}}}},"size":0,"_source":["tag","recv_ipv4"]}
        self.url=url+":9200/siem_events*/_search"
        self.headers={"Content-type":"application/json","connection":"close"}

    def __call__(self):
        self.final_list=[]

        response=requests.post(self.url, headers=self.headers, json=self.Request)
        #print(self.time_from,self.time_to, "UTC")

        js=json.loads(response.text)
        #print(response.text)
        try:
            len_aggr=len(js["aggregations"]["@tag"]["buckets"])
        except:
            print("except")
            len_aggr=0
            print(
                f'ExcepTime from: {(datetime.datetime.strptime(self.time_from, "%Y-%m-%dT%H:%M:%S.000Z") + datetime.timedelta(hours=3))};',
                f'Time to: {(datetime.datetime.strptime(self.time_to, "%Y-%m-%dT%H:%M:%S.000Z") + datetime.timedelta(hours=3))}')
            print(f"Status_code :  {response.status_code}; Groups: {len(self.final_list)}")

        for i in range(len_aggr):
            tmp_tag=js["aggregations"]["@tag"]["buckets"][i]["key"]
            #print(tmp_tag)
            len_host=len(js["aggregations"]["@tag"]["buckets"][i]["@recv_ipv4"]["buckets"])
            for j in range(len_host):
                tmp_host=js["aggregations"]["@tag"]["buckets"][i]["@recv_ipv4"]["buckets"][j]["key"]
                count=js["aggregations"]["@tag"]["buckets"][i]["@recv_ipv4"]["buckets"][j]["doc_count"]
                #print(tmp_host)
                self.final_list.append((tmp_host,tmp_tag,count))
        print(
            f'Time from: {(datetime.datetime.strptime(self.time_from, "%Y-%m-%dT%H:%M:%S.000Z") + datetime.timedelta(hours=3))};',
            f'Time to: {(datetime.datetime.strptime(self.time_to, "%Y-%m-%dT%H:%M:%S.000Z") + datetime.timedelta(hours=3))}')
        print(f"Status_code :  {response.status_code}; Groups: {len(self.final_list)}")
        #print(self.final_list)
        return self.final_list

#request=notnorm_request("http://siem.fck.pptrf.ru","2024-03-30T21:00:00.000Z","2024-04-01T19:28:51.000Z")()
#print(request)

