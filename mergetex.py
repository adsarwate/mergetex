#!/usr/bin/python

# mergetex.py
#
# Script for merging tex files into a single monolithic file.  This
# script should make it easy to generate an ArXiV-friendly single
# .tex file from a paper that is broken into subfiles using LaTeX's
# \input{} command.
#
# USAGE:
#     python mergetex.py  [input]  [output]
#     python mergetex.py  mypaper.tex  mypaperMerged.tex
#
# mergetex takes two arguments, the [input] file and the [output]
# file into which the merged files should go.  It recursively
# searches [input] and adds any file given by uncommented \input{}
# commands.
#
#
#
# v0.1 by Anand Sarwate (asarwate@alum.mit.edu)

import argparse
import string
import re
import sys
import os.path


def parseinclude(includefile,outfh):
    try:
        with open(includefile) as file:
            print("Found " + includefile + ".  Merging...\n")
    except IOError as e:
        print('Unable to open ' + includefile + ': does not exist or no read permissions')

    fincl = open(includefile, 'r')

    # parse file line by line
    for line in fincl:
        
        # strip out comments in the line, if any
        dc = line.split('\\%')       # look for escaped \%
        if (len(dc) == 1):           # then there is no \% to be escaped
            first_comm = dc[0].find('%')
            if (first_comm == -1):
                decom = line
            else:
                decom = line[:(first_comm+1)] + '\n'
        else: # we had to escape a \%
            decom = ""               # construct the uncommented part
            dc = line.split('%')
            for chunk in dc:  # look in each chunk to see if there is a %
                if (chunk[-1] == '\\'):  # if % is escaped...
                    decom = decom + chunk + '%'
                else:
                    if (chunk[-1] == '\n'):
                        decom = decom + chunk
                    else:
                        decom = decom + chunk + '%\n'
                    break

        # search for the line containing an \input{} command
        sec = re.match('\\\\input{(.*?)}', decom)
        if sec:
            # if the match is nonempty, then
            fname = re.sub('\\\\input{', '', sec.group(0))
            fname = re.sub('}', '', fname)
            if (fname.find('.tex') == -1):
                fname = fname + '.tex'
                
            print('\tFound include for ' + fname + '\n')
            parseinclude(fname,outfh)
            
        # if no \input{},  print the line to the output file
        else:
            outfh.write(decom)

    fincl.close()


# input argument parser
#    args.format will contain filename for format file
#    args.bibfile will contain filename of bibliography
inparser = argparse.ArgumentParser(description='Parses argument list')
inparser.add_argument('texfile', metavar='texfile', help='main .tex file')
inparser.add_argument('output', metavar='output', help='desired target output file')
args = inparser.parse_args()


# INPUT PARSING AND WARNING GENERATION
try:
    with open(args.texfile) as file:
        pass
except IOError as e:
    print('Unable to open ' + args.texfile + ': does not exist or no read permissions')

fin = open(args.texfile, 'r')
fout = open(args.output, 'w')

parseinclude(args.texfile,fout)    
      

    
