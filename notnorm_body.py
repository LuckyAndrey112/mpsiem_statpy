#!/usr/bin/python
from openpyxl import Workbook, load_workbook
from time_elastic import timelist
from styles_elasticv2 import styles_line_hor, styles_line_vert, a_merge, draw, generate_cell_addr
from datetime import datetime
import args_parse_elastic
from notnorm_request import notnorm_request
from host_class import host_class

#@fck_decorator
class matrix_notnorm:

    def __init__(self):
        print()
        print("Request for not normalized events")
        #self.t = timelist()
        self.spisok = []
        self.time_len = len(self.t)

        for j in range(self.time_len):
            self.time_from = self.t.lst[j]
            if j + 1 < self.time_len:
                self.time_to = self.t.lst[j + 1]
                self.spisok.append(notnorm_request("http://"+args_parse_elastic.arguments.url,self.time_from, self.time_to))
                #print("success")

        #print(self.spisok)
        self.ip_tag_dict = dict()
        self.ip_list_default = []
        ip_ok = []
        #print(self.time_from,self.time_to)
        a = notnorm_request("http://"+args_parse_elastic.arguments.url,self.t.lst[0], self.t.lst[self.time_len - 1])
        self.js = a()
        del a
        self.len_rows = len(self.js)
        #print("js",self.js)
        #print(self.len_rows)

        for i in range(self.len_rows):
            ip = self.js[i][0]
            tag = self.js[i][1]
            ti = f"{ip}///{tag}"

            self.ip_list_default.append(ti)  # составление полного перечня хостов за весь период
            self.ip_tag_dict[ti] = [ti]
            self.ip_tag_dict[ti].append(self.js[i][1])

        #print(self.ip_list_default)
        self.set_ip_default = set(self.ip_list_default)
        del self.js

        for j in range(self.time_len - 1):  # пробегаем по списку с объектами mp_request, вызываем каждый для запроса
            js = self.spisok[j]()
            ip_ok = []
            for i in range(len(js)):  # от 0 до кол-ва хостов за все время
                count_events = round(float((js[i][2]) / 3600),4)  # забираем количество событий с i объектаip = self.js[i][0]
                ip = js[i][0]
                tag=js[i][1]
                ti = f"{ip}///{tag}"
                #del self.js

                #print(ip,count_events)
                #print("dddd",self.ip_tag_dict.keys())
                if ti in self.ip_tag_dict:
                    #print("ti",ti)
                    self.ip_tag_dict[ti].append(count_events)
                    ip_ok.append(ti)

            set2_ok = set(ip_ok)
            #print("ip_ok",ip_ok)
            list2_ne_ok = list(self.set_ip_default - set2_ok)
            #print("ip_ok",ip_ok)
            #print("ok",set2_ok)
            #print("ne ok", list2_ne_ok)

            for k in list2_ne_ok:
                self.ip_tag_dict[k].append(0)
                #print("add null", k)
        del self.spisok
        self.hosts2 = []

        for i, v in enumerate(self.ip_tag_dict.items()):
            self.hosts2.append(host_class(v[0].split("///")[0], (v[1][1:],)))
            #print("lst",(v[1][1:],))
            #print("123",v[0].split("///")[0])
            self.hosts2[i].vendor = "not normalized"
            self.hosts2[i].tag = v[1][1]
            self.hosts2[i].title = ["non title"]
        #print(self.ip_tag_dict)
        del self.ip_tag_dict

    def __call__(self):
        #print("call")
        self.hosts2 = sorted(self.hosts2, key=lambda x: x.tag)
        return self.hosts2

#Matrix_not_norm = matrix_notnorm()

#for i in Matrix_not_norm():
#    l=i()
#    print(l,len(l))
