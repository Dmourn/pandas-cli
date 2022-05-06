import os
import pandas as pd

from pandas_cli import myutils
from pandas_cli.core import dpandas

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


# more of a reference than anything else
def test_csv_null():
    file_list = list(os.scandir("./data"))
    target_file = [x for x in file_list if x.name == "animals.csv"][0]
    csv_panda = dpandas.BasePanda(abs_path=target_file)

    csv_str_test = csv_panda.working_frame.to_csv()

    assert csv_str == csv_str_test


def test_csv_two_columns():
    target_file = [x for x in list(os.scandir("./data")) if x.name == "animals.csv"][0]
    csv_panda = dpandas.BasePanda(abs_path=target_file)

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


# TODO make tests: multi, excel, swap cols,
