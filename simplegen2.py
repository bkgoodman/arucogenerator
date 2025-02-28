#!/usr/bin/python3
import json


""" 
This is a stupid command line tool to generate markers
"""


def getbits(b):
    s = " \u2588\u2588 "
    for x in range(0,4):
        if (0x08>>x) & b:
            s += "\u2588"
        else:
            s += " "
    s += " \u2588\u2588 "
    return s


def gencode(code,codetype):
    markerwidth={
        "aruco":5,
        "4x4_1000":4,
        "5x5_1000":5,
        "6x6_1000":5,
        "7x7_1000":7
}
    print (" \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588")
    print (" \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588")
    print (" \u2588\u2588      \u2588\u2588")

    codewidth = markerwidth[codetype]
    byts=ardict[codetype][code]
    for y in range(0,codewidth):
        s=""
        for x in range(0,codewidth):
            bitnum = y * codewidth + x
            byte = byts[bitnum>>3]
            bt = byts[bitnum>>3] & (0x80>>bitnum%8)
            if (bt):
                s += "\u2588"
            else:
                s += " "
        print (f" \u2588\u2588 {s} \u2588\u2588")

    print (" \u2588\u2588      \u2588\u2588")
    print (" \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588")
    print (" \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588")

import sys
if __name__ == "__main__":
    global ardict
    fd = open("dict.json")
    ardict = json.load(fd)
    fd.close()
    gencode(int(sys.argv[1]),"4x4_1000")
