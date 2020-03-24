from openpyxl import Workbook
from openpyxl.styles import Alignment
import pandas as pd
import xlrd
import csv
import openpyxl
import codecs
import sys
import os
import re
import webbrowser
import time
import numpy as np
para=input('\nEnter Parameter File Name with path:\n')
book = openpyxl.load_workbook(para)
sheet = book.active
inputfile=str(sheet['D4'].value)
cvr_file=str(sheet['D5'].value)
clr_file=str(sheet['D6'].value)
com_file=str(sheet['D7'].value)
Input_Path=str(sheet['D8'].value)
Output_Path=str(sheet['D9'].value)


OGIS_Input_File=open(r''+inputfile+'',"r")
split_file=open(r''+Output_Path+'\Full_Split_File.csv',"a+")
split_file.write('Policy number'',''Claim Number'',''Transaction Type'',''Ins.-R/I Type'',''Account Line'',''Original Currency Amount'',''Major/Minor Line''\n')
for split_line in OGIS_Input_File :
	slices = [(30,40),(46,56),(23,25),(161,163),(25,27),(230,247),(10,14)]
	split_out_line=[split_line[slice(*slc)] for slc in slices]
	split_file.write(",".join(split_out_line))
	split_file.write('\n')
split_file.close()
os.popen('copy '+Input_Path+'\main_F2F.html '+Output_Path+'\Consolidated_output_F2F.html')

def comparefile () :
	os.popen('copy '+Input_Path+'\module_F2F.html '+Output_Path+'\Part_output_F2F_'+File_Type+'.html')
	ogis_file=open(Target_path,'r')
	cledger_file=open(source_path,'r')
	result_file=open(result_file1,'a+')
	match_file=open(match_file1,'a+')
	misfile=open(misfile1,'a+')
	a=0
	mismatch=0
	mis=0
	line = cledger_file.readlines()
	len_cledger=len(line)
	line1 = ogis_file.readlines()
	len_ogis=len(line1)
	i=0
	h=1
	s=0
	
	while len_cledger > 0 :
		match=0
		mis_cnt=0
		if i == 0 :
			result_file.write(''+Pol_Claim+','+typ+',OGIS_Value''\n')
			match_file.write(''+Pol_Claim+','+typ+',OGIS_Value''\n')
			misfile.write(''+Pol_Claim+'')
			#html_file.write('<tr><td>'+Pol_Claim+'</td><td>'+typ+'</td><td>OGIS_Value</td></tr>')
			
		else :
			x=line[i].split(',')
			w=x[0]
			j=0
			len_ogis=len(line1)
			while len_ogis > 0 :
				if j == 0 :
					c=line1[j].split(',')
					x1=c[0].strip()
				else :
					c=line1[j].split(',')
					x1=c[0].strip()

					if w == x1 and match == 0 :
						mis_cnt += 1
						if File_Type == "Claim_Subrogation" or File_Type == "Claim_CP_RI" or File_Type == "Claim_CR_RI" :
							x[1] = x[1].lstrip('-')

						f=float(x[1])
						g=float(c[1])
						a=round(f, 2)
						b=round(g,2)
						if a == b :
							match +=1
							match_file.write(''+x[0].strip()+','+x[1].strip()+','+c[1].strip()+'\n')
						else :
							result_file.write(''+x[0].strip()+','+x[1].strip()+','+c[1].strip()+'\n')
							#html_file.write('<tr><td>'+x[0].strip()+'</td><td>'+x[1].strip()+'</td><td>'+c[1].strip()+'</td></tr>')
							mismatch +=1
				j +=1
				len_ogis -=1
				
			if mis_cnt == 0 and i > 0 :
				mis +=1
				misfile.write('\n'+x[0].strip()+'')
		i +=1		
		len_cledger -=1
	match_file.close()
	result_file.close()
	misfile.close()


