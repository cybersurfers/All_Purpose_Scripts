#!/usr/bin/env python3

'''
Sometimes the PDFs you receive have pesky watermarks on them.  If you get tired of the watermarks, 
use this script to (hopefully) remove them.
'''

import sys
import os
import textwrap

def containspattern(line, patterns):
    for pattern in patterns:
        if pattern.encode() in line:
            return True


def cleanpdf(source, destination, patterns):
    f = open(source, 'r+b')
    lines = f.readlines()
    f.close()

    #Find all occurences of the watermark(s)
    alloccurences = [number for (number, line) in enumerate(lines) if containspattern(line, patterns)]
    toremove = []

    for number in alloccurences:
        #Find beginning of watermark
        begin = None
        i = number
        while i > 0 and not begin:
            i = i-1
            if 'BT'.encode() in lines[i]:
                begin = i
        if not begin:
            sys.exit('Beginning of watermark not found')
        #Find end of watermark
        end = None
        j = number
        while j < len(lines)-2 and not end:
            j = j+1
            if 'ET'.encode() in lines[j]:
                end = j
        if not end:
            sys.exit('End of watermark not found')
        # Add to list of where to replace with blank lines
        toremove.append((begin, end))  

    bytesremoved = 0
    for (begin, end) in toremove:
        for k in range(begin, end+1):
            size = len(lines[k])
            bytesremoved = bytesremoved + size
            lines[k] = ''.encode()

    if bytesremoved > 0:  # If no watermark was found, no output is written
        g = open(destination, 'w+b')
        for line in lines:
            g.write(line)
        g.close()
    return(bytesremoved, len(toremove))


if len(sys.argv) < 4:
    line1 = f"Usage:\n\t{sys.argv[0]} inputfile outputfile pattern1 ... patternN"
    line2 = "To update the PDF instead of creating a new one, provide the same value for inputfile and outputfile."
    line3 = f"Example:\n\t{sys.argv[0]} test.pdf test-clean.pdf 'stupid watermark' 'copyright of' 'crap company' '192.168.1.1'"
    sys.exit(f"\n\n{line1}\n\n{line2}\n\n{line3}\n\n")
    
source = sys.argv[1]
destination = sys.argv[2]
patterns = sys.argv[3:]

uncompress = os.system(f'pdftk {source} output {source+"-tmp"} uncompress')
if uncompress != 0:
    sys.exit('Unable to uncompress the PDF')

(bytesremoved, nremoved) = cleanpdf(source+'-tmp', destination+'-tmp', patterns)
if nremoved > 0:
    compress = os.system(f'pdftk {destination+"-tmp"} output {destination} compress')
    if compress != 0:
        sys.exit('Unable to compress the PDF')

    os.remove(source+'-tmp')
    if source != destination:
        os.remove(destination+'-tmp')
    print(f'Found {nremoved} patterns in file {source}, removing {bytesremoved} bytes')
else:
    os.remove(source+'-tmp')
