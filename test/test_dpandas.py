import os

import pytest
import pandas as pd

from pandas_cli import myutils
from pandas_cli.core import dpandas

# TODO instead of testing like a brute, try making a csv fuzzer

csv_str = """,Animal,Color,Count
0,penguin,red,13
1,penguin,blue,5
2,penguin,green,17
3,penguin,white,12
4,panda,red,6
5,panda,blue,12
6,panda,green,14
7,panda,white,19
8,fish,red,16
9,fish,blue,7
10,fish,green,13
11,fish,white,10
12,bear,red,17
13,bear,blue,10
14,bear,green,19
15,bear,white,6
"""

csv_two_cols_str = """,Animal,Color
0,penguin,red
1,penguin,blue
2,penguin,green
3,penguin,white
4,panda,red
5,panda,blue
6,panda,green
7,panda,white
8,fish,red
9,fish,blue
10,fish,green
11,fish,white
12,bear,red
13,bear,blue
14,bear,green
15,bear,white
"""

csv_dropped_cols_str = """,Color
0,red
1,blue
2,green
3,white
4,red
5,blue
6,green
7,white
8,red
9,blue
10,green
11,white
12,red
13,blue
14,green
15,white
"""

csv_dropped_rows_no_str = """,Animal,Color,Count
0,penguin,red,13
1,penguin,blue,5
2,penguin,green,17
3,penguin,white,12
4,panda,red,6
5,panda,blue,12
6,panda,green,14
7,panda,white,19
8,fish,red,16
9,fish,blue,7
12,bear,red,17
13,bear,blue,10
14,bear,green,19
15,bear,white,6
"""

csv_dropped_rows_yes_str = """,Animal,Color,Count
0,penguin,red,13
1,penguin,blue,5
2,penguin,green,17
3,penguin,white,12
4,panda,red,6
5,panda,blue,12
6,panda,green,14
7,panda,white,19
8,fish,red,16
9,fish,blue,7
10,bear,red,17
11,bear,blue,10
12,bear,green,19
13,bear,white,6
"""

csv_multi_index_str = """Animal,Color,Animal,Color,Count
penguin,red,penguin,red,13
penguin,blue,penguin,blue,5
penguin,green,penguin,green,17
penguin,white,penguin,white,12
panda,red,panda,red,6
panda,blue,panda,blue,12
panda,green,panda,green,14
panda,white,panda,white,19
fish,red,fish,red,16
fish,blue,fish,blue,7
fish,green,fish,green,13
fish,white,fish,white,10
bear,red,bear,red,17
bear,blue,bear,blue,10
bear,green,bear,green,19
bear,white,bear,white,6
"""


@pytest.fixture
def csv_panda():
    file_list = list(os.scandir("./data"))
    target_file = [x for x in file_list if x.name == "animals.csv"][0]
    return dpandas.BasePanda(abs_path=target_file)


def load_animals_csv():
    file_list = list(os.scandir("./data"))
    target_file = [x for x in file_list if x.name == "animals.csv"][0]
    return dpandas.BasePanda(abs_path=target_file), target_file


def test_bad_file():
    file_list = list(os.scandir("./data"))
    try:
        target_file = [x for x in file_list if x.name == "bad-file"][0]
    except IndexError:
        print("bad-file not found")
    with pytest.raises(Exception):
        dpandas.BasePanda(abs_path=target_file)


# more of a reference than anything else
def test_csv_null(csv_panda):
    # csv_panda, target_file = load_animals_csv()
    csv_str_test = csv_panda.working_frame.to_csv()
    assert csv_str == csv_str_test


def test_csv_two_columns(csv_panda):

    # TODO you wanted to test against pandas itself...
    csv_panda, target_file = load_animals_csv()

    selected = ["Animal", "Color"]

    # simulate pressing '0' and '1'
    col_dict = myutils.zd(csv_panda.cols)
    test_selected = []
    test_selected.append(col_dict["0"])
    test_selected.append(col_dict["1"])
    assert selected == test_selected

    csv_panda.select_cols(selected)

    pandas_test_frame = pd.read_csv(target_file, index_col=0)[selected]
    csv_frame = csv_panda.working_frame

    assert csv_frame.to_string() == pandas_test_frame.to_string()
    assert csv_panda.working_frame.to_csv() == csv_two_cols_str


def test_drop_col(csv_panda):
    selected = ["Animal", "Count"]
    csv_panda.drop_cols(selected)
    assert csv_panda.working_frame.to_csv() == csv_dropped_cols_str


def test_drop_row(csv_panda):
    selected = [10, 11]
    csv_panda.working_frame.drop(selected, axis=0, inplace=True)

    assert csv_panda.working_frame.to_csv() == csv_dropped_rows_no_str


def test_drop_row_no_reset(csv_panda):
    selected = [10, 11]
    csv_panda.drop_rows(selected, "n")
    assert csv_panda.working_frame.to_csv() == csv_dropped_rows_no_str


def test_drop_row_yes_reset(csv_panda):
    selected = [10, 11]
    csv_panda.drop_rows(selected, "y")
    assert csv_panda.working_frame.to_csv() == csv_dropped_rows_yes_str


def test_make_multi(csv_panda):
    # csv_panda, target_file = load_animals_csv()
    selected = ["Animal", "Color"]
    csv_panda.make_mi(selected)
    assert csv_panda.working_frame.to_csv() == csv_multi_index_str


# TODO make tests: multi, excel, swap cols,