def html_file() :
	ogis_file=open(Target_path,'r')
	cledger_file=open(source_path,'r')
	line = cledger_file.readlines()
	len_cledger=len(line)
	line1 = ogis_file.readlines()
	len_ogis=len(line1)
	html_file=open(r''+Output_Path+'\Part_output_F2F_'+File_Type+'.html','a+')
	cons_file=open(r''+Output_Path+'\Consolidated_output_F2F.html','a+')
	match_html=open(r''+Output_Path+'\Match_'+File_Type+'.csv','r')
	mismatch_html=open(r''+Output_Path+'\Mismatch_'+File_Type+'.csv','r')
	miss_html=open(r''+Output_Path+'\Missing_Record_'+File_Type+'.csv','r')
	line_match_html=match_html.readlines()
	len_match_html=len(line_match_html)
	line_mismatch_html=mismatch_html.readlines()
	len_mismatch_html=len(line_mismatch_html)
	mismatch=len_mismatch_html
	line_miss_html=miss_html.readlines()
	len_miss_html=len(line_miss_html)
	mis_cnt=len_miss_html
	i=0
	j=0
	mismatch_cnt=len_mismatch_html
	time.sleep(3)
	z=len_mismatch_html
	while len_mismatch_html > 1 and z > 0:
		if j == 0 :
			html_file.write('<b>&nbsp;&nbsp;Below are the records Mismatched in OGIS File</b><br/><br/><table>')
			j +=1
		x=line_mismatch_html[i].split(',')
		html_file.write('<tr><td>'+x[0].strip()+'</td><td>'+x[1].strip()+'</td><td>'+x[2].strip()+'</td></tr>')
		i += 1
		z -= 1
	i=0
	html_file.write('</table><br/><br/>')
	j=0
	o=len_miss_html
	while len_miss_html > 1 and  o > 0:
		if j == 0 :
			html_file.write('<b>&nbsp;&nbsp;Below are the records not available in OGIS File</b><br/><table>')
			j +=1
		m=line_miss_html[i].split(',')
		html_file.write('<tr><td>'+m[0].strip()+'</td></tr>')
		i += 1
		o -= 1
	i=0
	html_file.write('</table><br/><br/>')
	j=0
	l=0
	while l < 3 and len_match_html > 1 :
		if j == 0 :
			html_file.write('<b>&nbsp;&nbsp;Sample Matched records</b><br/><br/><table>')
			j +=1
		k=line_match_html[i].split(',')
		html_file.write('<tr><td>'+k[0].strip()+'</td><td>'+k[1].strip()+'</td><td>'+k[2].strip()+'</td></tr>')
		i += 1
		l += 1		
	html_file.write('</table>')
	html_file.close()
	mismatch -= 1
	mis_cnt -= 1
	len_cledger -= 1
	len_ogis -= 1
	if mismatch > 0 :
		data_stat='FAILED'
		data_stat_val='<a href='+Output_Path+'\Output_F2F_'+File_Type+'.html target="_blank"><font color="RED">FAILED</font></a>'
	else :
		data_stat='PASSED'
		data_stat_val='<a href='+Output_Path+'\Output_F2F_'+File_Type+'.html target="_blank"><font color="green">PASSED</font></a>'
	if mis_cnt > 0 :
		count_stat='FAILED'
		count_stat_val='<a href='+Output_Path+'\Output_F2F_'+File_Type+'.html target="_blank"><font color="RED">FAILED</font></a>'
		
	else :
		count_stat='PASSED'
		count_stat_val='<a href='+Output_Path+'\Output_F2F_'+File_Type+'.html" target="_blank"><font color="green">PASSED</font></a>'
	checkWords = ("File_Type","Ledger_Value","OGIS Value","mismatch","Missing","data_status","count_status")
	repWords = (str(File_Type),str(len_cledger),str(len_ogis),str(mismatch),str(mis_cnt),str(data_stat),str(count_stat))
	f1=open(r''+Output_Path+'\Part_output_F2F_'+File_Type+'.html')
	f2=open(r''+Output_Path+'\Output_F2F_'+File_Type+'.html',"w")
	for line in f1:
		for check, rep in zip(checkWords, repWords):
			line = line.replace(check, rep)
		f2.write(line)
	f1.close()
	f2.close()
	cons_file.write('<tr><td>'+File_Type+'</td><td>'+str(len_cledger)+'</td><td>'+str(len_ogis)+'</td><td>'+str(mismatch)+'</td><td>'+str(mis_cnt)+'</td><td>'+data_stat_val+'</td><td>'+count_stat_val+'</td></tr>')
	print ('\n Validation completed for '+File_Type+'')
	os.remove(r''+Output_Path+'\Part_output_F2F_'+File_Type+'.html')

