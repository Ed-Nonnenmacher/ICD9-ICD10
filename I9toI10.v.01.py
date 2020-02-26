import pandas as pd
import numpy as np
import os,re,sys,csv


##I9_Path and i10_Path are to hold paths to directory containing ICD9 and ICD10 GEMS .txt files
i9_Path=r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\icddata\gems_proj\diagnosis_gems_2018\2018_I9gem.txt'
i10_Path=r'C:\Users\enonnenmacher\AppData\Local\Programs\Python\Python37\icddata\gems_proj\diagnosis_gems_2018\2018_I10gem.txt'

import pandas as pd
import numpy as np
import os,re,sys,csv

##NOTES
##
##
##TASKS
##Have an automated way to search further into ICD child codes.  Like 477 has no match, but 4770 4771 and 4772 does. --what would be threshold to stop?  try all 477x, or all 477xx, or all 477xxx???
##
##
##Completed tasks/goals
##
##fwd---as class and func
##bwd---as class and func
##sm---as class and func
##Possible to make independent set of items for fwd and bwd, that way a fwb match can list
##which codes were pulled from which function


##-------------------------------------------------------------------------------
##------------------------MATCHING CLASS-------------------------------------
##-------------------------------------------------------------------------------


class data_tools:
    '''superclass containing tools/methods for managing data
    get_data(self,path,cols):
        returns pandas dataframe of .txt file

    dict_append(self,base,new):
        returns base dictionary containing data structure as item, with appended items of new dictionary to base dictionary'''


    def __init__(self,i9_Path=i9_Path,i10_Path=i10_Path):
        self.i9_Path=i9_Path
        self.i10_Path=i10_Path
        self.df9=self.get_data(self.i9_Path,['I9','I10','FLAG'])
        self.df10=self.get_data(self.i10_Path,['I10','I9','FLAG'])

    def get_data(self,path,cols):
        reg=re.compile(r'(\w*) +(\w*) +(\w*)')
        with open(path) as file:
            reader=csv.reader(file)
            return pd.DataFrame([list(reg.search(str(i)).groups()) for i in reader],columns=cols)

    def dict_append(self,base,new):
        for i in new:
            if i not in base.keys():
                base[i]=new[i]
                continue
            else:
                base[i].extend(new[i])
                base[i]=list(set(base[i]))
        return base



    

class data(data_tools):
    '''subclass to data_tools
    Inherits self.i9_Path, self.i_10Path, self.df9,self.df10, self.get_data, self.dict_append
    Class was developed entirely for efficiency, as timing is about 2/3 of its function counterparts

    def fwd(self,los):
        returns forward mathcing result from I9 GEMS to I10 GEMS
        returned dtype(dict)

    def bwd(self,los):
        returns backward matching results from I10 GEMs to I9 GEMS
        returned dtype(dict)

    def fwb(self,los):
        combined result of forward backward matching
        returned dtype(dict)

    def sm(self,los):
        secondary matching, where secondary ICD9 codes are identified, and provided a forward backward match as well.
        seconary ICD9 codes are identified as other ICD9 codes that share ICD-10 codes, either through forward or backward matching
        returned dtype(dict)'''
    
    def __init__(self):
        super().__init__()

    def fwd(self,los):
        '''los=icd9 codes to convert to icd 10'''
        a=dict()
        ##
        for i in los:
            if i in a.keys():
                a[i].extend(self.df9[self.df9['I9']==i]['I10'].values)
                a[i]=list(set(a[i]))
                continue
            else:
                a[i]=list(self.df9[self.df9['I9']==i]['I10'].values)
        return a



    def bwd(self,los):
        '''los=icd9 codes to convert to icd 10'''
        a=dict()

        for i in los:
            if i in a.keys():
                a[i].extend(list(self.df10[self.df10['I9']==i]['I10'].values))
                a[i]=list(set(a[i]))
            else:
                a[i]=list(self.df10[self.df10['I9']==i]['I10'].values)
        return a



    def fwb(self,los):
        f=self.fwd(los)
        b=self.bwd(los)
        return self.dict_append(f,b)




    def sm(self,los):
        fwb_1=self.fwb(los)
        secondary=list()
        secondary.extend(list(set(self.df9[self.df9['I10'].isin([i for x in fwb_1.values() for i in x])]['I9'])))
        secondary.extend(list(set(self.df10[self.df10['I10'].isin([i for x in fwb_1.values() for i in x])]['I9'])))
        print('Secondary ICD-9 codes: {}'.format(secondary))
        
        return self.dict_append(fwb_1,self.fwb(secondary))


##-------------------------------------------------------------------------------
##------------------------MATCHING FUNCTIONS-------------------------------------
##-------------------------------------------------------------------------------

'''Please refer to documentation in above class for return info.  Global scope functions perform almost exactly as their class counterparts.'''

def get_data(path,cols):
    reg=re.compile(r'(\w*) +(\w*) +(\w*)')
    with open(path) as file:
        reader=csv.reader(file)
        return pd.DataFrame([list(reg.search(str(i)).groups()) for i in reader],columns=cols)
    
def dict_append(base,new):
    '''goal is to update the items of base dict keys (which are lists), by appending/extending the items of new dict to the base dict'''
    for i in new:
        if i not in base.keys():
            base[i]=new[i]
            continue
        else:
            base[i].extend(new[i])
            base[i]=list(set(base[i]))
    return base


def fwd(los):
    a=dict()
    ##
    
    for i in los:
        if i in a.keys():
            a[i].extend(df9[df9['I9']==i]['I10'].values)
            a[i]=list(set(a[i]))
            continue
        else:
            a[i]=list(df9[df9['I9']==i]['I10'].values)
        
    return a

def bwd(los):
    a=dict()
        
    ##
    
    for i in los:
        if i in a.keys():
            a[i].extend(list(df10[df10['I9']==i]['I10'].values))
            a[i]=list(set(a[i]))
        else:
            a[i]=list(df10[df10['I9']==i]['I10'].values)
    return a




def fwb(los):
    a=fwd(los)
    b=bwd(los)
    return dict_append(a,b)


def sm(los):
    fwb_1=fwb(los)
    secondary=list()
    secondary.extend(list(set(df9[df9['I10'].isin([i for x in fwb_1.values() for i in x])]['I9'])))##forward match of secondary
    secondary.extend(list(set(df10[df10['I10'].isin([i for x in fwb_1.values() for i in x])]['I9'])))##backward match of secondary
    return list(set(secondary)),dict_append(fwb_1,fwb(secondary))


   
df9=get_data(i9_Path,['I9','I10','FLAG'])
df10=get_data(i10_Path,['I10','I9','FLAG'])




##---------------------------------------------
##--Leaving these samples here, should anyone--
##---------want to test with them--------------
##--------------ICD9 samples-------------------

a='''477
4770
4771
4772
4778
4779
6923
6926
7080
99527
9953
99560
99561
99562
99563
99564
99565
99566
99567
99568
99569
37205
37214
52566
V14
V140
V141
V142'''.split('\n')
