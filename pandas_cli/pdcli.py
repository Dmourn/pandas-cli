#from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import prompt, clear

from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.completion import WordCompleter

from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding import KeyBindings

#Keep this. refers to the implicit instantion of the Application class
from prompt_toolkit.application.current import get_app

import os
import re
import time

from prompt_toolkit.application import Application
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory, ConditionalAutoSuggest

from prompt_toolkit.shortcuts import CompleteStyle, ProgressBar, clear
from prompt_toolkit.shortcuts.progress_bar import formatters

import click

from prompt_toolkit.formatted_text import ANSI
from random import randint

#Gets rid of the openpyxl message possibly others
import warnings
warnings.simplefilter("ignore")

#from pandas_cli.myutils import show_choices

# this syntax breaks my debugging method
#from .myutils import show_choices
#from .core import dpandas
#from .internal import grammar
from pandas_cli.myutils import show_choices
from pandas_cli.core import dpandas
from pandas_cli.internal import grammar

DEBUG=True

def rainbow(lent=6,char='🐼'):
    cl=[
    "\x1b[38;5;50m",
    "\x1b[38;5;100m",
    "\x1b[38;5;214m",
    "\x1b[38;5;90m",
    "\x1b[38;5;80m",
    ]
    ol = [cl[randint(0,len(cl)-1)] for x in range(lent)]
    return char.join(ol)

def get_data_dir(adir='./data'):
    return list(os.scandir(adir))

# we have this already. ??? do we
# note to self. make better comments
def select_file(alist):
    pass

def bottom_toolbar():
    "Display the current input mode."
    if get_app().editing_mode == EditingMode.VI:
        return " [F4] Vi "
    else:
        return " [F4] Emacs "

import string,random
def random_string():
    lets = string.ascii_letters
    return ''.join([lets[random.randint(0,len(lets)-1)] for x in lets])

# why are you here?
A=dpandas.pd.DataFrame(map(lambda x: [random_string(),random_string(),random_string()],range(3)))

bindings = KeyBindings()