split_file=open(r''+Output_Path+'\Full_Split_File.csv',"r")

#For Policy NB GROSS and RI Premimum 

dataframe=pd.read_csv(split_file,sep=',')
df1=dataframe[["Policy number","Claim Number","Transaction Type","Ins.-R/I Type","Account Line","Original Currency Amount"]]
df_PNB_Gross=df1[df1["Ins.-R/I Type"].isin(["00","15"])&df1["Claim Number"].isin(["0"])&df1["Transaction Type"].isin(["1"])]
df_gross=df_PNB_Gross[["Policy number","Original Currency Amount"]]
df_gross_file=df_gross.groupby(["Policy number"]).sum()
df_csvs=df_gross_file.to_csv(""+Output_Path+"\OGIS_Data_RI_TYPE_00_15.csv")

dataframe1=pd.read_excel(cvr_file)
df2=dataframe1[["Policy No.","Reinsurance Type","Entry Type","Premium"]] 
df_cvr_gross=df2[df2["Entry Type"].isin(["Policy"])&df2["Reinsurance Type"].isin([" "])]
df_cvr_value=df_cvr_gross[["Policy No.","Premium"]]
df_cvr_file=df_cvr_value.groupby(["Policy No."]).sum()
df_csvs=df_cvr_file.to_csv(""+Output_Path+"\cover_ledger_entries_gross.csv")

source_path=r''+Output_Path+'\cover_ledger_entries_gross.csv'
Target_path=r''+Output_Path+'\OGIS_Data_RI_TYPE_00_15.csv'
File_Type='Policy_NB_Gross'
result_file1=r''+Output_Path+'\Mismatch_'+File_Type+'.csv'
match_file1=r''+Output_Path+'\Match_'+File_Type+'.csv'
misfile1=r''+Output_Path+'\Missing_Record_'+File_Type+'.csv'
typ='Cover_Ledger_value'
Pol_Claim='PolicyNumber'

comparefile ()
html_file()

df_PNB_RI=df1[df1["Ins.-R/I Type"].isin(["01","02"])&df1["Claim Number"].isin(["0"])&df1["Transaction Type"].isin(["1"])]
df_RI=df_PNB_RI[["Policy number","Original Currency Amount"]]
df_RI_file=df_RI.groupby(["Policy number"]).sum()
df_csvs=df_RI_file.to_csv(""+Output_Path+"\OGIS_Data_RI_TYPE_01_02.csv")

dataframe_NB_RI=pd.read_excel(cvr_file)
df3=dataframe_NB_RI[["Policy No.","Reinsurance Type","Entry Type","Premium"]] 
df_cvr_RI=df3[df3["Entry Type"].isin(["Policy"])&df3["Reinsurance Type"].isin(["Treaty"])]
df_cvr_RI=df_cvr_RI[["Policy No.","Premium"]]
df_cvr_RI_file=df_cvr_RI.groupby(["Policy No."]).sum()
df_csvs=df_cvr_RI_file.to_csv(""+Output_Path+"\cover_ledger_entries_RI.csv")

source_path=r''+Output_Path+'\cover_ledger_entries_RI.csv'
Target_path=r''+Output_Path+'\OGIS_Data_RI_TYPE_01_02.csv'
File_Type='Policy_NB_RI'
result_file1=r''+Output_Path+'\Mismatch_'+File_Type+'.csv'
match_file1=r''+Output_Path+'\Match_'+File_Type+'.csv'
misfile1=r''+Output_Path+'\Missing_Record_'+File_Type+'.csv'
typ='Cover_Ledger_value'
Pol_Claim='PolicyNumber'
comparefile ()
html_file()
df_PNB_RI_82=df1[df1["Ins.-R/I Type"].isin(["82","83","87"])&df1["Claim Number"].isin(["0"])&df1["Transaction Type"].isin(["1"])]
df_RI_82=df_PNB_RI_82[["Policy number","Ins.-R/I Type","Original Currency Amount"]]
df_RI_file_82=df_RI_82.groupby(["Policy number","Ins.-R/I Type"]).sum()
df_csvs=df_RI_file_82.to_csv(""+Output_Path+"\OGIS_Data_Policy_NB_RI_TYPE_82_83_87.csv")

