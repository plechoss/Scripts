## Run from a directory that contains a dir named 'Films'
## TODO: run with a path argument
## Assumes names don't contain numerical years in them for now
## Puts loose files in directories
## Renames directiories to the format "NAME (YEAR) [QUALITY]"

from os import listdir, rename, mkdir
from os.path import isfile, isdir, join

import numpy as np
import re

mypath = "./Films"

qualities = np.array(['2160p','1080p', '720p', '480p', 'bdremux', 'dvdrip', 'bdrip', 'uhd'])
qualities_nice = ['2160p','1080p', '720p', '480p', 'BDRemux', 'DVDRip', 'BDRip', 'UHD']

bad_characters = [',','.','_','(','[']

files = [f for f in listdir(mypath) if (isfile(join(mypath, f)) and f[0]!='.')]
dirs = [f for f in listdir(mypath) if (isdir(join(mypath, f)) and f[0]!='.')]

def get_quality(filename):
    filename_lower = filename.lower()

    quality_booleans = np.array(list(map(lambda x: x in filename_lower, qualities)))
    quality = 'X' if (True not in quality_booleans) else qualities_nice[np.nonzero(quality_booleans)[0][0]]
    return quality

def get_year(filename):
    year = re.search('(19|20)\d{2}', filename)
    year = year.group(0) if (year != None) else 'X'
    return year

def get_new_dir_name(filename):
    year = get_year(filename)
    quality = get_quality(filename)

    suffix = "(%s) [%s]" % (year, quality)
    delimiter = year + "|" + quality
    name = re.split(delimiter,filename)[0]

    for character in bad_characters:
        name = name.replace(character,' ')
    name = re.sub(' +', ' ',name)

    return name + suffix

for folder in dirs:
    new_name = get_new_dir_name(folder)
    while(isdir(new_name)):
        new_name = new_name + '_'
    rename(join(mypath, folder), join(mypath, new_name))

for filename in files:
    dir_name = get_new_dir_name(filename)
    while(isdir(dir_name)):
        dir_name = dir_name + '_'
    mkdir(join(mypath, dir_name))
    rename(join(mypath, filename), join(join(mypath, dir_name), filename))
