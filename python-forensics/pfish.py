############################################
# p-fish: Python File System Hash Program
# Author: Krishna Balam
# Creation Date: March 30th, 2015
# Version 1.0
############################################

import logging  # Python standarad library Logger
import time     # Python standarad library time functions
import sys      # Python standarad library for system specific parameters
import _pfish   # Support modules for pfish 


if __name__ = '__main__':
    
    # define pfish version constant. change when version changes
    PFISH_VERSION = '1.0'
    
    # turn on logging
    logging.basicConfig(filename="pFishLog.log", level=logging.DEBUG, format='%(asctime)s | %(levelname)s | %(messgae)s')
    
    # process command line arguments
    _pfish.ParseCommandLine()
    
    # Record Starting Time
    startTime = time.time()
    
    # Record welcome message
    logging.info('')
    logging.info('Welcome to p-Fish version ' + PFISH_VERION + ' ...')
    logging.info('New Scan started...')
    logging.into('')
    
    _pfish.DisplayMessage('Welcome to p-Fish... version ' + PFISH_VERSION)
    _pfish.DisplayMessage('New scan has started ...')
    
    # Record some information regarding system
    logging.info('System: ' + sys.platform)
    logging.info('Version: ' + sys.version)
    
    # Traverse file system directories and hash the files
    filesProcessed = _pfish.WalkPath()
    
    # Record end time and calculate duration
    endTime = time.time()
    duration = endTime - startTime
    
    logging.info("Files processed: " + str(filesProcessed))
    logging.info("Elapsed time: " + str(duration) + " seconds")
    logging.info('')
    
    logging.info("Program finished normally")
    logging.info('')
    
    _pfish.DisplayMessage("Program End")   