#For Policy RN Gross and RI Premimum 

df1=dataframe[["Policy number","Claim Number","Transaction Type","Ins.-R/I Type","Account Line","Original Currency Amount"]]
df_PNB_Gross=df1[df1["Ins.-R/I Type"].isin(["00","15"])&df1["Claim Number"].isin(["0"])&df1["Transaction Type"].isin(["4"])]
df_gross=df_PNB_Gross[["Policy number","Original Currency Amount"]]
df_gross_file=df_gross.groupby(["Policy number"]).sum()
df_csvs=df_gross_file.to_csv(""+Output_Path+"\OGIS_Data_Policy_RN_RI_TYPE_00_15.csv")

dataframe1=pd.read_excel(cvr_file)
df2=dataframe1[["Policy No.","Reinsurance Type","Entry Type","Premium"]] 
df_cvr_gross=df2[df2["Entry Type"].isin(["Renewal"])&df2["Reinsurance Type"].isin([" "])]
df_cvr_value=df_cvr_gross[["Policy No.","Premium"]]
df_cvr_file=df_cvr_value.groupby(["Policy No."]).sum()
df_csvs=df_cvr_file.to_csv(""+Output_Path+"\cover_ledger_entries_Policy_RN_gross.csv")

source_path=r''+Output_Path+'\cover_ledger_entries_Policy_RN_gross.csv'
Target_path=r''+Output_Path+'\OGIS_Data_Policy_RN_RI_TYPE_00_15.csv'
File_Type='Policy_RN_Gross'
result_file1=r''+Output_Path+'\Mismatch_'+File_Type+'.csv'
match_file1=r''+Output_Path+'\Match_'+File_Type+'.csv'
misfile1=r''+Output_Path+'\Missing_Record_'+File_Type+'.csv'
typ='Cover_Ledger_value'
Pol_Claim='PolicyNumber'
comparefile ()
html_file()
df_PRN_RI=df1[df1["Ins.-R/I Type"].isin(["01","02"])&df1["Claim Number"].isin(["0"])&df1["Transaction Type"].isin(["4"])]
df_RI=df_PRN_RI[["Policy number","Original Currency Amount"]]
df_RI_file=df_RI.groupby(["Policy number"]).sum()
df_csvs=df_RI_file.to_csv(""+Output_Path+"\OGIS_Data_Policy_RN_RI_TYPE_01_02.csv")

dataframe_RN_RI=pd.read_excel(cvr_file)
df3=dataframe_RN_RI[["Policy No.","Reinsurance Type","Entry Type","Premium"]] 
df_cvr_RI=df3[df3["Entry Type"].isin(["Renewal"])&df3["Reinsurance Type"].isin(["Treaty"])]
df_cvr_RI=df_cvr_RI[["Policy No.","Premium"]]
df_cvr_RI_file=df_cvr_RI.groupby(["Policy No."]).sum()
df_csvs=df_cvr_RI_file.to_csv(""+Output_Path+"\cover_ledger_entries_Policy_RN_RI.csv")

source_path=r''+Output_Path+'\cover_ledger_entries_Policy_RN_RI.csv'
Target_path=r''+Output_Path+'\OGIS_Data_Policy_RN_RI_TYPE_01_02.csv'
File_Type='Policy_RN_RI'
result_file1=r''+Output_Path+'\Mismatch_'+File_Type+'.csv'
match_file1=r''+Output_Path+'\Match_'+File_Type+'.csv'
misfile1=r''+Output_Path+'\Missing_Record_'+File_Type+'.csv'
typ='Cover_Ledger_value'
Pol_Claim='PolicyNumber'
comparefile ()
html_file()
df_PRN_RI_82=df1[df1["Ins.-R/I Type"].isin(["82","83","87"])&df1["Claim Number"].isin(["0"])&df1["Transaction Type"].isin(["4"])]
df_RI_82=df_PRN_RI_82[["Policy number","Ins.-R/I Type","Original Currency Amount"]]
df_RI_file_82=df_RI_82.groupby(["Policy number","Ins.-R/I Type"]).sum()
df_csvs=df_RI_file_82.to_csv(""+Output_Path+"\OGIS_Data_Policy_RN_RI_TYPE_82_83_87.csv")

