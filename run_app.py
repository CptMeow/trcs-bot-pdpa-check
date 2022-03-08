import mysql.connector as mysql
import os
import pandas as pd
import subprocess
from mysql.connector import Error
from os.path import exists

output = "CMD_ALL_SITE_OUTPUT.csv"
#Check output exists
if exists(output) :
    print("Output exists. deleted")
    os.remove(output)

#Start scrapy crawl
print("Start: BOT")
subprocess.call(["scrapy", "crawl", "allsite", "-O", output])
print("End: BOT")

#Check output exists to mysql
if exists(output) :
    print("Start: Import to database")
    empdata = pd.read_csv(output, index_col=False, delimiter = ',')
    try:
        conn = mysql.connect(host='localhost', database='cyber', user='root', password='')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()

            #loop through the data frame
            for i,row in empdata.iterrows():
                row = row.where((pd.notnull(row)), None)
                sql = "INSERT INTO `pdpa_check` (`domain`, `css`, `id`, `name`, `text`, `url`, `dataset_date`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, tuple(row))
                conn.commit()
            print("End: Import to database")
            
    except Error as e:
        print("Error while connecting to MySQL", e)
else :
    print("Output not exist")