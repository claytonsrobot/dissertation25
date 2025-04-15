#cd C:\Users\mgratzer\Documents\General\pubs\FY21\Update\figs\working\age

#import packages
import os
import numpy as np
import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
from pprint import pprint

from src.directories import Directories

class T4:
    mergeADs = None
    mergeADs_df1_s = None
    mergeADs_mrva = None
    mergeADs_sites = None
    mergeADsshp = None

    def __init__(self):
        self.nope = "nope"

    @classmethod
    def set_reggrp(cls, input):
        cls.reggrp = input


    @classmethod
    def get_reggrp(cls):
        return cls.reggrp


        
    def run():
        T4.section0_mpl_config()
        mergeADs,mergeADs_sites = T4.section1_import()
        reggrp = T4.section2_df(mergeADs,mergeADs_sites)
        T4.set_reggrp(reggrp)
        
    def graph():
        T4.plot_acvr_v_cvlpm(T4.get_reggrp())
        #T4.plot_MER_v_cvlpm(T4.get_reggrp())
        T4.plot_cver_v_cvlpm(T4.get_reggrp())
        T4.plot_cvcvr_v_cvlpm(T4.get_reggrp())

        
    def section0_mpl_config():
        matplotlib.rcParams['pdf.fonttype'] = 42
        matplotlib.rcParams['ps.fonttype'] = 42

    def section1_import():
        #mergeADs=pd.read_csv(os.path.join('../../../../../../../../../../github/map_gwage/MERASwd/Scripts','mads4lpmstats3235.csv'))
        Directories.set_project_dir(r"C:\\Users\\user\\Documents\\dev\\dissertation25\\projects\\task4\\")
        Directories.get_import_dir()
        mergeADs=pd.read_csv(os.path.join(Directories.get_import_dir(),'mads4lpmstats3235.csv'))
        mergeADsshp=mergeADs.shape
        print('mergeADsshp:',mergeADsshp)
        print('mergeADs:',mergeADs)


        def data_adjustment_mergeADs(mergeADs):
            mergeADs=mergeADs.replace(-9999,np.nan)
            mergeADs=mergeADs.replace(0,np.nan)
            mergeADs.loc[:,'GWSys']='TRRC'
            mergeADs.loc[mergeADs['Layer']=='MRVA','GWSys']='MRVA'
            mergeADs.loc[mergeADs['Layer'].isin(['CLBR','CNZC','LCAQ','MCAQ','UCAQ']),'GWSys']='CLBR'
            mergeADs.loc[mergeADs['Layer'].isin(['MWAQ','LWAQ','UWAQ']),'GWSys']='WLCX'
            return mergeADs

        mergeADs = data_adjustment_mergeADs(mergeADs)
        print('mergeADs,2:',mergeADs)
        mADcols=mergeADs.columns.unique().tolist()
        print(mADcols)
        mergeADs_sites = mergeADs['siteag'].unique().tolist()
        print('number of unique sites in mergeADs:',len(mergeADs_sites))#88
        print('\t')
        print('\t')
        return mergeADs,mergeADs_sites

    def section2_df(mergeADs,mergeADs_sites):

        # read Table 1
        df1=pd.read_csv(os.path.join(Directories.get_import_dir(),'joint1reg833.csv'))
        print(df1.columns.tolist())
        df1shp=df1.shape
        print('df1: ', df1shp)
        df1_sites = df1['siteag'].unique().tolist()
        print('number of unique sites in df1:',len(df1_sites))#88
        print('\t')
        
        mergeADs_df1_s=list(set(mergeADs_sites)-set(df1_sites))
        print('mergeADs_df1_s:',mergeADs_df1_s)
        print('\t')
        #sys.exit()
        mergeADs=mergeADs.merge(df1,how='left',on='siteag')
        mergeADs_mrva=mergeADs.loc[mergeADs['GWSys']=='MRVA']
        #sys.exit()
        
        reggrp=mergeADs_mrva.groupby('region')
        return reggrp 
    def plot_acvr_v_cvlpm(reggrp):
        ###########################################################################################
        #acvr v cvlpm
        ###########################################################################################
        fig, ax = plt.subplots()
        for name,group in reggrp:
            ax.plot(group['acvr'], group['cvlpmad'], label=name, marker = 'o', linestyle='')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.axline((.05, .05), (5, 5), color='r', linestyle='--', label='1:1 line')
        ax.set_xlabel('Average coefficient of variation of resistivity')
        ax.set_ylabel('Coefficient of variation of tracer age distribution')
        ax.legend()
        plt.savefig(Directories.get_export_dir()+'acvr_cvLPM_4115_byreg.png')
        plt.close()
        print('Thank You!')
        #sys.exit()
        print('avlrsn_vlpmsn1154 plotted with log axes. Thank You!')
    #def plot_MER_v_cvlpm(reggrp):
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
    def plot_cver_v_cvlpm(reggrp):
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
        ax.axline((.01, .01), (10, 10), color='r', linestyle='--', label='1:1 line')
        ax.set_xlabel('Coefficient of variation of effective resistivity')
        #ax.set_xlabel('Variance of effective resistivity, in Ohms squared - meters squared')
        ax.set_ylabel('Coefficient of variation of tracer age distribution')
        ax.legend()
        plt.savefig(Directories.get_export_dir()+'cVeR_cvLPM_4115_byreg.png')
        plt.close()
        print('Thank You!')
        #sys.exit()
        print('avlrsn_vlpmsn1154 plotted with log axes. Thank You!')
    def plot_cvcvr_v_cvlpm(reggrp):
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
        ax.axline((.01, .01), (10, 10), color='r', linestyle='--', label='1:1 line')
        # Set axis limits
        #ax.set_xlim(0.1, 1000)
        #ax.set_ylim(0.1, 1000)
        ax.set_xlabel('Coefficient of variation of coefficient of variation of resistivity')
        #ax.set_xlabel('Variance of effective resistivity, in Ohms squared - meters squared')
        ax.set_ylabel('Coefficient of variation of tracer age distribution')
        ax.legend()
        plt.savefig(Directories.get_export_dir()+'cVcVR_cvLPM_4115_byreg.png')
        plt.close()
        print('Thank You!')
        #sys.exit()
        print('avlrsn_vlpmsn1154 plotted with log axes. Thank You!')
        ###########################################################################################
        ###########################################################################################
        #sys.exit()

if __name__ == "__main__":
    T4.run()
    T4.graph()