#For Policy EN Gross and RI Premimum 

df1=dataframe[["Policy number","Claim Number","Transaction Type","Ins.-R/I Type","Account Line","Original Currency Amount"]]
df_PNB_Gross=df1[df1["Ins.-R/I Type"].isin(["00","15"])&df1["Claim Number"].isin(["0"])&df1["Transaction Type"].isin(["5"])]
df_gross=df_PNB_Gross[["Policy number","Original Currency Amount"]]
df_gross_file=df_gross.groupby(["Policy number"]).sum()
df_csvs=df_gross_file.to_csv(""+Output_Path+"\OGIS_Data_Policy_EN_RI_TYPE_00_15.csv")

dataframe1=pd.read_excel(cvr_file)
df2=dataframe1[["Policy No.","Reinsurance Type","Entry Type","Premium"]] 
df_cvr_gross=df2[df2["Entry Type"].isin(["Endorsement"])&df2["Reinsurance Type"].isin([" "])]
df_cvr_value=df_cvr_gross[["Policy No.","Premium"]]
df_cvr_file=df_cvr_value.groupby(["Policy No."]).sum()
df_csvs=df_cvr_file.to_csv(""+Output_Path+"\cover_ledger_entries_Policy_EN_gross.csv")

source_path=r''+Output_Path+'\cover_ledger_entries_Policy_EN_gross.csv'
Target_path=r''+Output_Path+'\OGIS_Data_Policy_EN_RI_TYPE_00_15.csv'
File_Type='Policy_EN_Gross'
result_file1=r''+Output_Path+'\Mismatch_'+File_Type+'.csv'
match_file1=r''+Output_Path+'\Match_'+File_Type+'.csv'
misfile1=r''+Output_Path+'\Missing_Record_'+File_Type+'.csv'
typ='Cover_Ledger_value'
Pol_Claim='PolicyNumber'
comparefile ()
html_file()
df_PEN_RI=df1[df1["Ins.-R/I Type"].isin(["01","02"])&df1["Claim Number"].isin(["0"])&df1["Transaction Type"].isin(["5"])]
df_RI=df_PEN_RI[["Policy number","Original Currency Amount"]]
df_RI_file=df_RI.groupby(["Policy number"]).sum()
df_csvs=df_RI_file.to_csv(""+Output_Path+"\OGIS_Data_Policy_EN_RI_TYPE_01_02.csv")

dataframe_EN_RI=pd.read_excel(cvr_file)
df3=dataframe_EN_RI[["Policy No.","Reinsurance Type","Entry Type","Premium"]] 
df_cvr_RI=df3[df3["Entry Type"].isin(["Endorsement"])&df3["Reinsurance Type"].isin(["Treaty"])]
df_cvr_RI=df_cvr_RI[["Policy No.","Premium"]]
df_cvr_RI_file=df_cvr_RI.groupby(["Policy No."]).sum()
df_csvs=df_cvr_RI_file.to_csv(""+Output_Path+"\cover_ledger_entries_Policy_EN_RI.csv")

source_path=r''+Output_Path+'\cover_ledger_entries_Policy_EN_RI.csv'
Target_path=r''+Output_Path+'\OGIS_Data_Policy_EN_RI_TYPE_01_02.csv'
File_Type='Policy_EN_RI'
result_file1=r''+Output_Path+'\Mismatch_'+File_Type+'.csv'
match_file1=r''+Output_Path+'\Match_'+File_Type+'.csv'
misfile1=r''+Output_Path+'\Missing_Record_'+File_Type+'.csv'
typ='Cover_Ledger_value'
Pol_Claim='PolicyNumber'
comparefile ()
html_file()
df_PEN_RI_82=df1[df1["Ins.-R/I Type"].isin(["82","83","87"])&df1["Claim Number"].isin(["0"])&df1["Transaction Type"].isin(["5"])]
df_RI_82=df_PEN_RI_82[["Policy number","Ins.-R/I Type","Original Currency Amount"]]
df_RI_file_82=df_RI_82.groupby(["Policy number","Ins.-R/I Type"]).sum()
df_csvs=df_RI_file_82.to_csv(""+Output_Path+"\OGIS_Data_Policy_EN_RI_TYPE_82_83_87.csv")

