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
#"w",newline=''
source_folder =input('Enter the sourcefile path with name :\n')
target_folder =input('Enter the Targetfile path with name :\n')
result_path = input('Enter the resultpath :\n')
#codecs.open(source_folder, 'rU', 'utf-16')

currentDT = datetime.datetime.now()

print ('validationstarttime-'+ str(currentDT))
start = currentDT
s = open(source_folder,  encoding = 'utf-8',newline='')
t = open(target_folder, encoding = 'utf-8',newline='')

df = pd.read_csv(s,sep="|", quotechar='"', decimal=",",low_memory=False,index_col=0)
sourcefile1=input('enter File Name to convert sourceFile: ')
df1=df.to_csv(sourcefile1, sep='|', encoding='utf-8', quotechar='"', decimal='.',index=False)
#print(df1)
a=open(sourcefile1,encoding='utf-8')
sf=csv.reader(a)
mask=df1.duplicated()

df = pd.read_csv(t,sep="|", quotechar='"', decimal=",",low_memory=False,index_col=0)

targetfile1=input('enter File Name to convert TargetFile: ')
print(sourcefile1)
print(targetfile1)
df2=df.to_csv(targetfile1, sep='|', encoding='utf-8', quotechar='"', decimal='.',index=False)
mask2=df2.duplicated()
b=open(targetfile1,encoding='utf-8')
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
print('------------Duplicate Check-------------------')
print('the No.of Records which are duplicate in source file:',df[mask].shape)
print('The actual Record count in the source  file: ',df1.shape)



print('the No.of Records which are duplicate in target file:',df[mask1].shape)
print('The actual Record count in the target  file: ',df2.shape)
currentDT = datetime.datetime.now()
print ('validationendtime-'+ str(currentDT))
end = currentDT
print('duration:'+ str(start-end))
result_file.write('matched row count:'+str(matchcount)+'Mismatched row count:'+str(mismatchcount))
