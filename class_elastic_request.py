import requests
import json
import datetime

class elastic_request:
    def __init__(self,url,time_from,time_to):
        self.time_from=time_from
        self.time_to=time_to
        self.Request={"query":{"bool":{"filter":[{"bool":{"must":[{"range":{"time":{"gte":time_from}}},
                     {"range":{"time":{"lt":time_to}}}]}}]}},"aggs":{"@event_src.vendor":
                     {"terms":{"field":"event_src/vendor","size":500000,"order":{"_key":"asc"}},"aggs":{"@event_src.host":{"terms":{"field":"event_src/host","size":500000,
                     "order":{"@count.value":"desc"}},"aggs":{"@count":{"value_count":{"script":"true"}}}},"#m@event_src.host":{"missing":{"field":"event_src/host"},
                     "aggs":{"@count":{"value_count":{"script":"true"}}}}}},"#m@event_src.vendor":{"missing":{"field":"event_src/vendor"},"aggs":{"@event_src.host":
                     {"terms":{"field":"event_src/host","size":500000,"order":{"@count.value":"desc"}},"aggs":{"@count":{"value_count":{"script":"true"}}}},
                     "#m@event_src.host":{"missing":{"field":"event_src/host"},"aggs":{"@count":{"value_count":{"script":"true"}}}}}}},"size":0,
                     "_source":["event_src/vendor","event_src/host"]}
        self.url=url+":9200/siem_events*/_search"
        self.headers={"Content-type":"application/json","connection":"close"}

    def __call__(self):
        self.final_list=[]
        response=requests.post(self.url, headers=self.headers, json=self.Request, timeout=(20,3600))
        print(
            f'Time from: {(datetime.datetime.strptime(self.time_from, "%Y-%m-%dT%H:%M:%S.000Z") + datetime.timedelta(hours=3))};',
            f'Time to: {(datetime.datetime.strptime(self.time_to, "%Y-%m-%dT%H:%M:%S.000Z") + datetime.timedelta(hours=3))}')
        print("Status_code :", response.status_code, end='; ')

        js=json.loads(response.text)

        try:
            len_aggr=len(js["aggregations"]["@event_src.vendor"]["buckets"])
        except:
            len_aggr=0

        for i in range(len_aggr):
            tmp_vendor=js["aggregations"]["@event_src.vendor"]["buckets"][i]["key"]
            if tmp_vendor == "opensource":
                tmp_vendor = "linux/unix"


            try:
                len_vendor=len(js["aggregations"]["@event_src.vendor"]["buckets"][i]["@event_src.host"]["buckets"])
            except:
                len_vendor=0
            for j in range(len_vendor):
                tmp_host=js["aggregations"]["@event_src.vendor"]["buckets"][i]["@event_src.host"]["buckets"][j]["key"]
                tmp_count=js["aggregations"]["@event_src.vendor"]["buckets"][i]["@event_src.host"]["buckets"][j]["doc_count"]
                self.final_list.append((tmp_vendor, tmp_host, tmp_count))
                #print(tmp_vendor, tmp_host, tmp_count)

        try:
            vendor_undefined=js["aggregations"]["#m@event_src.vendor"]["@event_src.host"]["buckets"]
            len_vendor_undefined=len(vendor_undefined)
        except:
            len_vendor_undefined=0

        for i in range(len_vendor_undefined):
            tmp_host=js["aggregations"]["#m@event_src.vendor"]["@event_src.host"]["buckets"][i]["key"]
            tmp_count2=js["aggregations"]["#m@event_src.vendor"]["@event_src.host"]["buckets"][i]["doc_count"]
            #print("undefind",tmp_host,tmp_count)
            self.final_list.append(("undefined", tmp_host, tmp_count2))

        #not_norm_count=js["aggregations"]["#m@event_src.vendor"]["#m@event_src.host"]["doc_count"]
        #print("not normilized","not normilized",not_norm_count)
        #self.final_list.append(("not normalized","not normalized", not_norm_count))
        print(f"Groups quantity: {len(self.final_list)}")
        return self.final_list

#request=elastic_request("http://siem.fck.pptrf.ru","2024-03-03T21:00:00.000Z","2024-03-14T11:28:51.000Z")()
#print(request)
