#cd C:\Users\mgratzer\Documents\General\pubs\FY21\Update\figs\working\age

#import packages
import os,sys
import time
import numpy as np
from scipy import stats
import pandas as pd 
import geopandas as gp
# import seaborn as sns #nicer boxplots
import matplotlib
import matplotlib.pyplot as plt
from numpy import array
# import sciencebasepy
# import zipfile
# # import scripts from gitrepo
# import ZipUtility as zu 
# import SB_Uploader as su
from shapely.geometry import Point
import statistics
import math
from math import log10, floor
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
#############################
# att=gp.read_file(os.path.join('../../../../../../../../../../github/MAPQW/Data/SB/QW/mscl_qwsites_att','mscl_qwsites_att.shp'))
# #att=att.replace(-9999,np.nan)
# attshp=att.shape
# mADcols=att.columns.unique().tolist()
# print('att:',attshp)
# print(mADcols)
# att_sites = att['SITEAG'].unique().tolist()
# print('number of unique sites in att:',len(att_sites))#88
# print('\t')
###########################################################################
#mergeADs=pd.read_csv('mad1174pguLtY.csv')
#mergeADs=pd.read_csv('mad1174nonan4pearsonpguLtY.csv')
#mergeADs=pd.read_csv('revisedmad_nonan_pearson.csv')
#mergeADs=pd.read_csv('morecompletenonantYLpb3.csv')
#mergeADs=pd.read_csv(os.path.join('../../../../../../../../../../github/map_gwage/MERASwd/Scripts/plots','mergeADsTable_c2_pguLtY21751455.csv'))
mergeADs=pd.read_csv(os.path.join('../../../../../../../../../../github/map_gwage/MERASwd/Scripts','mads4lpmstats3235.csv'))
#mergeADs=mergeADs.replace(-9999,np.nan)
mergeADsshp=mergeADs.shape
mADcols=mergeADs.columns.unique().tolist()
print('mergeADs:',mergeADsshp)
print(mADcols)
mergeADs_sites = mergeADs['siteag'].unique().tolist()
print('number of unique sites in mergeADs:',len(mergeADs_sites))#88
print('\t')
# mergeADs_att_s=list(set(mergeADs_sites)-set(att_sites))
# print('mergeADs_att_s:',mergeADs_att_s)
# att_t2g_s=list(set(att_sites)-set(t2g_sites))
# print('att_t2g_s:',att_t2g_s)
print('\t')
#sys.exit()

mergeADs.loc[:,'GWSys']='TRRC'
mergeADs.loc[mergeADs['Layer']=='MRVA','GWSys']='MRVA'
mergeADs.loc[mergeADs['Layer'].isin(['CLBR','CNZC','LCAQ','MCAQ','UCAQ']),'GWSys']='CLBR'
mergeADs.loc[mergeADs['Layer'].isin(['MWAQ','LWAQ','UWAQ']),'GWSys']='WLCX'

mergeADs=mergeADs.replace(-9999,np.nan)
mergeADs=mergeADs.replace(0,np.nan)

#mergeADs_mrva=mergeADs.loc[mergeADs['Layer']=='MRVA']
# read Table 1
#df1=gp.read_file(os.path.join('../../../../GISdata','Table1_Sites_Info.shp'))
#df1=gp.read_file(os.path.join('../../../../../../../shps','t1wreg3532043.shp'))
df1=pd.read_csv(os.path.join('../../../../../../../shps','joint1reg833.csv'))
print(df1.columns.tolist())
#df1=df1.drop_duplicates()
df1shp=df1.shape
print('df1: ', df1shp)
df1_sites = df1['siteag'].unique().tolist()
print('number of unique sites in df1:',len(df1_sites))#88
print('\t')
#keepcols=['siteag', 'geometry','Formation', 'Descrip', 'Geo_Age','hUnit']
#df1=df1.loc[:,keepcols]
# t2g['dttm'] = t2g['datecorr'] + ' ' + t2g['timecorr'].astype(str)
# t2g['dttm'] = pd.to_datetime(t2g['dttm'], format='%m/%d/%Y %H:%M')
# t2g_dttm = t2g['dttm'].unique().tolist()
# print('number of unique dttm in t2g:',len(t2g_dttm))
#print('\t')

