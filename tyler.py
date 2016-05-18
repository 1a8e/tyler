#!/usr/bin/python2

versionString = 'v0.220.150919174949'
appName = u'\u03c4\u03c8\u03bb\u03b5\u03c1'
# Copyright 2015 Anas Ahmed
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

import re
import os
import pickle
import readline
import datetime

green = '32'
red = '31'
blue = '34'
yellow = '33'
bakseq = 0

def hilite(string, color, bold):
    attr = []
    attr.append(color)
    if bold:
        attr.append('1')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

def extractFromCSV(filename):
    cydict = {}
    cydict['count'] = (0, 0, int(os.sys.argv[3]), int(os.sys.argv[3]))
    totcount = 0
    errcount = 0
    succount = 0
    pat = r'[\d: /]+,([a-zA-Z]+ [a-zA-Z ]*[a-zA-Z]+),(.*),(\d{10}).*'
    with open(filename, 'r') as f:
        for line in f:
            totcount += 1
            match = re.search(pat, line)
            if match:
                if match.group(3).strip() in cydict:
                    print hilite('Duplicate: ' + match.group(3).strip(), 
                        yellow, 0)
                    cydict['count'] = (
                        cydict['count'][0] - 1,
                        cydict['count'][1],
                        cydict['count'][2],
                        cydict['count'][3]
                        )
                cydict[match.group(3).strip()] = \
                    (match.group(1).strip().title(), 0, None)
                succount += 1
                cydict['count'] = (
                    cydict['count'][0] + 1,
                    cydict['count'][1],
                    cydict['count'][2],
                    cydict['count'][3]
                    )
            else:
                errcount += 1
                print >> os.sys.stderr,\
                    hilite('Failed to parse line ' + str(totcount), red, 1)
    print
    print 'Read ' + str(totcount) + ' lines'
    print hilite(str(succount) + ' succesful', green, 1)
    print hilite(str(errcount) +' failed', green if not errcount else red, 1)
    os.system('sleep 5')
    return cydict

def loadbak():
    global bakseq
    baklist = sorted(
        filter(lambda x: re.search(r'(attn_bak)(\d+)', x),
            os.listdir(os.path.join('.'))),
        key=lambda x: int(re.search(r'(\d+)', x).group(1))
        )
    if(len(baklist)):
        bakseq = int(re.search(r'(\d+)', baklist[-1]).group(1))

        assert bakseq is len(baklist)

        with open('attn_bak' + str(bakseq), 'r+') as currbak:
            cydict = pickle.load(currbak)
        print hilite('Loaded backup ' + str(bakseq) + ' with ' +
            str(len(cydict)-1) + ' entries', green, 1)
        os.system('sleep 2')
        return cydict
    else:
        print hilite('Attempt to load an existing backup failed!', red, 1)
        return None

def writebak(cydict):
    global bakseq
    bakseq += 1
    with open('attn_bak' + str(bakseq), 'w') as currbak:
        pickle.dump(cydict, currbak)

def debugMode(cydict):
    if cydict:
        for key in sorted(cydict.keys(), key=lambda x: cydict[x]):
            print hilite(str(cydict[key]) +' ' + key,
                green if cydict[key][1] else red, 0)
        assert cydict['count'][1] + cydict['count'][2] is cydict['count'][3]
        assert len(cydict)-1 is cydict['count'][0]
    else:
        print hilite('cydict not initalised', red, 0)

def regnew(cydict, number):
    choice = raw_input(hilite('1: New registration | 0: Retry:\n', yellow, 1))
    if choice is '1':
        while True:
            inputstr = raw_input(hilite('Full Name:\n', blue, 1))
            if inputstr is 'q':
                return
            namepat = r'([a-zA-Z]+ [a-zA-Z ]*[a-zA-Z]+)'
            match = re.search(namepat, inputstr)
            if not match:
                print ('Invalid name! | q: quit')
            else:
                inputstr = inputstr.strip().title()
                break
    elif choice is '0':
        return
    else:
        print('Invalid choice!')
        return
    cydict['count'] = (
        cydict['count'][0] + 1,
        cydict['count'][1] + 1,
        cydict['count'][2] - 1,
        cydict['count'][3]
        )
    cydict[number] = (
        inputstr,
        cydict['count'][1],
        str(datetime.datetime.now())
        )
    print hilite('You have succesfully identified as: ' + 
        cydict[number][0], green, 1)
    writebak(cydict)

def loginMode(cydict):
    timestr = '2016-03-04 16:00:00.000000'
    os.system('clear')
    print hilite('Admittance begins at ' + timestr, yellow, 1)
    while str(datetime.datetime.now()) < timestr:
        os.system('sleep 1')
    while cydict['count'][2]:
        os.system('sleep 2')
        os.system('clear')
        print (hilite(appName + ' ' + versionString[:6], blue, 0))
        print (hilite('powered by MPSTME GNU/Linux User Group', blue, 0))
        print hilite(str(cydict['count'][2]) + ' spot(s) remaining', yellow, 1)
        inputstr = raw_input(hilite('Phone number:\n', blue, 1))
        if inputstr == 'konsbn,':
            return 0
        inputstr = inputstr.strip()
        match = re.search(r'\d{10}', inputstr)
        if not match or len(inputstr) is not 10:
            print hilite('Invalid number!', red, 1)
        else:
            if inputstr in cydict:
                if cydict[inputstr][1]:
                    print hilite('Identification already completed for: ' +  
                        inputstr, yellow, 1)
                else:
                    cydict['count'] = (
                        cydict['count'][0],
                        cydict['count'][1] + 1,
                        cydict['count'][2] - 1,
                        cydict['count'][3]
                        )
                    cydict[inputstr] = (
                        cydict[inputstr][0],
                        cydict['count'][1],
                        str(datetime.datetime.now())
                        )
                    print hilite('You have succesfully identified as: ' + 
                        cydict[inputstr][0], green, 1)
                    writebak(cydict)
            else:
                print hilite('No entry found corresponding to: ' + 
                    inputstr, red, 1)
                regnew(cydict, inputstr)
    while True:
        os.system('clear')
        inputstr = raw_input(hilite('Admittance Closed!', yellow, 1))
        if inputstr == 'konsbn,':
            return 0

def main():
    if (len(os.sys.argv)==4 and os.sys.argv[1]=='0') or\
    (len(os.sys.argv)==2 and os.sys.argv[1]=='1'):
        if not int(os.sys.argv[1]):
            cydict = extractFromCSV(os.sys.argv[2])
        else:
            cydict = loadbak()
        if(cydict):
            loginMode(cydict)
        debugMode(cydict)
    else:
        print ('Usage: \nattendance mode[1=reload] \
            \nattendance mode[0=init] csv_file_name spots')

if __name__ == '__main__':
    main()

# [number] -> (name, attn_seq, timestamp)