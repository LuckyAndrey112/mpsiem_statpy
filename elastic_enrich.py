import requests
import json

class elastic_request_enrich():
    def __init__(self,url,time_from,time_to):
        self.time_from=time_from
        self.time_to=time_to
        self.Request = {"query":{"bool":{"filter":[{"bool":{"must":[{"range":{"time":{"gte":self.time_from}}},{"range":{"time":{"lt":self.time_to}}}]}}]}},"aggs":{"@event_src.vendor":{"terms":{"field":"event_src/vendor","size":500000,"order":{"_key":"asc"}},"aggs":{"@event_src.host":{"terms":{"field":"event_src/host","size":500000,"order":{"_key":"asc"}},"aggs":{"@tag":{"terms":{"field":"tag","size":500000,"order":{"_key":"asc"}},"aggs":{"@event_src.title":{"terms":{"field":"event_src/title","size":500000,"order":{"@count.value":"desc"}},"aggs":{"@count":{"value_count":{"script":"true"}}}},"#m@event_src.title":{"missing":{"field":"event_src/title"},"aggs":{"@count":{"value_count":{"script":"true"}}}}}},"#m@tag":{"missing":{"field":"tag"},"aggs":{"@event_src.title":{"terms":{"field":"event_src/title","size":500000,"order":{"@count.value":"desc"}},"aggs":{"@count":{"value_count":{"script":"true"}}}},"#m@event_src.title":{"missing":{"field":"event_src/title"},"aggs":{"@count":{"value_count":{"script":"true"}}}}}}}},"#m@event_src.host":{"missing":{"field":"event_src/host"},"aggs":{"@tag":{"terms":{"field":"tag","size":500000,"order":{"_key":"asc"}},"aggs":{"@event_src.title":{"terms":{"field":"event_src/title","size":500000,"order":{"@count.value":"desc"}},"aggs":{"@count":{"value_count":{"script":"true"}}}},"#m@event_src.title":{"missing":{"field":"event_src/title"},"aggs":{"@count":{"value_count":{"script":"true"}}}}}},"#m@tag":{"missing":{"field":"tag"},"aggs":{"@event_src.title":{"terms":{"field":"event_src/title","size":500000,"order":{"@count.value":"desc"}},"aggs":{"@count":{"value_count":{"script":"true"}}}},"#m@event_src.title":{"missing":{"field":"event_src/title"},"aggs":{"@count":{"value_count":{"script":"true"}}}}}}}}}},"#m@event_src.vendor":{"missing":{"field":"event_src/vendor"},"aggs":{"@event_src.host":{"terms":{"field":"event_src/host","size":500000,"order":{"_key":"asc"}},"aggs":{"@tag":{"terms":{"field":"tag","size":500000,"order":{"_key":"asc"}},"aggs":{"@event_src.title":{"terms":{"field":"event_src/title","size":500000,"order":{"@count.value":"desc"}},"aggs":{"@count":{"value_count":{"script":"true"}}}},"#m@event_src.title":{"missing":{"field":"event_src/title"},"aggs":{"@count":{"value_count":{"script":"true"}}}}}},"#m@tag":{"missing":{"field":"tag"},"aggs":{"@event_src.title":{"terms":{"field":"event_src/title","size":500000,"order":{"@count.value":"desc"}},"aggs":{"@count":{"value_count":{"script":"true"}}}},"#m@event_src.title":{"missing":{"field":"event_src/title"},"aggs":{"@count":{"value_count":{"script":"true"}}}}}}}},"#m@event_src.host":{"missing":{"field":"event_src/host"},"aggs":{"@tag":{"terms":{"field":"tag","size":500000,"order":{"_key":"asc"}},"aggs":{"@event_src.title":{"terms":{"field":"event_src/title","size":500000,"order":{"@count.value":"desc"}},"aggs":{"@count":{"value_count":{"script":"true"}}}},"#m@event_src.title":{"missing":{"field":"event_src/title"},"aggs":{"@count":{"value_count":{"script":"true"}}}}}},"#m@tag":{"missing":{"field":"tag"},"aggs":{"@event_src.title":{"terms":{"field":"event_src/title","size":500000,"order":{"@count.value":"desc"}},"aggs":{"@count":{"value_count":{"script":"true"}}}},"#m@event_src.title":{"missing":{"field":"event_src/title"},"aggs":{"@count":{"value_count":{"script":"true"}}}}}}}}}}},"size":0,"_source":["event_src/vendor","event_src/host","tag","event_src/title"]}
        self.headers={"Content-type":"application/json","connection":"close"}
        self.url = url + ":9200/siem_events*/_search"

    def __call__(self):
        print()
        print("Enrichment request for tag and title")
        self.final_list=[]
        response=requests.post(self.url, headers=self.headers, json=self.Request, timeout=(20,3600))
        print("Status code", response.status_code)
        print("OK")
        js=json.loads(response.text)
        len_aggr=len(js["aggregations"]["@event_src.vendor"]["buckets"])

        for i in range(len_aggr):
            tmp_vendor=js["aggregations"]["@event_src.vendor"]["buckets"][i]["key"]
            if tmp_vendor == "opensource":
                tmp_vendor = "linux/unix"

            len_vendor=len(js["aggregations"]["@event_src.vendor"]["buckets"][i]["@event_src.host"]["buckets"])
            for j in range(len_vendor):
                tmp_host=js["aggregations"]["@event_src.vendor"]["buckets"][i]["@event_src.host"]["buckets"][j]["key"]
                tmp_tag = js["aggregations"]["@event_src.vendor"]["buckets"][i]["@event_src.host"]["buckets"][j]["@tag"][
                    "buckets"][0]["key"]
                try:
                    tmp_title=js["aggregations"]["@event_src.vendor"]["buckets"][i]["@event_src.host"]["buckets"][j]["@tag"][
                    "buckets"][0]["@event_src.title"]["buckets"]#[0]["key"]
                except:
                    tmp_title=[]

                tmp_title_list = []
                if tmp_tag == None:
                    tmp_tag == "None_tag"

                for g in range(len(tmp_title)):
                    tmp_title_list.append(tmp_title[g]["key"])
                tmp_title_list = sorted(tmp_title_list, reverse=True)

                self.final_list.append((tmp_vendor, tmp_host, tmp_tag,tmp_title_list))

        vendor_undefined=js["aggregations"]["#m@event_src.vendor"]["@event_src.host"]["buckets"]
        len_vendor_undefined=len(vendor_undefined)

        for i in range(len_vendor_undefined):
            try:
                tmp_host=js["aggregations"]["#m@event_src.vendor"]["@event_src.host"]["buckets"][i]["key"]
            except:
                tmp_host="undefined host"
            try:
                tmp_tag2=js["aggregations"]["#m@event_src.vendor"]["@event_src.host"]["buckets"][i]["@tag"]["buckets"][0]["key"]
            except:
                tmp_tag2="None_tag"
            try:
                tmp_title2=js["aggregations"]["#m@event_src.vendor"]["@event_src.host"]["buckets"][i]["@tag"]["buckets"][0]["@event_src.title"]["buckets"]
            except:
                tmp_title2=[]
            #print(3456, tmp_title2)
            tmp_title_list2=[]
            for g in range(len(tmp_title2)):
                tmp_title_list2.append(tmp_title2[g]["key"])
            tmp_title_list2=sorted(tmp_title_list2, reverse=True)

            #print("undefind",tmp_host,tmp_count)
            #print(12345, tmp_tag2)
            self.final_list.append(("undefined", tmp_host,tmp_tag2,tmp_title_list2))

        self.final_list.append(("not normalized","not normalized","not normalized",["not normalized"]))
        #print("len",len(self.final_list))
        return self.final_list

#request=elastic_request_enrich("http://siem.fck.pptrf.ru","2024-03-03T21:00:00.000Z","2024-03-14T11:28:51.000Z")()
#print(request)
#for i in request:
#    print(len(i))
