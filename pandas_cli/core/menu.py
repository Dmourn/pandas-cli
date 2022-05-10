import click
from pandasclick.myutils import zd, show_choices
from pandasclick.dpandas import BasePanda

# TODO figure out what you wanted to do here :)
# TODO write better comments
# gets obj dicts with keys:
# datadir', 'ftype', 'abs_path_selected', 'pandas_objs'

# menu options
MENU_OPTIONS = {
    "f": "file select",
    "c": "column selection",
    "m": "make MultiIndex",
    "r": "reset",
    "x": "exit",
    "s": "save",
}


def main_menu(obj):
    # lol
    show_choices(obj["pandas_objs"], msg="what you want to do", options=MENU_OPTIONS)
