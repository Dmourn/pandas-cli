import os
import re
import sys

from random import randint

from prompt_toolkit.shortcuts import CompleteStyle, ProgressBar, clear
from prompt_toolkit.completion import WordCompleter

from prompt_toolkit.enums import EditingMode
from prompt_toolkit.key_binding import KeyBindings

# Keep this. refers to the implicit instantion of the Application class
from prompt_toolkit.application.current import get_app

# from prompt_toolkit.application import Application
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

# from prompt_toolkit.auto_suggest import AutoSuggestFromHistory, ConditionalAutoSuggest

from prompt_toolkit.shortcuts.progress_bar import formatters

from prompt_toolkit.formatted_text import ANSI

import click


from pandas_cli import myutils
from pandas_cli.core import dpandas
from pandas_cli.internal import grammar
from pandas_cli.myutils import show_choices

DEBUG = True


def get_data_dir(adir="./data"):
    try:
        return list(os.scandir(adir))
    except FileNotFoundError:
        print("./data not found. Try specifying --dir ")
        sys.exit(1)


def rainbow(lent=6, char="🐼"):
    """Silly prompt"""
    color_list = [
        "\x1b[38;5;50m",
        "\x1b[38;5;100m",
        "\x1b[38;5;214m",
        "\x1b[38;5;90m",
        "\x1b[38;5;80m",
    ]
    prompt_chars = [color_list[randint(0, len(color_list) - 1)] for x in range(lent)]
    return char.join(prompt_chars)


def bottom_toolbar():
    "Display the current input mode."
    if get_app().editing_mode == EditingMode.VI:
        return " [F4] Vi "
    return " [F4] Emacs "


def selector(panda_item, once: bool, msg="a thing"):
    """Takes property of BasePanda and returns list of selection"""
    col_dict = myutils.zd(panda_item)
    selected = show_choices(col_dict, once=once, msg=msg)
    return selected


bindings = KeyBindings()

split_input = re.compile(r"\W")


