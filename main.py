import logging
import os
import sys
from crawler import Crawler
from globals import LINKEDIN_URL, LOG_NAME
from datetime import datetime
from logging.handlers import RotatingFileHandler

#Sample Driver class to run the crawler
def main():
   
    initialize()

    logger = logging.getLogger(LOG_NAME)
    
    try:
        
        logger.info("Begin Scraping...")
        main_url = LINKEDIN_URL + 'wvmx/profile'
        crawler = Crawler() 
        crawler.post(main_url, None)		
    
    except:
        logger.error(sys.exc_info()[0])
        raise
    
    finally:
        logger.info("Scraping Complete")

#Initialize the log
def initialize():
    
    #Create Log folder
    log_dir = 'Log'
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    
    #Create folder for this particular scrape 
    today = datetime.today()
    
    format_time = lambda time_element: len(str(time_element)) == 1 and '0' + str(time_element) or str(time_element)
                                            
    #Folder formatting
    hour = format_time(today.hour)
    minute = format_time(today.minute)
    second = format_time(today.second)

    folder_name = 'DailyScrape_' + str(today.month) + '.' + str(today.day) + '.' + str(today.year) + '_' + hour + '.' + minute + '.' + second
                                                                                                                
    #scrape directory run
    scrape_dir = log_dir + '/' + folder_name
    if not os.path.isdir(scrape_dir):
        os.mkdir(scrape_dir)
    
    log = logging.getLogger(LOG_NAME)
    log.setLevel(logging.DEBUG)

    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s :: %(message)s")

    #Set up text logger
    txt_handler = RotatingFileHandler(log_dir +'/' + folder_name + '/' + 'Log.txt', backupCount=5)
    txt_handler.setFormatter(log_formatter)
    log.addHandler(txt_handler)

    #Set up screen logger
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    log.addHandler(console_handler)
    
    log.info("Logger initialized.")

if __name__ == "__main__":
        main()
