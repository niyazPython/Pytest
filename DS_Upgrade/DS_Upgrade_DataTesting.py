import codecs
import csv

result_path='//PW7AM1XDPC22147/Jenkins_Test/DS_Upgrade/'

def comparefile():
    sfile=codecs.open(result_path+'11.5.csv','r')
    tfile=codecs.open(result_path+'11.7_TASSIGNMENT_REPORT.csv','r')
    database_set = dict()
    colnames=dict()
    a=0
    i=0
    j=0
    k=0
    row=list()
    rlist=list()
    mismatch=0
    mismatchcount=0
    matchcount=0
    f=open(result_path+'TASSIGNMENT_REPORT_Comparsion.txt','w')
    src_csv=csv.reader(sfile)
    tgt_csv1=csv.reader(tfile)
    for r in src_csv:
        for l in r:
            colnames[i]=l
            i=i+1
        sfile.seek(0)
        break
    for rline in tfile:
        #print('\n',rline)
        j=j+len(rline)+1
        rline=rline.strip('\n')
        rows=rline.split(',',)
        database_set[rows[0]] =k
        k=j

    for line in src_csv: #csv.reader((line4.replace('\0','') for line4 in sfile)):
        if line[0] in database_set:
            j= database_set[line[0]]
            tfile.seek(j)
            row=tgt_csv1.__next__()
            a=(len(row)-1)
            while(a>-1):
                if (line[a]==row[a]):
                    a=a-1
                else:
                    f.write('\nMismatch in row:'+line[0]+' column number:'+colnames[a]+' '+line[a]+' '+row[a])
                    mismatch=mismatch+1
                    a=a-1
            if mismatch>0:
                f.write('\nRow:'+line[0]+' mismatched')
                mismatchcount=mismatchcount+1
                mismatch=0
            else:
                f.write('\nRow:'+line[0]+' matched')
                matchcount=matchcount+1
        else:
            f.write('\nRow: '+line[0]+' Not available in Target')
            mismatchcount=mismatchcount+1
    f.write('\nRecords matched: '+str(matchcount)+' Records Mismatched: '+str(mismatchcount))
    print('\nRecords matched: ',matchcount,' Records Mismatched: ',mismatchcount,'\nResult is stored in '+result_path+'result.txt')
    f.close()
    sfile.close()
    tfile.close()

def comparefile_compositekey():
    sfile=codecs.open(result_path+'KBONDBA.UGCI_FINAN_TXN_ALLOC_11.7.csv','r')
    tfile=codecs.open(result_path+'KBONDBA.UGCI_FINAN_TXN_ALLOC_11.5.csv','r')
    database_set = dict()
    colnames=dict()
    a=0
    i=0
    j=0
    k=0
    row=list()
    rlist=list()
    mismatch=0
    mismatchcount=0
    matchcount=0
    f=open(result_path+'KBONDBA.UGCI_FINAN_TXN_ALLOC_Comparsion.txt','w')
    src_csv=csv.reader(sfile)
    tgt_csv1=csv.reader((line5.replace('\0','') for line5 in tfile))
    for r in src_csv:
    #for r in sfile: 
        for l in r:
            colnames[i]=l
            i=i+1
        sfile.seek(0)
        break
    for rline in tfile:
        j=j+len(rline)+1
        rline=rline.strip('\n')
        rows=rline.split(',',)
        database_set[rows[0]+rows[1]] =k
        k=j

    #for line in src_csv: #csv.reader((line4.replace('\0','') for line4 in sfile)):
    for line in csv.reader((line4.replace('\0','') for line4 in sfile)):   
        if line[0]+line[1] in database_set:
            j= database_set[line[0]+line[1]]
            tfile.seek(j)
            row=tgt_csv1.__next__()
            #row=tfile.__next__()
            #print()
            a=(len(row)-1)
            while(a>-1):
                #print(a)
                #print(line[a])
                #print(row[a])
                if (line[a]==row[a]):
                    a=a-1
                else:
                    f.write('\nMismatch in row:'+line[0]+line[1]+' column number:'+colnames[a]+' '+line[a]+' '+row[a])
                    mismatch=mismatch+1
                    a=a-1
            if mismatch>0:
                f.write('\nRow:'+line[0]+line[1]+' mismatched')
                mismatchcount=mismatchcount+1
                mismatch=0
            else:
                #f.write('\nRow:'+line[0]+line[1]+' matched')
                matchcount=matchcount+1
        else:
            f.write('\nRow: '+line[0]+line[1]+' Not available in Target')
            mismatchcount=mismatchcount+1
    f.write('\nRecords matched: '+str(matchcount)+' Records Mismatched: '+str(mismatchcount))
    print( 'Filename :  KBONDBA.UGCI_FINAN_TXN_ALLOC')
    print('\nRecords matched: ',matchcount,' Records Mismatched: ',mismatchcount,'\nResult is stored in '+result_path+'KBONDBA.UGCI_FINAN_TXN_ALLOC_Comparsion.txt')
    f.close()
    sfile.close()
    tfile.close()
def comparefile_nounique_key():
    sourcefile=codecs.open(result_path+'TBROKER_FEED_HIST_11.7.csv','r')
    targetfile=codecs.open(result_path+'TBROKER_FEED_HIST_8.7.csv','r')
    #sf=csv.reader(sourcefile)
    #tf=csv.reader(targetfile)
    matchcount=0
    count=1
    mismatchcount=0
    totalmatch=0
    sdict=dict()
    tdict=dict()
    for line in csv.reader((line4.replace('\0','') for line4 in sourcefile)):
        if str(line) in sdict:
            count=sdict[str(line)]
            count=count+1
            sdict[str(line)]=count
            count=1
        else:
            sdict[str(line)]=count
        count=1
    for line1 in csv.reader((line4.replace('\0','') for line4 in targetfile)):
        if str(line1) in tdict:
            count=tdict[str(line1)]
            count=count+1
            tdict[str(line1)]=count
            count=1
        else:
            tdict[str(line1)]=count
    result_file=open(result_path+'TBROKER_FEED_HIST_11.7_8.7_Comparison.txt','w')
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
            result_file.write('\nMismatched record:'+st)
    print('matched row count:',matchcount,'Mismatched row count:',mismatchcount,'\nResult is stored in '+result_path+'TBROKER_FEED_HIST_11.7_8.7_Comparison.txt')
    print( 'Filename : TBROKER_FEED_HIST_11.7_8.7_COMPARISON')
    result_file.write('matched row count:'+str(matchcount)+'Mismatched row count:'+str(mismatchcount))

#Below function calls the comparefile function to compare the results of the oracle and Dbe queries that have
#primaty key and writes the result to a text file
#comparefile()
#Below function calls the comparefile function to compare the results of the oracle and Dbe queries that have
#composte key and writes the result to a text file
#comparefile_compositekey()
#Below function calls the comparefile function to compare the results of the oracle and Dbe queries that
# does not have any unique key and writes the result to a text file
comparefile_nounique_key()
