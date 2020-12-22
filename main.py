#!/usr/bin/env python3

from pprint import pprint
from urllib.parse import urlparse
from optparse import OptionParser, OptionValueError

def Convert(a):
    """convert a list to dict"""
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct

def uri_validator(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

def print_stats(source):
    for key, value in source.items():
        length = str(len(value))
        print(key + ' -> ' + length + ' item' if length == "1"\
             else key + ' -> ' + length + " items")

usage = "usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-o", "--output",
                action="store_true", dest="file_name",
                help="write to files")

(options, args) = parser.parse_args()

file = open('input.txt', 'r')
lines = file.readlines()
file.close

# remove trailing lines
lines_w_o_trailing_newline = []
for line in lines:
    if line != '\n':
        lines_w_o_trailing_newline.append(line.rstrip())

# sort
netlocs = []
for line in lines_w_o_trailing_newline:
    if uri_validator(line):
        netloc = (urlparse(line)).netloc
        if not (netloc == '') or not (netloc == '\n'):
            if netloc not in netlocs:
                netlocs.append(netloc)
                netlocs.append([])
                netloc_idx = netlocs.index(netloc)
                url = (urlparse(line)).geturl()
                (netlocs.__getitem__(netloc_idx+1)).append(url)
            else:
                netloc_idx = netlocs.index(netloc)
                url = (urlparse(line)).geturl()
                (netlocs.__getitem__(netloc_idx+1)).append(url)

# cpnvert to dict
netlocs_dict = Convert(netlocs)

#print_stats(netlocs_dict)

if options.file_name:
# write to separate files
    for key in netlocs_dict:
        print(key)
        output = open("input_" + key + ".txt", 'w')
        output_list = netlocs_dict[key]
        for line in output_list:
            output.write(line + "\n")
        output.close