#For Claim Reserve Gross and RI Premimum 

df1=dataframe[["Policy number","Claim Number","Transaction Type","Ins.-R/I Type","Account Line","Original Currency Amount"]]
df_PCR_Gross=df1[df1["Ins.-R/I Type"].isin(["00","15"])&df1["Account Line"].isin(["50"])&df1["Transaction Type"].isin(["19"])]
df_gross=df_PCR_Gross[["Claim Number","Original Currency Amount"]]
df_gross_file=df_gross.groupby(["Claim Number"]).sum()
df_csvs=df_gross_file.to_csv(""+Output_Path+"\OGIS_Data_Claim_CR_RI_TYPE_00_15.csv")

dataframe1=pd.read_excel(clr_file)
df2=dataframe1[["Claim No.","Entry Type","Estim. Total Cost (LCY)"]] 
df_cvr_gross=df2[df2["Entry Type"].isin(["Indemnity"])]
df_cvr_value=df_cvr_gross[["Claim No.","Estim. Total Cost (LCY)"]]
df_cvr_file=df_cvr_value.groupby(["Claim No."]).sum()
df_csvs=df_cvr_file.to_csv(""+Output_Path+"\claim_ledger_entries_claim_CR_gross.csv")

source_path=r''+Output_Path+'\claim_ledger_entries_claim_CR_gross.csv'
Target_path=r''+Output_Path+'\OGIS_Data_Claim_CR_RI_TYPE_00_15.csv'
File_Type='Claim_CR_Gross'
result_file1=r''+Output_Path+'\Mismatch_'+File_Type+'.csv'
match_file1=r''+Output_Path+'\Match_'+File_Type+'.csv'
misfile1=r''+Output_Path+'\Missing_Record_'+File_Type+'.csv'
typ='Claim_Ledger_value'
Pol_Claim='ClaimNumber'
comparefile ()
html_file()
df_CCR_RI=df1[df1["Ins.-R/I Type"].isin(["01","02"])&df1["Account Line"].isin(["50"])&df1["Transaction Type"].isin(["19"])]
df_RI=df_CCR_RI[["Claim Number","Original Currency Amount"]]
df_RI_file=df_RI.groupby(["Claim Number"]).sum()
df_csvs=df_RI_file.to_csv(""+Output_Path+"\OGIS_Data_Claim_CR_RI_TYPE_01_02.csv")

df3=dataframe1[["Claim No.","Entry Type","Estim. Total Cost (LCY)"]] 
df_cvr_RI=df3[df3["Entry Type"].isin(["Reins./Coins. Recovery"])]
df_cvr_RI=df_cvr_RI[["Claim No.","Estim. Total Cost (LCY)"]]
df_cvr_RI_file=df_cvr_RI.groupby(["Claim No."]).sum()
df_csvs=df_cvr_RI_file.to_csv(""+Output_Path+"\claim_ledger_entries_claim_CR_RI.csv")

source_path=r''+Output_Path+'\claim_ledger_entries_claim_CR_RI.csv'
Target_path=r''+Output_Path+'\OGIS_Data_Claim_CR_RI_TYPE_01_02.csv'
File_Type='Claim_CR_RI'
result_file1=r''+Output_Path+'\Mismatch_'+File_Type+'.csv'
match_file1=r''+Output_Path+'\Match_'+File_Type+'.csv'
misfile1=r''+Output_Path+'\Missing_Record_'+File_Type+'.csv'
typ='Claim_Ledger_value'
Pol_Claim='ClaimNumber'
comparefile ()
html_file()
df_CCR_RI_82=df1[df1["Ins.-R/I Type"].isin(["82","83","87"])&df1["Claim Number"].isin(["0"])&df1["Transaction Type"].isin(["19"])]
df_RI_82=df_CCR_RI_82[["Claim Number","Ins.-R/I Type","Original Currency Amount"]]
df_RI_file_82=df_RI_82.groupby(["Claim Number","Ins.-R/I Type"]).sum()
df_csvs=df_RI_file_82.to_csv(""+Output_Path+"\OGIS_Data_Claim_CR_RI_TYPE_82_83_87.csv")