@click.command()
@click.option("-e", "--execute", type=str, help="execute command for testing")
def cli(execute):
    """
    Main repl, currently it is doing too much
    """
    # clear()

    @bindings.add("f4")
    def _(event):
        app = event.app
        if app.editing_mode == EditingMode.EMACS:
            app.editing_mode = EditingMode.VI
        else:
            app.editing_mode = EditingMode.EMACS

    @bindings.add("c-c")
    @bindings.add("c-q")
    def _(event):
        def quit():
            running = False
            event.app.exit()

        quit()

    my_lexer, my_style, my_completion = grammar.create_lexer()
    gr = grammar.create_grammar()

    dir_list = get_data_dir()

    completion_list = [
        "exit",
        "quit",
        "load",
        "trans",
        "show",
        "cols",
        "split",
        "select",
        "ls",
        "search",
        "reset",
        "save",
        "sort",
        "multi",
        "rows",
        "drop",
        "chcols",
        "pop",
    ]

    dpandas_completer = WordCompleter(completion_list)

    prompt_string = ANSI(rainbow() + "> ")
    history = InMemoryHistory()
    session = PromptSession(
        message=prompt_string,
        history=history,
        auto_suggest=AutoSuggestFromHistory(),
        lexer=my_lexer,
        enable_history_search=True,
        style=my_style,
        bottom_toolbar=bottom_toolbar,
        completer=dpandas_completer,
        key_bindings=bindings,
        complete_style=CompleteStyle.COLUMN,
    )
    running = True

    while running is True:

        text = session.prompt()

        seperator = 50 * "*"

        # matched = gr.match(text)
        # if matched:
        #    vl = matched.variables()
        #    #print(vl.get("noun1"))

        # FIXME This is shit tier parsing. You are relying on the execption
        try:
            # spliting by whitespace
            if execute:
                print("Executing from command line")
                res = split_input.findall(execute)
                print(f"exec: {execute}\tres: {res}\t text:{text}\n")
                # tl=text.split(res[0])
                tl = [execute]
            else:
                print("NOT Executing from command line")
                res = split_input.findall(text)
                tl = text.split(res[0])
            # print(f'split: {tl}')
        except:
            print("\033[31mtry statement failed line:190\033[0m")
            tl = [text]

        if tl[0] == "clear":
            clear()

        elif tl[0] == "load":
            # dir_list = os.scandir(data_dir)

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

            with ProgressBar(formatters=custom_formatters) as p_bar:
                for entry in p_bar(dir_list, label="Loading data"):
                    panda_list.append(dpandas.BasePanda(abs_path=entry))
                    pd_str_list.append(entry.__str__())

            dpandas_completer.words += [x.__str__() for x in panda_list]

        # this should look for cols
        elif tl[0] == "show" or tl[0] == "ls" or tl[0] == "sh":
            count = 0
            try:
                if len(tl) >= 1 and (
                    tl[1:] == ["" for x in tl[1:]] or tl == [1]
                ):  # lol
                    print("\n".join([x.__str__() for x in panda_list]))
                    # print([x.__str__() for x in pd_str_list])
                elif tl[1] == "rows":
                    print("rows not implemented yet cause strings/numbers")

                elif tl[1] == "cols":
                    for i in tl[2:]:
                        for j in panda_list:
                            if i == j.__str__():
                                count += 1
                                # j.show_a_column()
                                selected = selector(
                                    j.cols, once=True, msg="a column to show"
                                )
                                j.show_a_column(selected)

                else:
                    for i in tl[1:]:
                        for j in panda_list:
                            if i == j.__str__():
                                count += 1
                                # starlen = 50 - len(str(count))
                                # print(f"{count}" + starlen * "*")
                                print(seperator)
                                j.show_me()
                                print(seperator)
            except:
                print("Something whent wrong, did you load first?")

        elif tl[0] == "cols":
            """
            just show the columns
            """
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        print("\n".join(j.get_wk_cols()))

        elif tl[0] == "trans":
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        j.transform()
                        print(j.working_frame)

        elif tl[0] == "reset":  #  and tl[1] in pd_str_list:
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        j.reset()

        elif tl[0] == "search":  #  and tl[1] in pd_str_list:
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        try:
                            count += 1
                            starlen = 50 - len(str(count))
                            print(f"{count}" + starlen * "*")
                            j.working_frame = j.search()
                            j.show_me()
                            print(50 * "*")
                        except AttributeError:
                            print("\033[91mYou may only search string data.\033[0m")

        elif tl[0] == "sel" or tl[0] == "select":
            count = 0
            try:
                if tl[1] == "rows":
                    print("rows not implemented yet because strings/numbers")

                elif tl[1] == "cols":
                    for i in tl[2:]:
                        for j in panda_list:
                            if i == j.__str__():
                                count += 1
                                j.select_cols(selector(j.cols, once=False))
            except IndexError:
                print("use select cols")

        elif tl[0] == "sort":  #  and tl[1] in pd_str_list:
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        # print(f"{count}" + (50 - len(str(count))) * "*")
                        j.sort(selector(j.cols, once=True))
                        print(seperator)
                        j.show_me()
                        print(seperator)

        elif tl[0] == "save":  #  and tl[1] in pd_str_list:
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1

                        ext = show_choices(
                            {"1": "csv", "2": "xlsx", "3": "json"},
                            once=True,
                            getvals=True,
                        )
                        print(f"you picked {ext}")
                        name_in = input(f"Save {i} output as *.{ext}: ")
                        file_name = name_in + "." + ext
                        drop_index = input("Drop index? Y/n ")

                        try:
                            # TODO put this functionality in dpandas
                            # i.e. j.save(fmt, drop_index: bool)
                            if "n" in drop_index or "N" in drop_index:
                                if ext == "xlsx":
                                    j.working_frame.to_excel(file_name)
                                if ext == "csv":
                                    j.working_frame.to_csv(file_name)
                                if ext == "json":
                                    j.working_frame.to_json(file_name)
                            else:
                                if ext == "xlsx":
                                    j.working_frame.to_excel(file_name, index=False)
                                if ext == "csv":
                                    j.working_frame.to_csv(file_name, index=False)
                                if ext == "json":
                                    j.working_frame.to_json(file_name)
                        except ModuleNotFoundError:
                            print("you don't have openpyxl installed")
                        except:
                            print(f"Nothing saved ext:{ext} file_name:{file_name}")

        elif tl[0] == "multi":
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        try:
                            j.make_mi(selector(j.cols, once=False))
                        except TypeError:
                            print("nothing happend?")

        elif tl[0] == "drop":
            count = 0
            try:
                if tl[1] == "rows":
                    for i in tl[2:]:
                        for j in panda_list:
                            if i == j.__str__():
                                count += 1
                                selected = selector(
                                    [str(x) for x in j.rows], once=False
                                )
                                usr_input = input(
                                    "Reset index? Y/n, careful if you don't have integer index: "
                                )
                                # TODO change this awful shit
                                try:
                                    j.drop_rows([int(x) for x in selected], usr_input)
                                except:
                                    j.drop_rows(selected, usr_input)

                elif tl[1] == "cols":
                    for i in tl[2:]:
                        for j in panda_list:
                            if i == j.__str__():
                                count += 1
                                selected = selector(j.cols, once=False)
                                j.drop_cols(selected)
            except IndexError:
                print("You must specify what to drop")

        elif tl[0] == "pop":
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        j.pop_cols()

        elif tl[0] == "pager" or tl[0] == "page":
            count = 0
            for i in tl[1:]:
                for j in panda_list:
                    if i == j.__str__():
                        count += 1
                        click.echo_via_pager(j.working_frame.to_string())

        elif tl[0] == "exit" or tl[0] == "quit" or tl[0] == "q":
            print("Goodbye!")
            running = False
            try:
                if DEBUG:
                    return panda_list
            except:
                break

        else:
            print(f"you said: {text} and nothing happend...\n")


if __name__ == "__main__":
    panda_list = cli()
    if DEBUG:
        try:
            a = [x for x in panda_list if x.__str__() == "animals.csv"][0]
        except IndexError:
            pass
