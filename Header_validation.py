import pandas as pd
from itertools import chain
import xlsxwriter
import os
import csv
import sys
import pandas as pd
import codecs
import datetime
#Print()
source_file = list()
target_file = list()
mapping = list()
results = list()

currentDT = datetime.datetime.now()

start = currentDT
print ('validationstarttime-'+ str(currentDT))

result_path = input('Enter the resultpath :\n')
sourcefile=input('Enter the Source file name:\n')
df = pd.read_excel(sourcefile,sep='|')
name=input('Enter column Name')

df0=df[df["Output"].isin([name])]
df1=df0['Extract File Header'].str.split(',')
df2=pd.DataFrame({
'0' : list(chain.from_iterable(df1.tolist()))})
print('Headers in Dictonary:',df2)
df2=df2.to_csv('Header_dict.csv',index=False)

a=open('Header_dict.csv',encoding='utf-8')
sf=csv.reader(a)
targetfile=input('Enter the target file name:\n')
df = pd.read_csv(targetfile,sep='|',index_col=False)
df3=list(df.columns.values)
df4=pd.DataFrame(df3)
df5=df4.to_csv('Header_from_file.csv',index=False)

print('Headers in File: ',df4)
b=open('Header_From_file.csv',encoding='utf-8')
tf=csv.reader(b)
matchcount=0
count=1
mismatchcount=0
totalmatch=0
sdict=dict()
tdict=dict()
for line in sf:
    if str(line) in sdict:
        count=sdict[str(line)]
        count=count+1
        sdict[str(line)]=count
        count=1
    else:
        sdict[str(line)]=count
count=1
for line1 in tf:
    if str(line1) in tdict:
        count=tdict[str(line1)]
        count=count+1
        tdict[str(line1)]=count
        count=1
    else:
        tdict[str(line1)]=count
result_file=open(result_path+"Mismatch.txt",'w',newline='')
for k,v in sdict.items():
    if k in tdict:
        if v==tdict[k]:
            matchcount=matchcount+v
        elif v>tdict[k]:
            matchcount=matchcount+tdict[k]
            mismatchcount=mismatchcount+(v-tdict[k])
            st=(str(k).strip('[]')).replace('\'','')
            result_file.write('\n Difference in count for the below record\n'+st+'\nsource:'+str(v)+' Tatget:'+str(tdict[k]))
        else:
            matchcount=matchcount+v
            mismatchcount=mismatchcount+(tdict[k]-v)
            st=(str(k).strip('[]')).replace('\'','')
            result_file.write('\n Difference in count for the below record\n'+st+'\nsource:'+str(v)+' Tatget:'+str(tdict[k]))
    else:
        #print(k)
        st=(str(k).strip('[]')).replace('\'','')
        mismatchcount=mismatchcount+1
        result_file.write('\nMismatched record:'+str(st.encode('utf-8')))
print("file mismatch summary"+'-matched row count:',matchcount,'Mismatched row count:',mismatchcount)
currentDT = datetime.datetime.now()
print ('validationendtime-'+ str(currentDT))
end = currentDT
print('duration:'+ str(start-end))
result_file.write('matched row count:'+str(matchcount)+'Mismatched row count:'+str(mismatchcount))