mergeADs_df1_s=list(set(mergeADs_sites)-set(df1_sites))
print('mergeADs_df1_s:',mergeADs_df1_s)
# df1_t2g_s=list(set(df1_sites)-set(t2g_sites))
# print('df1_t2g_s:',df1_t2g_s)
print('\t')
#sys.exit()
mergeADs=mergeADs.merge(df1,how='left',on='siteag')
mergeADs_mrva=mergeADs.loc[mergeADs['GWSys']=='MRVA']
#mergeADs_mrva.to_csv('mergeADs_mrva_scatterplots1224.csv')
#sys.exit()
# medmrvlpma=statistics.median(mergeADs_mrva['varianceLPMages'])
# medmravr=statistics.median(mergeADs_mrva['avgVARres'])
# meanmrvlpma=np.mean(mergeADs_mrva['varianceLPMages'])
# meanmravr=np.mean(mergeADs_mrva['avgVARres'])
# medmrver=statistics.median(mergeADs_mrva['varreseff'])
# meanmrver=np.mean(mergeADs_mrva['varreseff'])
# medmrvvr=statistics.median(mergeADs_mrva['varVARres'])
# meanmrvvr=np.mean(mergeADs_mrva['varVARres'])
# medmrvpt=statistics.median(mergeADs_mrva['VARPTbs'])
# meanmrvpt=np.mean(mergeADs_mrva['VARPTbs'])
# medmrxbpt=statistics.median(mergeADs_mrva['xbPTbs'])
# meanmrxbpt=np.mean(mergeADs_mrva['xbPTbs'])
# medmrmawa=statistics.median(mergeADs_mrva['meanAgeWeightedAvg'])
# meanmrmawa=np.mean(mergeADs_mrva['meanAgeWeightedAvg'])

reggrp=mergeADs_mrva.groupby('region')
###########################################################################################
###########################################################################################
#acvr v cvlpm
###########################################################################################
fig, ax = plt.subplots()
for name,group in reggrp:
	ax.plot(group['acvr'], group['cvlpmad'], label=name, marker = 'o', linestyle='')
    # ax.set_ylim(group['mrva_ymin'],0)
# ax.plot(mergeADs['varlogreseff'], mergeADs['varianceLPMages'], marker = 'o', linestyle='')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Average coefficient of variation of resistivity')
#ax.set_xlabel('Variance of effective resistivity, in Ohms squared - meters squared')
ax.set_ylabel('Coefficient of variation of tracer age distribution')
ax.legend()
plt.savefig('acvr_cvLPM_4115_byreg.png')
plt.close()
print('Thank You!')
#sys.exit()
print('avlrsn_vlpmsn1154 plotted with log axes. Thank You!')
###########################################################################################
###########################################################################################
#MER v cvlpm
###########################################################################################
# fig, ax = plt.subplots()
# for name,group in reggrp:
# 	if name=='Delta':
# 		ax.plot(group['varreseff'], group['varianceLPMages'], label=name, marker = 'o', linestyle='')
# ax.set_xscale('log')
# ax.set_yscale('log')
# ax.set_xlabel('Variance of effective resistivity, (Ohm-meters) squared')
# #ax.set_xlabel('Variance of effective resistivity, in Ohms squared - meters squared')
# ax.set_ylabel('Variance of tracer age distribution, years squared')
# ax.legend()
# #plt.savefig('VRE_vLPM_12204_Delta.png')
# plt.close()
# print('Thank You!')
# #sys.exit()
# print('avlrsn_vlpmsn1154 plotted with log axes. Thank You!')
###########################################################################################
###########################################################################################
#cver v cvlpm
###########################################################################################
fig, ax = plt.subplots()
for name,group in reggrp:
	ax.plot(group['cver'], group['cvlpmad'], label=name, marker = 'o', linestyle='')
    # ax.set_ylim(group['mrva_ymin'],0)
# ax.plot(mergeADs['varlogreseff'], mergeADs['varianceLPMages'], marker = 'o', linestyle='')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Coefficient of variation of effective resistivity')
#ax.set_xlabel('Variance of effective resistivity, in Ohms squared - meters squared')
ax.set_ylabel('Coefficient of variation of tracer age distribution')
ax.legend()
plt.savefig('cVeR_cvLPM_4115_byreg.png')
plt.close()
print('Thank You!')
#sys.exit()
print('avlrsn_vlpmsn1154 plotted with log axes. Thank You!')
###########################################################################################
###########################################################################################
#cvcvr v cvlpm
###########################################################################################
fig, ax = plt.subplots()
for name,group in reggrp:
	ax.plot(group['cvcvr'], group['cvlpmad'], label=name, marker = 'o', linestyle='')
    # ax.set_ylim(group['mrva_ymin'],0)
# ax.plot(mergeADs['varlogreseff'], mergeADs['varianceLPMages'], marker = 'o', linestyle='')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Coefficient of variation of coefficient of variation of resistivity')
#ax.set_xlabel('Variance of effective resistivity, in Ohms squared - meters squared')
ax.set_ylabel('Coefficient of variation of tracer age distribution')
ax.legend()
plt.savefig('cVcVR_cvLPM_4115_byreg.png')
plt.close()
print('Thank You!')
#sys.exit()
print('avlrsn_vlpmsn1154 plotted with log axes. Thank You!')
###########################################################################################
###########################################################################################
sys.exit()