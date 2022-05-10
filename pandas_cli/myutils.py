"""
Helpers
"""
import click

DEBUGGING = True

# ziplist
# returns tuples of keys and values
def zl(adict: dict):
    return zip(list(adict.keys()), list(adict.values()))


# def zd(y,getvals=False):
def zd(y, getvals=True):

    """
    zipdict
    makes a dictionary with string intgers to make click happy
    somtimes a list may get passed, we want everyone to be happy
    """

    int_dict = dict()

    if type(y) == list:
        for i, j in zip(range(len(y)), y):
            int_dict[str(i)] = j
        return int_dict

    elif type(y) == dict:
        if getvals:
            for i, j in zip(range(len(list(y.values()))), list(y.values())):
                int_dict[str(i)] = j
            return int_dict
        else:
            for i, j in zip(range(len(list(y.keys()))), list(y.keys())):
                int_dict[str(i)] = j
            return int_dict


OPTIONS = {"x": "exit", "s": "save"}


def show_choices(
    adict,
    once=False,
    msg="a key to examine",
    getvals=False,
    color1="yellow",
    color2="black",
    color3="blue",
    color4="black",
    color5="green",
    options=OPTIONS,
):

    if getvals:
        int_dict = zd(adict, getvals=True)
    else:
        int_dict = zd(adict)

    running = True
    sel_list = []

    click.clear()

    while running:

        # we pop out the values from int_dict so this triggers when
        # nothing is left to select
        if len(int_dict) == 0:
            click.secho("ALL DONE", fg=color1)
            running = False
            return sel_list

        for i, j in zl(int_dict):
            str_a = click.style(f"{i}", bg=color1, fg=color2)
            str_b = click.style(f":", blink=True)
            try:
                str_c = click.style(f"{j.name}", bg=color2, fg=color1)

            # maybe take out attr
            except AttributeError:
                str_c = click.style(f"{j}", bg=color2, fg=color1)
                if DEBUGGING:
                    pass
            finally:
                try:
                    click.echo(str_a + str_b + str_c)
                except UnboundLocalError:
                    click.echo(str_a + str_b + str_c)
        click.echo(
            click.style(f"You selected:", bg=color3, fg=color4)
            + click.style(f" {sel_list}", underline=True, bg=color4, fg=color3)
        )

        # for i,j in zl(options):
        #    print(f'{i}:{j}')
        click.secho("Menu Options", fg=color3, bg=color4)
        click.secho("\t".join([":".join([x, y]) for x, y in zl(options)]))

        usr_sel = input(f"Select {msg}: ")

        if usr_sel == "x" or usr_sel == "X":
            click.secho("Exiting", fg=color3, bg=color1)
            running = False
            return sel_list

        elif usr_sel == "s" or usr_sel == "S":
            print("saving choices")
            return sel_list

        try:
            sel = int_dict[usr_sel]
            click.clear()
            if once is True:
                return sel
            if type(adict) == list:
                sel_list.append(sel)
                del int_dict[usr_sel]
                if running == False:
                    return sel_list
            else:
                sel_list.append(sel)
                del int_dict[usr_sel]
                if running == False:
                    return sel_list

        except KeyError:
            click.clear()
            click.secho(
                f"Select a valid choice:{usr_sel} not valid",
                bg="bright_red",
                fg="black",
            )

