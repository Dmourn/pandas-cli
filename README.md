# pandas-cli

A command line interface for manipulating dataframes in python pandas.



## Visuals
![] (images/out.gif)

## Installation

still a WIP.
```
pip install -e . 
```

## Usage

You must have a directory named data in your current directory. I'll fix it soon.

The program will attempt to load excel, csv, or json files (by extension) in the data dir.

You can save the 'working frame' of a file as those formats as well.


```
pandas-cli 

OR 

cd pandas_cli && python -im simple  

```

The second option above allows you to access the list pl with all the 'dpandas' objects loaded.

Once the cli is open.

```
load

show

show file.csv

drop cols file.csv

sort file.csv

reset file.csv

save file.csv

```
There is tab completion for everything, but no semantics..yet.

## Project status
WIP

I used the core of this for look at string data only. So many features are lacking 
I would like to add (i.e. Re-typing ints and float, calculations)

File handling isn't great. Couldn't figure out if I want to use click or not.
I think I will just use argparse, but for now it is a dependency.

Right now, everything is assummed to be a string.
This creates some odd behavior when comparing input to values.

```
search file.csv
```

Will crash if you search on an numeric column.