split_input = re.compile('\W')
clear()
def main():

    @bindings.add("f4")
    def _(event):
        app = event.app
        "Toggle between Emacs and Vi mode."
        if app.editing_mode == EditingMode.EMACS:
            app.editing_mode = EditingMode.VI
        else:
            app.editing_mode = EditingMode.EMACS

    @bindings.add("c-c")
    @bindings.add("c-q")
    def _(event):
        def quit():
            running=False
            event.app.exit()
        quit()

    history = InMemoryHistory()
    session = PromptSession(history=history, auto_suggest=AutoSuggestFromHistory(), enable_history_search=True)
    data_dir='./data'

    my_lexer, my_style,my_completion = grammar.create_lexer()
    gr = grammar.create_grammar()

    completion_list = ['exit', 'quit', 'load', 'trans',
                       'show', 'cols', 'split', 'select',
                       'search', 'reset', 'save',
                       'sort', 'multi', 'rows',
                        'drop', 'chcols', 'pop']

    dpandas_completer = WordCompleter(completion_list)
    running = True
    rain = rainbow()
    while running == True:

        pstring = ANSI(rainbow()+'> ')
        text = session.prompt(pstring, bottom_toolbar=bottom_toolbar, lexer=my_lexer, style=my_style, completer=dpandas_completer, key_bindings=bindings, complete_style=CompleteStyle.COLUMN) 

        #you did this manualy and its a shit show
        ma = gr.match(text)
        if ma:
            vl = ma.variables()
            print(vl.get('noun1'))

        try:
            #spliting by whitespace
            res = split_input.findall(text)
            tl=text.split(res[0])
            #print(f'split: {tl}')
        except:
            tl = [text]


        if tl[0] == 'exit'  or tl[0] == 'quit' or tl[0] == 'q':
            print("Goodbye!") 
            running = False
            try:
                if DEBUG:
                    return panda_list
            except:
                break

        elif tl[0] == 'clear':
            clear()
        elif tl[0] == 'load':
            dl = os.scandir(data_dir)
            
            panda_list = []
            pd_str_list = []
          
            custom_formatters = [
                formatters.Label(suffix=": "),
                formatters.Bar(start="|", end="|", sym_a="#", sym_b="#", sym_c="-"),
                formatters.Text(" "),
                formatters.Progress(),
                formatters.Text(" "),
                formatters.Percentage(),
                formatters.Text(" [elapsed: "),
                formatters.TimeElapsed(),
                formatters.Text(" left: "),
                formatters.TimeLeft(),
                formatters.Text(", "),
                formatters.IterationsPerSecond(),
                formatters.Text(" iters/sec]"),
                formatters.Text("  "),
            ]

            with ProgressBar(formatters=custom_formatters) as pb:
                #for i in panda_list:
                #print("Loading data dir")
                for entry in pb(dl, label=f"Loading data"): #, total=len(panda_list)):
                    panda_list.append(dpandas.BasePanda(abs_path=entry))
                    time.sleep(.01)
                    #print(f'Loaded {i}')
                    pd_str_list.append(entry.__str__())

            dpandas_completer.words += [x.__str__() for x in panda_list]

        #this should look for cols 
        elif tl[0] == 'show' or tl[0] == 'ls' or tl[0] == 'sh':
            count = 0
            try:
                if len(tl)>=1 and (tl[1:]==['' for x in tl[1:]] or tl==[1]): #lol
                    print('\n'.join([x.__str__() for x in panda_list]))
                    #print([x.__str__() for x in pd_str_list])
                elif tl[1]=='row':
                    print('rows not implemented yet cause strings/numbers')

                elif tl[1]=='col':
                    for i in tl[2:]:
                        for j in panda_list:
                            if i == j.__str__():
                                count += 1
                                j.show_a_column()    
                else:
                    for i in tl[1:]:
                        for j in panda_list:
                            if i == j.__str__():
                                count += 1
                                starlen = 50-len(str(count))
                                print(f'{count}'+starlen*'*')
                                j.show_me()
                                print(50*'*')
            except:
                print('Something whent wrong, did you load first?')

        elif tl[0] == 'cols':
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        print('\n'.join(j.get_wk_cols()))

        elif tl[0] == 'trans':
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        j.transform()
                        print(j.working_frame)

        elif tl[0] == 'reset': #  and tl[1] in pd_str_list:
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        j.reset()

        elif tl[0] == 'search': #  and tl[1] in pd_str_list:
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        try:
                            count += 1
                            starlen = 50-len(str(count))
                            print(f'{count}'+starlen*'*')
                            j.working_frame = j.search()
                            j.show_me()
                            print(50*'*')
                        except AttributeError:
                            print("\033[91mYou may only search string data.\033[0m")

        elif tl[0] == 'sel' or tl[0] == 'select':
            count = 0
            try:
                if tl[1]=='rows':
                    print('rows not implemented yet cause strings/numbers')

                elif tl[1]=='cols':
                    for i in tl[2:]:
                        for j in panda_list:
                            if i == j.__str__():
                                count += 1
                                j.select_cols()    
            except IndexError:
                print('use select cols')

        elif tl[0] == 'chcols':
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        print(f'{count}'+(50-len(str(count)))*'*')
                        j.select_cols()
                        print(50*'*')

        elif tl[0] == 'sort': #  and tl[1] in pd_str_list:
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        print(f'{count}'+(50-len(str(count)))*'*')
                        j.sort()
                        print(50*'*')

        elif tl[0] == 'save': #  and tl[1] in pd_str_list:
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        #should save csv by default for size. also good place to use your filetypes. So janky to update lol
                        if DEBUG==True:
                            #file types to save as
                            y=show_choices({'1':'csv','2':'xlsx','3':'json'}, once=True, getvals=True)
                            print(f'you picked {y}')
                            ext=y
                        x = input(f'Save {i} output as *.{ext}: ')
                        file_name = x+'.'+ext
                        y = input('Drop index? Y/n ')
                        try:
                            if 'n' in y or 'N' in y:
                                #ihatethis
                                if ext == 'xlsx':
                                    j.working_frame.to_excel(file_name)
                                if ext == 'csv':
                                    j.working_frame.to_csv(file_name)
                                if ext == 'json':
                                    j.working_frame.to_json(file_name)
                            else:
                                if ext == 'xlsx':
                                    j.working_frame.to_excel(file_name, index=False)
                                if ext == 'csv':
                                    j.working_frame.to_csv(file_name, index=False)
                                if ext == 'json':
                                    j.working_frame.to_json(file_name)
                        except:
                            print("Nothing saved")

        elif tl[0] == 'multi':
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        try:
                            ok=j.make_mi()
                            j.working_frame.index = j.MI
                        except TypeError:
                            print("nothing happend?")

    
        elif tl[0] == 'drop':
            count = 0
            if tl[1]=='rows':
                for i in tl[2:]:
                    for j in panda_list:
                        if i == j.__str__():
                            count += 1
                            j.drop_rows()

            elif tl[1]=='cols':
                for i in tl[2:]:
                    for j in panda_list:
                        if i == j.__str__():
                            count += 1
                            j.drop_cols()

        elif tl[0] == 'pop':
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        j.pop_cols()


        elif tl[0] == 'pager' or tl[0] == 'page':
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        click.echo_via_pager(j.working_frame.to_string())
            
        else:
            print(f'you said: {text} and nothing happend...\n')
    

if __name__=='__main__':
    pl = main()
    try:
        a,b,c,d=pl
    except:
        pass
