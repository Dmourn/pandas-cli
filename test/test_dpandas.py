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

import os
# more of a reference than anything else
def test_csv():
    file_list = list(os.scandir('./data'))
    target_file = [x for x in file_list if x.name == 'animals.csv'][0]
    csv_panda = dpandas.BasePanda(abs_path=target_file)

    csv_str_test = csv_panda.working_frame.to_csv()

    assert csv_str == csv_str_test

# TODO make excel test for multi. excel files are annoying

# TODO more tests