#For Claim Payment Gross and RI Premimum 

df1=dataframe[["Policy number","Claim Number","Transaction Type","Ins.-R/I Type","Account Line","Original Currency Amount"]]
df_PCP_Gross=df1[df1["Ins.-R/I Type"].isin(["00","15"])&df1["Account Line"].isin(["50"])&df1["Transaction Type"].isin(["21","22"])]
df_gross=df_PCP_Gross[["Claim Number","Original Currency Amount"]]
df_gross_file=df_gross.groupby(["Claim Number"]).sum()
df_csvs=df_gross_file.to_csv(""+Output_Path+"\OGIS_Data_Claim_CP_RI_TYPE_00_15.csv")

dataframe1=pd.read_excel(clr_file)
df2=dataframe1[["Claim No.","Entry Type","Total Cost (LCY)"]] 
df_cvr_gross=df2[df2["Entry Type"].isin(["Indemnity"])]
df_cvr_value=df_cvr_gross[["Claim No.","Total Cost (LCY)"]]
df_cvr_file=df_cvr_value.groupby(["Claim No."]).sum()
df_csvs=df_cvr_file.to_csv(""+Output_Path+"\claim_ledger_entries_claim_CP_gross.csv")

source_path=r''+Output_Path+'\claim_ledger_entries_claim_CP_gross.csv'
Target_path=r''+Output_Path+'\OGIS_Data_Claim_CP_RI_TYPE_00_15.csv'
File_Type='Claim_CP_Gross'
result_file1=r''+Output_Path+'\Mismatch_'+File_Type+'.csv'
match_file1=r''+Output_Path+'\Match_'+File_Type+'.csv'
misfile1=r''+Output_Path+'\Missing_Record_'+File_Type+'.csv'
typ='Claim_Ledger_value'
Pol_Claim='ClaimNumber'
comparefile ()
html_file()
df_CCP_RI=df1[df1["Ins.-R/I Type"].isin(["01","02"])&df1["Account Line"].isin(["50"])&df1["Transaction Type"].isin(["21","22"])]
df_RI=df_CCP_RI[["Claim Number","Original Currency Amount"]]
df_RI_file=df_RI.groupby(["Claim Number"]).sum()
df_csvs=df_RI_file.to_csv(""+Output_Path+"\OGIS_Data_Claim_CP_RI_TYPE_01_02.csv")

df3=dataframe1[["Claim No.","Entry Type","Total Cost (LCY)"]] 
df_cvr_RI=df3[df3["Entry Type"].isin(["Reins./Coins. Recovery"])]
df_cvr_RI=df_cvr_RI[["Claim No.","Total Cost (LCY)"]]
df_cvr_RI_file=df_cvr_RI.groupby(["Claim No."]).sum()
df_csvs=df_cvr_RI_file.to_csv(""+Output_Path+"\claim_ledger_entries_claim_CP_RI.csv")

source_path=r''+Output_Path+'\claim_ledger_entries_claim_CP_RI.csv'
Target_path=r''+Output_Path+'\OGIS_Data_Claim_CP_RI_TYPE_01_02.csv'
File_Type='Claim_CP_RI'
result_file1=r''+Output_Path+'\Mismatch_'+File_Type+'.csv'
match_file1=r''+Output_Path+'\Match_'+File_Type+'.csv'
misfile1=r''+Output_Path+'\Missing_Record_'+File_Type+'.csv'
typ='Claim_Ledger_value'
Pol_Claim='ClaimNumber'
comparefile ()
html_file()
df_CCP_RI_82=df1[df1["Ins.-R/I Type"].isin(["82","83","87"])&df1["Claim Number"].isin(["0"])&df1["Transaction Type"].isin(["21","22"])]
df_RI_82=df_CCP_RI_82[["Claim Number","Ins.-R/I Type","Original Currency Amount"]]
df_RI_file_82=df_RI_82.groupby(["Claim Number","Ins.-R/I Type"]).sum()
df_csvs=df_RI_file_82.to_csv(""+Output_Path+"\OGIS_Data_Claim_CP_RI_TYPE_82_83_87.csv")

