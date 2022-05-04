import pandas as pd
import numpy as np

#from pandas_cli.myutils import BaseUtils
from ..myutils import show_choices

class BasePanda(object):
    def __init__(self, data=None, ftype=None, abs_path=None):

        self.abs_path = abs_path

        if abs_path != None:
            data=self.abs_path.path
            self.ftype = self.abs_path.name.rsplit('.')[1]
        else:
            self.ftype = ftype

        if self.ftype == 'json':
            try:
                self.original_frame = pd.read_json(data)
            except:
                print('json data not loaded properly')

        elif self.ftype == 'xlsx':
            try:
                #openpyxl is required for the DirEntry type but I think I fixed it with the rel path above
                import openpyxl
                self.original_frame = pd.read_excel(data)
            except:
                print('excel data not loaded properly')

        elif self.ftype == 'csv':
            try:
                self.original_frame = pd.read_csv(data, index_col=0) # should make index_col optional
            except:
                print('csv data not loaded properly, try adjusting delimeters')

        else:
            self.original_frame = pd.DataFrame(data)
        
        self.working_frame = self.original_frame.copy()
        self.cols = self.get_wk_cols()
        self.og_cols = self.original_frame.columns.to_list()
        self.MI = None

    def len(self):
        return len(self.working_frame)

    def reset(self):
        self.working_frame = self.original_frame.copy()

    def show_me(self):
        print(self.working_frame)

    def select_cols(self):
        selected = show_choices(self.original_frame.columns.to_list(), msg=f'select_col from {self.__str__()}', color3='green')
        self.working_frame = self.original_frame[selected]
        return self.working_frame[selected]

    # maybe there shoudl be set/get functions.

    def get_wk_cols(self):
        self.cols = self.working_frame.columns.to_list()
        return self.working_frame.columns.to_list()

    #selected is a list if once==False (Default)
    def make_mi(self):
        selected = show_choices(self.get_wk_cols(), msg='make_mi')
        for i in selected:
            print(self.working_frame[i].dtype)
        try:
            self.MI = pd.MultiIndex.from_frame(self.working_frame[selected])
        except TypeError:
            #Force to string
            self.MI = pd.MultiIndex.from_frame(self.working_frame[selected].astype(str))
        except ValueError:
            print("Type not supported nothing changed")
        return self.MI

    def sort(self):
        selected = show_choices(self.working_frame.columns.to_list(), msg='Select column to sort by', once=True)
        print(f'len(selected)={len(selected)}')
        try:
            self.working_frame = self.working_frame.sort_values(selected)
        except:
            print("Something went wrong")

    #selected is a single entry if once==True
    def sort_mi(self):
        selected = show_choices(list(self.MI.names), msg='Select item to sort MI', once=True)
        print(f'len(selected)={len(selected)}')
        try:
            self.MI = self.MI.sort_values(selected)
        except:
            print("Something went wrong")

    def swap_mi(self):
        selected = show_choices(self.MI.names)
        if len(selected) == 2:
            try:
                return self.MI.swaplevels(selected[0],selected[1])
            except:
                print("swap_mi failed. only 2 cols please. needs MI")
    
    def search(self):

        """This will search the values in a column for the string entered on the cli"""

        selected=show_choices(self.get_wk_cols(),msg='column to search on',once=True)
        print('What would you like to search for?')
        x=input(f'{selected}: ')
        B=self.working_frame.copy()

        astr="***Excluded from search***"

        try:
            B_notna=B.loc[B[selected].notna()]
            B_na=B.loc[B[selected].isna()]
            print(f'{astr}\n {B_na[selected]} ')
            print(f'**************************')
            B=B_notna.loc[B_notna[selected].str.contains(x)]

        #ValueError: Cannot mask with non-boolean array containing NA / NaN values
        except ValueError:
            print('The data should be string. The handling of Nan\'s could be better')
        return B

    def auto_search(self,term,col):
        """same as search but with data already supplied"""
        B=self.working_frame.copy()
        astr="***Excluded***"
        #B=B.loc[[x in y for y in B[selected]]]
        try:
            B_notna=B.loc[B[col].notna()]
            B_na=B.loc[B[col].isna()]
            B=B_notna.loc[B_notna[col].str.contains(term,regex=False)]
            if not B.empty:
                return B.reset_index(drop=True)
        except ValueError:
            print('The data could be better. The handling of Nan\'s could be better')

    def drop_rows(self):
        selected=show_choices(self.get_wk_rows(), msg='rows to drop', once=False)
        self.working_frame.drop(selected, axis=0, inplace=True)
        x=input('Reset index? Y/n, careful if you don\'t have integer index')
        if 'n' not in x or 'N' not in x:
            self.working_frame.reset_index(drop=True,inplace=True)
    
    def drop_cols(self):
        selected=show_choices(self.get_wk_cols(),msg='columns to drop',once=False)
        self.working_frame.drop(selected, axis=1, inplace=True)

    # string to list
    def split(self, pat='\n\n'):
        print("creates a new frame/series what now")
        selected=show_choices(self.get_wk_cols(), msg='column to split',once=True)
        B=self.working_frame[selected].str.split(pat=pat)
        return B
    
    #list to b.a.p. (big ass panda)
    def explode(self):
        """
        this does nothing. should explode the dataframe 
        """
        selected=show_choices(self.get_wk_cols(),msg='column to "Explode"',once=True)
        x=input(f'{selected}: ')
        #B=self.working_frame.copy()
        
    #takes a row and makes it the column header
    def pop_cols(self):
        selected=show_choices(self.get_wk_rows(), msg='row to replace columns', once=True)
        self.working_frame.columns=self.working_frame.iloc[selected].values
        self.show_me()
    
    def transform(self):
        self.working_frame=self.working_frame.T

    #total afterthought lol also you used Baseutil bause you lose output to toolkit
    def show_a_column(self):
        #selected=show_choices(self.get_wk_cols(), msg='Select a column',once=True)
        selected=show_choices(self.get_wk_cols(), msg='Select a column',)
        print(self.working_frame[selected])

    def __str__(self):
        try:
            return str(self.abs_path.name)
        except:
            return 'File name not found?'

#class XLPanda(BasePanda):
#    def __init__(self, **kwargs):
#        super().__init__(self, **kwargs)
#        self.ftype = 'xlsx'

#class JSONPanda(BasePanda):
#    ftype='json'
#    """
#    this assumes that you recieve a json file with
#    """
#    def get_data(self):
#        sub_data = self.working_frame['data']
#        emp = pd.DataFrame()
#        emp = emp.append([x[1] for x in sub_data.items()])
#        return BasePanda(data=emp)
