import os
import csv
jfiles=list()
import pandas as pd
extension=[".dat",".DAT"]

#please enter the folder Name in the below variable
srcfilepath ="C:\\Users\\nahmed\\Documents\\GitHub\\Greece_PythonRepo\\Source"

os.chdir(srcfilepath)
for root,dirs,files in os.walk(srcfilepath):
    for file in files:
        if file.endswith(tuple(extension)):
            jfiles.append(file)
            print(file)

            df = pd.read_csv(file,sep="|", quotechar='"', decimal=",",low_memory=False,encoding='UTF-8')

            mask = df.duplicated()
            #print(df[mask])
            count=0
            df_dup=pd.DataFrame(df[mask])
            count=count+1
            print('No.of Rows in '+file+': ',df.shape[0])

            if (df[mask].shape[0])>0:
                print('Duplicates Found : Yes')

                file_write=df_dup.to_csv(file[:-4]+'_Duplicates.txt',index=0,sep="|")

                print('No.of Duplicate Records in file: ',df[mask].shape[0])
            else:
                print('Duplicates Found : No')

count=len(jfiles)
print('No.of files in Folder:',count)
