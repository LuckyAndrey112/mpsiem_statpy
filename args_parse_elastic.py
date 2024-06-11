#!/usr/bin/python
import argparse
import sys


class args_class:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Sample of valid arguments: MP_stat.exe -t 14.5 -u siem.ru")
        parser.add_argument('-t', '--time', action='store', help='Time in days. Sample: -t 14.5')
        parser.add_argument('-u', '--url', action='store', help='URL Elasticsearch database. Sample: -u siem.ru')
        args = parser.parse_args()
        if args.time==None:
            print("Error. Missing -t key")
            sys.exit()
        try:
            self.time=float(args.time)
        except:
            print("TypeError. Time value must be int or float")
            sys.exit()
        self.url = args.url

        if self.url==None:
            print("Error. Missing -u key")
            sys.exit()


if len(sys.argv)<2:
    print("Error. Need enter arguments -t and -u")
    print("Use -h option for help")
    sys.exit()

arguments=args_class()
#print(arguments.__dict__)
#print(arguments.__dict__)
#print(sys.argv)
