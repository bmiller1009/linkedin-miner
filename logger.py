import os
import logging
from logging.handlers import RotatingFileHandler
from globals import LOG_FILE_PATH, LOG_NAME, DIR_PREFIX, LOG_FORMAT, LOG_FILE
from datetime import datetime

class Log():    
    
    @staticmethod
    def initialize():
        
        log_dir, folder = Log.__build_folders()
        
        log = logging.getLogger(LOG_NAME)
        log.setLevel(logging.DEBUG)
    
        log_formatter = logging.Formatter(LOG_FORMAT)
    
        #Set up text logger
        txt_handler = RotatingFileHandler('{0}/{1}/{2}'.format(log_dir, 
                                            folder, LOG_FILE), backupCount=5)
        
        txt_handler.setFormatter(log_formatter)
        log.addHandler(txt_handler)
    
        #Set up screen logger
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        log.addHandler(console_handler)
        
        log.info("Logger initialized.")
    
    @staticmethod
    def __build_folders():
        #closure for date format
        def format_time(time_element):
            if len(str(time_element)) == 1:
                return '0{0}'.format(str(time_element))
            else:
                return str(time_element)
        
        #Create Log folder
        log_dir = '{0}Log'.format(LOG_FILE_PATH)
        if not os.path.isdir(log_dir):
            os.mkdir(log_dir)
        
        #Create folder for this particular scrape 
        today = datetime.today()
        
        #TODO:  Clean this up
        folder = DIR_PREFIX + str(today.month) + '.' + str(today.day) + \
                    '.' + str(today.year) + '_' + format_time(today.hour) + \
                    '.' + format_time(today.minute) + '.' + \
                    format_time(today.second)
                                                                                                                                  
        #scrape directory run
        scrape_dir = '{0}/{1}'.format(log_dir, folder)
        if not os.path.isdir(scrape_dir):
            os.mkdir(scrape_dir)
            
        return log_dir, folder