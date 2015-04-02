############################################
# p-fish support functions: Where all the work gets done
# Author: Krishna Balam
# Creation Date: March 30th, 2015
# Version 1.0
# functions:
# DisplayMessage()  ParseCommandLine()  WalkPath()
# HashFile()        class_CSVWriter     ValidateDirectory()
# ValidateDirectoryWritable()
############################################

import os             # Python standard library for os functions
import stat           # Python standard library functions for interpreting os results
import time           # Python standard library for time functions
import hashlib        # Python standard library for secure hashes and message digests
import argparse       # Python standard library for argument parsing
import csv            # Python standard library for csv file functions
import logging        # Python standard library for logging

# Get logger from main pfish program

log = logging.getLogger(name = 'main._pfish')

# now the functions

#
# Function name: ParseCommand()
# Description: Define command line arguments and then process and validate them when supplied
# Input: None

# Actions: uses standard library argparse to process the command line arguments
#          establishes global variable gl_args for arguments
#          any function then can obtain the information about arguments

def ParseCommanLine():
    
    # define an object of type parser 
    parser = argparse.ArgumentParser(description="Argument parser for python file system hashing.. p-fish")
    
    # add argument verbose to the parser to give user ability to see verbose execution messages
    parser.add_argument('-v', '--verbose', action='store_true', help='allows prograss messages to be displayed')
    
    # setup a mutually exclusive group for hashing alogrithm that can be selected by the user
    group = parser.add_mutually_exclusive_group(required=True)
    
    # add md5 algorithm option 
    group.add_argument('--md5', help='specifies MD5 algorithm', action='store_true')
    # add sha256 algorithm option
    group.add_argument('--sha256', help='specifies SHA256 algorithm', action='store_true')
    # add sha512 algorithm option
    group.add_argument('--sha512', help='specifies SHA512 algorithm', action='store_true')