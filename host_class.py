from styles_elasticv2 import  generate_cell_addr
#from main_elastic import matrix

class host_class:
    def __init__(self, hostname, lst):
        self.hostname = hostname

        tmp_lst = list(*lst)
        self.lst = tmp_lst[1:]
        #print("host_class", len(self.lst), self.hostname)
        del tmp_lst
        self.vendor = None
        self.number = 1
        #self.tag="None_tag"
        #self.title=["None_title"]

    def __call__(self):
        self.max = f"=MAX(E{self.number}:{generate_cell_addr(len(self.lst) + 4)}{self.number})"
        self.avg = f"=ROUND(AVERAGE(E{self.number}:{generate_cell_addr(len(self.lst) + 4)}{self.number}),5)"
        self.final_list = [self.vendor, (' / '.join(map(str, self.title))), self.hostname, self.tag] + self.lst + [self.max, self.avg]
        del self.lst
        #print("hosts",self.__dict__)
        #print([self.vendor, self.hostname] + [self.tag,self.title] + self.lst)# + [self.max, self.avg])
        return self.final_list