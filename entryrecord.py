import logging
import sys
import os
import MySQLdb as mdb
from globals import *

#Maps to a single row of data in the main_entry table in the database.
class EntryRecord():
    
    def __init__(self):
        self._entry_id = 0
        self._entry_type_id = 0
        self._entry_name = ''
        self._profile_url = ''
        self._entry_job_title = ''
        self._entry_location = ''
        self._entry_region = ''
        self._scrape_date = ''
        self._semi_known_main_entry_id = 0
        self._shares_groups = False;
        self._shares_connections = False;
    
    @property
    def entry_id(self):
        return self._entry_id
    
    @property
    def entry_type_id(self):
        return self._entry_type_id

    @entry_type_id.setter
    def entry_type_id(self, value):
        self._entry_type_id = value
    
    @property
    def entry_name(self):
        return self._entry_name

    @entry_name.setter
    def entry_name(self, value):
        self._entry_name = value

    @property
    def profile_url(self):
        return self._profile_url

    @profile_url.setter
    def profile_url(self, value):
        self._profile_url = value

    @property
    def entry_job_title(self):
        return self._entry_job_title.replace("'", "")

    @entry_job_title.setter
    def entry_job_tite(self, value):
        self._entry_job_title = value

    @property
    def entry_location(self):
        return self._entry_location.replace("'", "")

    @entry_location.setter
    def entry_location(self, value):
        self._entry_location = value

    @property
    def entry_region(self):
        return self._entry_region.replace("'", "")

    @entry_region.setter
    def entry_region(self, value):
        self._entry_region = value

    @property
    def scrape_date(self):
        return self._scrape_date

    @property
    def semi_known_main_entry_id(self):
        return self._semi_known_main_entry_id

    @semi_known_main_entry_id.setter
    def semi_known_main_entry_id(self, value):
        self._semi_known_main_entry_id = value

    @property 
    def shares_groups(self):
        return int(self._shares_groups)

    @shares_groups.setter
    def shares_groups(self, value):
        self._shares_groups = value

    @property
    def shares_connections(self):
        return int(self._shares_connections)

    @shares_connections.setter
    def shares_connections(self, value):
        self._shares_connections = value

    def __repr__(self):
        return """[EntryRecord: main_entry_id={0}, entry_type_id={1}, entry_name={2}, profile_url={3}, entry_job_title={4}, entry_location={5}, 
                entry_region={6}, semi_known_main_entry_id={7}, shares_groups={8}, shares_groups={9}]""".format(self.entry_id, self.entry_type_id, self.entry_name, self.profile_url, self.entry_job_title, self.entry_location, self.entry_region, self.semi_known_main_entry_id, self.shares_groups, self.shares_connections)

    def save(self):
            
            logger = logging.getLogger(LOG_NAME)

            con = None

            sql = """INSERT INTO main_entry (entry_type_id, entry_name, profile_url, 
            entry_job_title, entry_location, entry_region, semi_known_main_entry_id, 
            shares_groups, shares_connections)
            VALUES
            (
                {0},
                {1},
                {2},
                {3},
                {4},
                {5},
                {6},
                {7},
                {8}
            )""".format(self.entry_type_id, self.format_sql_string(self.entry_name), self.format_sql_string(self.profile_url), self.format_sql_string(self.entry_job_title)                       ,self.format_sql_string(self.entry_location), self.format_sql_string(self.entry_region), self.semi_known_main_entry_id, self.shares_groups, 
                        self.shares_connections)    
            
            try:
                
                con = mdb.connect(DB_SERVER, DB_USER, DB_PWD, DB_NAME)

                with con:
                    cur = con.cursor()
                    logger.info("Saving Entry Record.  SQL = '" + sql + '"')
                    cur.execute(sql)
                    rowid = cur.lastrowid
                    logger.info("Saving Entry Record Complete.  Main Entry ID ='" + str(rowid) + "'")
                    return rowid

            except:
                logger.error(sys.exc_info()[0])
                raise

            finally:
                if con:
                    con.close()

    def format_sql_string(self, sql_string):
        if sql_string == '' or sql_string == None:
            return " NULL" 
        else:
            return "'" + sql_string.replace("'", "''").strip() + "'"
