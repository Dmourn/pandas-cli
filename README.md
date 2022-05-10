# pandas-cli

A command line interface for manipulating dataframes in python pandas.



## Visuals
![](images/out.gif)

## Installation

still a WIP.
```
pip install . 
```

## Usage

You must have a directory named data in your current directory. I'll fix it soon.

The program will attempt to load excel, csv, or json files (by extension) in the data dir.

You can save the 'working frame' of a file as those formats as well.


```
pandas-cli 
```
Or interact with the objects from dpandas.py

```
python -i pandas_cli/main.py  

```
This allows you to access the list `pandas_list` with `a` being the object created by data/animals.csv.

Once the cli is open. The first command must be `load` which loads the files in ./data (this should change)

The syntax is as follows `verb [cols,rows] file.ext` with ext being the extension.

For example:
`drop cols file.csv`

**Try using the tab completion :)**

List of verbs (some are inactive or aliases for other verbs)
```
exit
quit
load
trans
show
cols
split
select
ls
search
reset
save
sort
multi
rows
drop
chcols
pop
```


## Project status
WIP

I used the core of this for look at string data only. So many features are lacking 
I would like to add (i.e. Re-typing ints and float, calculations)

File handling isn't great.

Some functions assume the data are strings.
This creates some odd behavior when comparing input to values.

```
search file.csv
```
Will crash if you search on an numeric column.

