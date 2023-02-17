# Python 3.x
from urllib.request import urlopen, urlretrieve, quote
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd
import os
import sys
import glob
import schedule
import time
import logging


url = 'https://www.gov.uk/government/statistics/oil-and-oil-products-section-3-energy-trends'
u = urlopen(url)
try:
    html = u.read().decode('utf-8')
finally:
    u.close()

soup = BeautifulSoup(html, "html.parser")
soup=soup.find_all('h3', text=re.compile('natural gas liquids and feedstocks'))
urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(soup))
filename = urls[0].rsplit('/', 1)[-1]
resp = requests.get(urls[0])




def getFile(path):
    local_dir=path
    output = open(local_dir+filename, 'wb')
    output.write(resp.content)
    output.close()
    data=pd.read_excel(resp.content, sheet_name='Quarter')
    print("------Downloaded File in your Path")
    return data
    
def getNewFile(filename,path):
    lfilename=filename
    path=path
    if(lfilename!=lfilename):
        data=getFile(path)
        return data
    else:
        print("No New file arrived in website")
        
    
#Profiling Method
#Profiling Method
def get_basic_profile(dataframe):
    df=dataframe
    quantile_range = 0.5
    results = {}
    
    for column in dataframe.columns:
        count = df[column].count()
        nans = df[column].isna().sum()
        min = df[column].min()
        max = df[column].max()
        median = df[column].median()
        std = df[column].std()
        kurt = df[column].kurt()
        skew = df[column].skew()
        quant = df[column].quantile(q=quantile_range)
        
        results[column] = {'count': count,
                            'count_na': nans,
                            'min':min,
                            'max':max,
                            'median':median,
                            'std':std,
                            'kurt':kurt,
                            'skew':skew,
                            f'quant {quantile_range}':quant}
 
    return results

    

#Check Local Directory
lfilename=''
local_dir=''
if len(sys.argv) > 1:   
    local_dir = sys.argv[1]
    if os.path.exists(local_dir):
        excel_files = glob.glob(os.path.join(local_dir, '*.xlsx'))
        if(len(excel_files)<1):
            data=getFile(local_dir)
            #Clean and save csv
            df=data.iloc[3::, :]
            print("Cleaned the Data")
            dft=df.transpose()
            dft=dft.reset_index(drop=True)
            dft.columns = dft.iloc[0]
            dft=dft.iloc[1::, :]
            # renaming the column "Column1"
            dft.rename(columns = {"Column1": "Quarters"},inplace = True)
            #Saving Cleanded file to csv
            fncsv=local_dir+filename.replace('.xlsx', '.csv')
            dft.to_csv(fncsv)
            print("Saved the data csv after cleaning to local path")
            #Basic Profiling for 
            profileb=dft.describe(include='all')
            prbcsv=local_dir+filename.replace('.xlsx', '')+"_data_profiling.csv"
            profileb.to_csv(prbcsv)
            print("Saved the Basic profiling as csv")
            ##Applying Advance Profiling
            dftt=dft.iloc[::, 1::]
            dftt = dftt.astype('float')
            profilen=get_basic_profile(dftt)
            profilen = pd.DataFrame.from_dict(profilen)
            prbcsv=local_dir+filename.replace('.xlsx', '')+"_numeric_data_profiling.csv"
            profilen.to_csv(prbcsv)
            print("Saved the Advance Basic profiling as csv")
        else:
            # loop over the list of csv files
            for f in excel_files:
                lfilename=str(f.split("/")[-1])
                data=getNewFile(lfilename,local_dir)   
                #Clean and save csv
                df=data.iloc[3::, :]
                print("Saved the data csv after cleaning to local path")
                dft=df.transpose()
                dft=dft.reset_index(drop=True)
                dft.columns = dft.iloc[0]
                dft=dft.iloc[1::, :]
                # renaming the column "Column1"
                dft.rename(columns = {"Column1": "Quarters"},inplace = True)
                #Saving Cleanded file to csv
                fncsv=local_dir+lfilename.replace('.xlsx', '.csv')
                dft.to_csv(fncsv)
                #Basic Profiling for 
                profileb=dft.describe(include='all')
                prbcsv=local_dir+lfilename.replace('.xlsx', '')+"_data_profiling.csv"
                profileb.to_csv(prbcsv)
                print("Saved the Basic profiling as csv")
                ##Applying Advance Profiling
                dftt=dft.iloc[::, 1::]
                dftt = dftt.astype('float')
                profilen=get_basic_profile(dftt)
                profilen = pd.DataFrame.from_dict(profilen)
                prbcsv=local_dir+lfilename.replace('.xlsx', '')+"_numeric_data_profiling.csv"
                profilen.to_csv(prbcsv) 
                print("Saved the Advance Basic profiling as csv")
    else:
        print("Please Pass Local Directory EG: python rjcf.py /Users/abhinitakumari/Desktop/RJC")
else:
    print("Please Pass Local Directory EG: python rjcf.py /Users/abhinitakumari/Desktop/RJC")