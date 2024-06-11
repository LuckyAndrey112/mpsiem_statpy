#!/usr/bin/python
def fck_decorator(class_to_decorate):
    class DecoratedClass(class_to_decorate):

        """костыль1 ФЦК"""
        @staticmethod
        def summ_list(lst1, lst2):
            lst_rez = []
            if len(lst1) != len(lst2):
                print("Error, lists of different lengths")
                return
            for i in range(len(lst1)):
                lst_rez.append(lst1[i] + lst2[i])
            return lst_rez

        """костыль 2 ФЦК"""
        def microsoft_list(self):
            m_lst = []
            for i in self.hosts2:
                if i.vendor == "microsoft":
                    m_lst.append(i)
            return m_lst

        """костыль 3 ФЦК"""
        def microsoft_aggr(self):
            # print("Длина списка", {len(self.hosts2)})
            delete_candidate = []
            self.microsoft = self.microsoft_list()
            for k, i in enumerate(self.hosts2):
                if i.vendor in ("ESENT", "EventLog", "SceCli"):
                    for j in self.microsoft:
                        if j.hostname == i.hostname:
                            j.lst = self.summ_list(j.lst, i.lst)
                            # delete_candidate.append((i.vendor,i.hostname))
                            delete_candidate.append((i))
            self.hosts2 = list(filter(lambda x: x not in delete_candidate, self.hosts2))
            # print(delete_candidate)
            # self.hosts2=list(filter(lambda x:x.vendor not in [x[0] for x in delete_candidate] or x.hostname not in [x[1] for x in delete_candidate],self.hosts2))
            # print(len(self.hosts2))
            for i in self.hosts2:
                if i.vendor in ("ESENT", "EventLog", "SceCli"):
                    i.vendor = "microsoft"

        """костыль 4 ФЦК"""
        def microsoft_duble(self):
            delete_candidate = []
            microsoft_one = []
            for i in self.microsoft:
                for j in self.microsoft:
                    if j.hostname.lower() == i.hostname.lower() and i != j and j.hostname.lower() not in microsoft_one:
                        #print("до", i.hostname, i.lst)
                        i.lst = self.summ_list(j.lst, i.lst)
                        #print("после", i.hostname, i.lst)
                        microsoft_one.append(j.hostname.lower())
                        delete_candidate.append((j))
            #print("delete cand 4", delete_candidate)
            #print("micr 1", microsoft_one)
            self.hosts2 = list(filter(lambda x: x not in delete_candidate, self.hosts2))

        """костыль 5"""

        def linux_list(self):
            l_lst = []
            for i in self.hosts2:
                if i.vendor == "linux/unix":
                    l_lst.append(i)
            return l_lst

        """костыль 6"""
        def linux_aggr(self):
            # print("Длина списка", {len(self.hosts2)})
            delete_candidate = []
            self.linux = self.linux_list()
            for k, i in enumerate(self.hosts2):
                if i.vendor in ("openvpn", "suse", "undefined", "openssh"):
                    for j in self.linux:
                        if j.hostname == i.hostname:
                            #print(i.hostname)
                            #print(f'before del from {j.lst}', end=' ')
                            j.lst = self.summ_list(j.lst, i.lst)
                            #print(f'after del  {j.lst}', end=' ')
                            delete_candidate.append((i))

            #print(f'from {len(self.hosts2)}', end=' ')
            self.hosts2 = list(filter(lambda x: x not in delete_candidate, self.hosts2))
            #print(f'to {len(self.hosts2)}')

            #print(delete_candidate)
            for i in self.hosts2:
                if i.vendor in ("openvpn", "suse","openssh"):
                    i.vendor = "linux/unix"
                if i.title == "unix_like":
                    i.vendor = "linux/unix"

        """костыль 7"""

        def kasper_domain_list(self):
            k_lst = []
            for i in self.hosts2:
                if i.vendor == "kaspersky" and "." in i.hostname:
                    k_lst.append(i)

            return k_lst


        """костыль 8"""

        def kaspersky_aggr(self):
            # print("Длина списка", {len(self.hosts2)})
            delete_candidate = []
            self.kasper = self.kasper_domain_list()
            for k, i in enumerate(self.hosts2):
                if not "." in i.hostname and i.vendor == "kaspersky":
                    #print("non put", i.hostname)
                    for j in self.kasper:
                        if j.hostname.split(".")[0] == i.hostname:
                            #print("123",j.hostname)
                            #print(f'before del from {j.lst}')
                            j.lst = self.summ_list(j.lst, i.lst)
                            #print(f'after del from {j.lst}')
                            # delete_candidate.append((i.vendor,i.hostname))
                            delete_candidate.append((i))
            #print(f'from {len(self.hosts2)}')
            self.hosts2 = list(filter(lambda x: x not in delete_candidate, self.hosts2))
            #print(f'after {len(self.hosts2)}')

        """костыль 9"""
        def unix_like(self):
            for i in self.hosts2:
                #print(i.title)
                if i.title == ["unix_like"] and i.vendor=="undefined":
                    i.vendor="linux/unix"


        def decorate(self):
            self.microsoft_aggr()
            self.linux_aggr()
            self.linux_aggr()
            self.microsoft_duble()
            self.kaspersky_aggr()
            self.unix_like()
            #print("Decorate successfull")


    return DecoratedClass