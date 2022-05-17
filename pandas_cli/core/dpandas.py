import pandas as pd

# from pandas_cli.myutils import BaseUtils
# TODO this should become unnecessary after refactor
from ..myutils import show_choices


class BasePanda:
    """
    This is the object for mainting the state during interaction.
    """

    def __init__(self, data=None, ftype=None, abs_path=None):

        self.abs_path = abs_path

        # FIXME File handling is really damn bad
        if abs_path is not None:
            try:
                data = self.abs_path.path
                self.ftype = self.abs_path.name.rsplit(".")[1]
            except IndexError as err:
                self.abs_path = None
                raise Exception(ValueError) from err
        else:
            self.ftype = ftype

        if self.ftype == "json":
            try:
                self.original_frame = pd.read_json(data)
            except:
                print("json data not loaded properly")

        elif self.ftype == "xlsx":
            try:
                self.original_frame = pd.read_excel(data)
            except:
                print("excel data not loaded properly")

        elif self.ftype == "csv":
            try:
                # should make index_col optional
                self.original_frame = pd.read_csv(data, index_col=0)
            except:
                print("csv data not loaded properly, try adjusting delimeters")

        else:
            self.original_frame = pd.DataFrame(data)

        self.working_frame = self.original_frame.copy()
        self.cols = self.get_wk_cols()
        self.rows = self.get_wk_rows()
        self.og_cols = self.original_frame.columns.to_list()
        self.multi_index = None

    def len(self):
        """Get length"""
        return len(self.working_frame)

    def reset(self):
        """
        reset the working frame to the original
        """
        self.working_frame = self.original_frame.copy()

    def get_wk_cols(self):
        """
        Get columns from the working frame
        """
        self.cols = self.working_frame.columns.to_list()
        # return self.working_frame.columns.to_list()
        return self.cols

    def get_wk_rows(self):
        """
        Get rows from the working frame as string
        """
        # self.rows = [str(x) for x in self.working_frame.index.to_list()]
        self.rows = self.working_frame.index.to_list()
        return self.rows

    def show_me(self):
        """
        Prints the working frame.
        """
        print(self.working_frame)

    def select_cols(self, selected: list):
        """
        Select coloumns. If not selected, a coloumn will be dropped from the frame.
        """
        self.working_frame = self.original_frame[selected]
        return self.working_frame[selected]

    def make_mi(self, selected: list):
        """
        Makes a multi-index.
        """
        for i in selected:
            print(self.working_frame[i].dtype)
        try:
            self.multi_index = pd.MultiIndex.from_frame(self.working_frame[selected])
        except TypeError:
            # Force to string
            self.multi_index = pd.MultiIndex.from_frame(
                self.working_frame[selected].astype(str)
            )
            # self.working_frame.index = self.multi_index
        except ValueError:
            print("Type not supported nothing changed")
        finally:
            self.working_frame.index = self.multi_index

    def sort(self, selected: list):
        """
        sort by a column
        """
        try:
            self.working_frame = self.working_frame.sort_values(selected)
        except:
            print("Something went wrong")

    # TODO move this out
    def sort_mi(self):
        selected = show_choices(
            list(self.multi_index.names),
            msg="Select item to sort multi_index",
            once=True,
        )
        print(f"len(selected)={len(selected)}")
        try:
            self.multi_index = self.multi_index.sort_values(selected)
        except:
            print("Something went wrong")

    # TODO move this out
    def swap_mi(self):
        """
        swap levels in multi-index
        """
        selected = show_choices(self.multi_index.names)
        if len(selected) == 2:
            try:
                return self.multi_index.swaplevels(selected[0], selected[1])
            except:
                print("swap_mi failed. only 2 cols please. needs multi_index")

    # TODO move this out
    def search(self):

        """This will search the values in a column for the string entered on the cli"""

        selected = show_choices(
            self.get_wk_cols(), msg="column to search on", once=True
        )
        print("What would you like to search for?")
        usr_str = input(f"{selected}: ")
        df_new = self.working_frame.copy()

        astr = "***Excluded from search***"

        try:
            df_new_notna = df_new.loc[df_new[selected].notna()]
            df_new_na = df_new.loc[df_new[selected].isna()]
            print(f"{astr}\n {df_new_na[selected]} ")
            print("**************************")
            df_new = df_new_notna.loc[df_new_notna[selected].str.contains(usr_str)]

        # ValueError: Cannot mask with non-boolean array containing NA / NaN values
        except ValueError:
            print("The data should be string. The handling of Nan's could be better")
        return df_new

    # TODO move this out
    def auto_search(self, term, col):
        """
        same as search but with data already supplied
        This was useful once, maybe not anymore
        """

        df_new = self.working_frame.copy()

        # df_new=df_new.loc[[x in y for y in df_new[selected]]]
        try:
            df_new_notna = df_new.loc[df_new[col].notna()]
            df_new_na = df_new.loc[df_new[col].isna()]
            df_new = df_new_notna.loc[df_new_notna[col].str.contains(term, regex=False)]
            if not df_new.empty:
                return df_new.reset_index(drop=True)
        except ValueError:
            print("The data could be better. The handling of Nan's could be better")

    def drop_rows(self, selected: list, usr_input):
        """
        Does this work?
        """
        """
        selected = show_choices(self.get_wk_rows(), msg="rows to drop", once=False)
        usr_input = input("Reset index? Y/n, careful if you don't have integer index")
        """
        self.working_frame.drop(selected, axis=0, inplace=True)
        # if "n" not in usr_input or "N" not in usr_input:
        if usr_input.count("y") > 0 or usr_input.count("Y"):
            self.working_frame.reset_index(drop=True, inplace=True)

    def drop_cols(self, selected):
        """
        Drop columns :)
        """
        self.working_frame.drop(selected, axis=1, inplace=True)

    # TODO move this out
    # TODO This had a specific use case with hence the default pat. make it general and apply to the panda
    def split(self, pat="\n\n"):
        """
        string to list
        """
        print("creates a new frame/series what now")
        selected = show_choices(self.get_wk_cols(), msg="column to split", once=True)
        split_list = self.working_frame[selected].str.split(pat=pat)
        return split_list

    # TODO move this out
    def explode(self):
        """
        this does nothing. should explode the dataframe
        """
        selected = show_choices(
            self.get_wk_cols(), msg='column to "Explode"', once=True
        )
        usr_input = input(f"{selected}: ")
        # B=self.working_frame.copy()

    # takes a row and makes it the column header
    # TODO move this out
    # TODO figure out how to represent this in the repl
    def pop_cols(self):
        selected = show_choices(
            self.get_wk_rows(), msg="row to replace columns", once=True
        )
        self.working_frame.columns = self.working_frame.iloc[selected].values
        self.show_me()

    def transform(self):
        """
        Returns Df.T
        """
        self.working_frame = self.working_frame.T

    # TODO move this out
    def show_a_column(self, selected):
        """
        Show a column without affecting the working frame
        """
        print(self.working_frame[selected])

    def __str__(self):
        try:
            return str(self.abs_path.name)
        except:
            return "File name not found?"
