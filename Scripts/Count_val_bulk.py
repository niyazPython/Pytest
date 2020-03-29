import cx_Oracle
import jaydebeapi
import jpype
import codecs
import csv
import datetime
import re
from collections import defaultdict
import pandas as pd
import pyodbc

result_path='H:/Desktop/'
source_table = list()
target_table = list()
only_in_source = list()
only_in_target = list()
result_sum = list ()
mapping = list()
source_schema = input("please enter the source schema name ")
target_schema = input("please enter the target schema name ")
def Dbconnection():
    global target_con
    global source_con
    dbuser='r3_nahmed'
    dbpass='Work9#aig'
    dbhost='a2ec702c1-scan.us2.ocm.s7130945.oraclecloudatcustomer.com'
    dbport='1521'
    dbserv='sgicdhq'
    oracle_connectsting=str(dbuser+'/'+dbpass+'@'+dbhost+':'+dbport+'/'+dbserv)
    source_con = cx_Oracle.connect(oracle_connectsting)
    print ("Source is connected")
    s_dbuser='r3_nahmed'
    s_dbpass='Work9#aig'
    s_dbhost='a2ec702c1-scan.us2.ocm.s7130945.oraclecloudatcustomer.com'
    s_dbport='1521'
    s_dbserv='sgicdhq'
    oracle_connectstring=str(s_dbuser+'/'+s_dbpass+'@'+s_dbhost+':'+s_dbport+'/'+s_dbserv)
    target_con=cx_Oracle.connect(oracle_connectstring)
    print ("target is connected")

    source_query = "select table_name from all_tables where owner='"+ source_schema+"'"
    target_query = "select table_name from all_tables where owner='"+ target_schema+"'"
    source_cursor=source_con.cursor()
    target_cursor= target_con.cursor()
    source_cursor.execute(source_query)
    target_cursor.execute(target_query)
    for i in source_cursor:
        source_table.append(i[0])

    for i in target_cursor:
        target_table.append(i[0])
    schema_mapping(source_table,target_table)

def schema_mapping(source_table,target_table):
        for x in source_table:
            for y in target_table:
                if x == y:
                    mapping.append(x)
        only_in_source = [ element for element in source_table if element not in target_table]
        only_in_target = [ element for element in target_table if element not in source_table]

        print("No of table in source schema", len(source_table))
        print("No of table in target schema", len(target_table))

        count_check(mapping)

def count_check(mapping):
    source_cursor=source_con.cursor()
    target_cursor= target_con.cursor()
    for i in  mapping:
        try:
            source_cursor.execute("select count(*) from "+source_schema+"."+i)
            x = source_cursor.fetchall()
            target_cursor.execute("select count(*) from "+target_schema+"."+i)
            v = target_cursor.fetchall()
            result_sum.append([i,x[0][0],v[0][0]])

        except(ValueError):
            continue

Dbconnection()
df=pd.DataFrame(result_sum,columns=["Tablename", "source_count", "Target_count"])
df['count_result'] = df.source_count == df.Target_count
df.to_csv(result_path +'Result_summary.csv')
with open(result_path +'Result_summary.csv','a') as fd:
    fd.write("table present only in source schema")
    if len(only_in_source) > 0:
        fd.write("table present only in source schema")
        df3 = pd.dataframe(only_in_source,columns=["only_in_source"])
        df3.to_csv(fd)
    if len(only_in_target) > 0:
        fd.write("table present only in target schema")
        df4 = pd.dataframe(only_in_target,columns=["only_in_target"])
        df4.to_csv(fd)
fd.close()
source_con.close()
target_con.close()
print(df[["Tablename", "source_count", "Target_count", "count_result"]])