#For Subrogation Gross and RI Premimum 

df1=dataframe[["Policy number","Claim Number","Transaction Type","Ins.-R/I Type","Account Line","Original Currency Amount"]]
df_PSU_Gross=df1[df1["Ins.-R/I Type"].isin(["00","15"])&df1["Account Line"].isin(["50"])&df1["Transaction Type"].isin(["26"])]
df_gross=df_PSU_Gross[["Claim Number","Original Currency Amount"]]
df_gross_file=df_gross.groupby(["Claim Number"]).sum()
df_csvs=df_gross_file.to_csv(""+Output_Path+"\OGIS_Data_Claim_SU_RI_TYPE_00_15.csv")

dataframe1=pd.read_excel(clr_file)
df2=dataframe1[["Claim No.","Entry Type","Total Cost (LCY)"]] 
df_cvr_gross=df2[df2["Entry Type"].isin(["Third-Party Recovery"])]
df_cvr_value=df_cvr_gross[["Claim No.","Total Cost (LCY)"]]
df_cvr_file=df_cvr_value.groupby(["Claim No."]).sum()
df_csvs=df_cvr_file.to_csv(""+Output_Path+"\claim_ledger_entries_claim_SU_gross.csv")

source_path=r''+Output_Path+'\claim_ledger_entries_claim_SU_gross.csv'
Target_path=r''+Output_Path+'\OGIS_Data_Claim_SU_RI_TYPE_00_15.csv'
File_Type='Claim_Subrogation'
result_file1=r''+Output_Path+'\Mismatch_'+File_Type+'.csv'
match_file1=r''+Output_Path+'\Match_'+File_Type+'.csv'
misfile1=r''+Output_Path+'\Missing_Record_'+File_Type+'.csv'
typ='Claim_Ledger_value'
Pol_Claim='ClaimNumber'
comparefile ()
html_file()

#For commison
dc=dataframe[["Major/Minor Line","Claim Number","Transaction Type","Original Currency Amount"]]
df_com_Gross=dc[dc["Claim Number"].isin(["0"])&dc["Transaction Type"].isin(["21"])]
dc_gross=df_com_Gross[["Major/Minor Line","Original Currency Amount"]]
dc_gross_file=dc_gross.groupby(["Major/Minor Line"]).sum()
df_csvs=dc_gross_file.to_csv(""+Output_Path+"\Commison_Splitted_file.csv")

dataframe_com=pd.read_excel(com_file)
df2=dataframe_com[["Minor Code","Entry Type","Amount"]] 
df_cvr_gross=df2[df2["Entry Type"].isin(["Reins. Inbound Commission"])]
df_cvr_value=df_cvr_gross[["Minor Code","Amount"]]
df_cvr_file=df_cvr_value.groupby(["Minor Code"]).sum()
df_csvs=df_cvr_file.to_csv(""+Output_Path+"\commison_ledger_entries.csv")

source_path=r''+Output_Path+'\commison_ledger_entries.csv'
Target_path=r''+Output_Path+'\Commison_Splitted_file.csv'
File_Type='Commison'
result_file1=r''+Output_Path+'\Mismatch_'+File_Type+'.csv'
match_file1=r''+Output_Path+'\Match_'+File_Type+'.csv'
misfile1=r''+Output_Path+'\Missing_Record_'+File_Type+'.csv'
typ='Commison_Ledger_value'
Pol_Claim='Major/Minor Code'
comparefile ()
html_file()

print ("\n\nValidation completed successfully opening summary output file in browser")
webbrowser.open(''+Output_Path+'\Consolidated_output_F2F.html');