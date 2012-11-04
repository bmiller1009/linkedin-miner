import logging
import sys
import MySQLdb as mdb
from globals import DB_SERVER, DB_USER, DB_PWD, DB_NAME, LOG_NAME

#Maps to a single row of data in the main_entry table in the database.
class EntryRecord():
    
    def __init__(self):
        self.entry_id = 0
        self.entry_type_id = 0
        self.entry_name = ''
        self.profile_url = ''
        self.job_title = ''
        self.location = ''
        self.region = ''
        self.scrape_date = ''
        self.semi_known_main_entry_id = 0
        self.shares_groups = False;
        self.shares_connections = False;

    def __repr__(self):
        return """[EntryRecord: main_entry_id={0}, entry_type_id={1}, 
        entry_name={2}, profile_url={3}, entry_job_title={4}, 
        entry_location={5}, entry_region={6}, semi_known_main_entry_id={7}, 
        shares_groups={8}, shares_groups={9}]""".format(self.entry_id, 
                                self.entry_type_id, 
                                self.entry_name, self.profile_url, 
                                self.job_title, self.location, 
                                self.region, self.semi_known_main_entry_id, 
                                self.shares_groups, self.shares_connections)

    def save(self):
        
        def format_sql_string(sql_string):
            if sql_string == '' or sql_string == None:
                return " NULL" 
            else:
                return "'" + sql_string.replace("'", "''").strip() + "'"
        
        logger = logging.getLogger(LOG_NAME)
        
        con = None
        
        sql = """INSERT INTO main_entry (entry_type_id, entry_name, 
        profile_url, entry_job_title, entry_location, entry_region, 
        semi_known_main_entry_id, shares_groups, shares_connections)
        VALUES ({0},{1},{2},{3},{4},{5},{6},{7},{8})""".format(
                            self.entry_type_id, 
                            format_sql_string(self.entry_name), 
                            format_sql_string(self.profile_url), 
                            format_sql_string(self.job_title),
                            format_sql_string(self.location), 
                            format_sql_string(self.region), 
                            self.semi_known_main_entry_id, self.shares_groups, 
                            self.shares_connections)    
        
        #Throw a better error here and look at the calls made to this function
        try:
            
            con = mdb.connect(DB_SERVER, DB_USER, DB_PWD, DB_NAME)
        
            with con:
                cur = con.cursor()
                logger.info("Saving Entry Record.  SQL = '" + sql + '"')
                cur.execute(sql)
                rowid = str(cur.lastrowid)
                logger.info("""Saving Complete. ID ='{0}'""".format(rowid))
                return rowid
        
        except:
            logger.error(sys.exc_info()[0])
            raise
        
        finally:
            if con:
                con.close()