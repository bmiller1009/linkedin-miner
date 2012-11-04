import logging
from crawler import Crawler
from globals import LINKEDIN_URL, LOG_NAME
from logger import Log

#Sample Driver class to run the crawler
def main():
    
    Log.initialize()
    
    logger = logging.getLogger(LOG_NAME)

    logger.info("Begin Scraping...")
    main_url = '{0}wvmx/profile'.format(LINKEDIN_URL)
    
    try:
        crawler = Crawler() 
    except IOError as exc:
        raise IOError("Construction of Crawler object failed due to a " + \
                      "problem with the cookie file", exc.strerror)
    else:
        html = crawler.post(main_url)    
        crawler.save_contacts(html)
        logger.info("Scraping Complete")

if __name__ == "__main__":
        main()
