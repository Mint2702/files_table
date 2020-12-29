from typing import List, Dict, Any, Optional
from tabulate import tabulate
from datetime import *
import copy


class Table:
    __slots__ = ("data", "headers", "types")

    def __init__(self, data: List[dict] or Dict[str, list] or List[list]):
        """
        Initiates slots of 'data', 'headers' and 'types'
        """

        if self.check_type(data) == "dict":
            self.headers = list(data.keys())
            self.data = self.from_dict_to_list_lists(data)
            self.types = self.get_column_types()
        elif self.check_type(data) == "list of dicts":
            try:
                self.headers = list(data[0].keys())
                self.data = self.from_list_dicts_to_list_lists(data)
                self.types = self.get_column_types()
            except Exception:
                print("Wrong format")
                return None
        elif self.check_type(data) == "list of lists":
            self.headers = data[0]
            self.data = data[1:]
            self.types = self.get_column_types()
        else:
            print("Wrong format")
            return None

    def from_list_dicts_to_list_lists(self, data: List[dict]) -> List[list]:
        """
        Rewrites information from a list of dicts to a list of lists
        """

        if self.check_headers_dict(data) is False:
            print("Wrong format")
            return False
        new_data = []
        headers = list(data[0].keys())
        for line in data:
            dict_to_list = []
            for header in headers:
                dict_to_list.append(line[header])
            new_data.append(dict_to_list)
        return new_data

    def from_dict_to_list_lists(self, data: Dict[str, list]) -> List[list]:
        """
        Rewrites information from a dict to a list of lists
        """

        new_data = []
        headers = list(data.keys())
        max_len = self.max_length(data)

        for i in range(max_len):
            dict_to_list = []
            for header in headers:
                try:
                    dict_to_list.append(data[header][i])
                except Exception:
                    dict_to_list.append("")
            new_data.append(dict_to_list)
        return new_data

    def check_headers_dict(self, data: List[dict]) -> bool:
        """
        Checks if the headers in all dicts in the list of input are the same
        """

        oldheaders = list(data[0].keys())
        for line in data:
            headers = list(line.keys())
            if headers != oldheaders:
                return False
        return True

    def max_length(self, data: Dict[str, list]) -> int:
        """
        Returns the maximum length of the table if the input is dictionary
        """

        headers = list(data.keys())
        leng = len(data[headers[0]])
        for header in headers:
            if len(data[header]) > leng:
                leng = len(header)
        return leng

    def check_type(self, data: Any) -> str:
        """
        Specifies type of the input for __init__
        """

        if type(data) is dict:
            headers = list(data.keys())
            for header in headers:
                if type(data[header]) is not list:
                    print("Wrong dictionary input")
                    return False
            return "dict"
        elif type(data) is list:
            if type(data[0]) is dict:
                for element in data:
                    if type(element) is not dict or self.check_headers_dict is False:
                        print("Wrong list of dictionaries")
                        return False
                return "list of dicts"
            elif type(data[0]) is list:
                for element in data:
                    if type(element) is not list:
                        print("Wrong list of dictionaries")
                        return False
                return "list of lists"
            else:
                print("Wrong list format")
                return False
        else:
            print("Wrong input format")
            return False

    def get_column_types(self, by_number: bool = True) -> dict:
        """
        Get types of columns from the table
        """

        types = {}
        for i in range(len(self.headers)):
            first_type = type(self.data[0][i]).__name__
            if by_number is True:
                header = i
            else:
                header = self.headers[i]
            for row in self.data:
                if type(row[i]).__name__ != first_type:
                    types[header] = "Multiple types"
                    break
                types[header] = first_type
        return types

    def set_column_types(self, types_dict: dict, by_number: bool = True):
        """
        Set types of columns from the table
        """

        for key in types_dict:
            for row in self.data:
                if by_number is True:
                    try:
                        if types_dict[key] == str:
                            row[key] = str(row[key])
                        elif types_dict[key] == int:
                            row[key] = int(row[key])
                        elif types_dict[key] == float:
                            row[key] = float(row[key])
                        elif types_dict[key] == bool:
                            row[key] = bool(row[key])
                        elif types_dict[key] == date:
                            row[key] = date(row[key])
                        else:
                            print("Unapropriate input")
                            break
                    except Exception:
                        print("Couldn't convert")
                        break
                else:
                    try:
                        count = self.headers.index(key)
                        if types_dict[key] == str:
                            row[count] = str(row[count])
                        elif types_dict[key] == int:
                            row[count] = int(row[count])
                        elif types_dict[key] == float:
                            row[count] = float(row[count])
                        elif types_dict[key] == bool:
                            row[count] = bool(row[count])
                        elif types_dict[key] == date:
                            row[count] = date(row[count])
                        else:
                            print("Unapropriate input")
                            break
                    except Exception:
                        print("Couldn't convert")
                        break

    def print_table(self):
        """
        Print data from the table
        """

        return tabulate(self.data, headers=self.headers)

    def get_rows_by_number(
        self, start: int, stop: Optional[int] = None, copy_table: bool = False
    ):
        """
        Returns row/rows specified by its number
        """

        start -= 1
        if stop is None:
            stop = start + 1
        if start > stop or stop <= 0 or start <= 0:
            print(
                "Please check you 'start' and 'stop' arguements - start should be less than stop"
            )
            return False
        if copy_table:
            if start >= len(self.data) or stop > len(self.data):
                print("Wrong interval")
                return False

            rows = [copy.deepcopy(self.data[i]) for i in range(start, stop)]
            rows.insert(0, copy.deepcopy(self.headers))
            new_table = Table(rows)
            return new_table
        else:
            if start >= len(self.data) or stop > len(self.data):
                print("Wrong interval")
                return False

            rows = [self.data[i] for i in range(start, stop)]
            rows.insert(0, copy.deepcopy(self.headers))
            new_table = Table(rows)
            return new_table

    def get_rows_by_index(self, *args, copy_table: bool = False):
        """
        Returns row/rows specified by its value from the first column
        """

        if not args:
            print("Please enter some values")
            return False

        values = [value for value in args]

        if copy_table:
            table = []
            for value in values:
                for row in self.data:
                    if row[0] == value:
                        table.append(copy.deepcopy(row))
            table.insert(0, copy.deepcopy(self.headers))
            new_table = Table(table)
            return new_table
        else:
            table = []
            for value in values:
                for row in self.data:
                    if row[0] == value:
                        table.append(row)
            table.insert(0, copy.deepcopy(self.headers))
            new_table = Table(table)
            return new_table

    def get_values(self, column: int or str = 0) -> list:
        """
        Returns a list of data in the specified column
        """

        try:
            if type(column) == int:
                column_data = [copy.deepcopy(row[column]) for row in self.data]
                return column_data
            else:
                column_index = self.headers.index(column)
                column_data = [copy.deepcopy(row[column_index]) for row in self.data]
                return column_data
        except Exception:
            print("Wrong input. Column not found")

    def get_value(self, column: int or str = 0) -> str or int or float or date:
        """
        Returns data in the specified column
        """

        try:
            if type(column) == int:
                column_data = copy.deepcopy(self.data[0][column])
                return column_data
            else:
                column_index = self.headers.index(column)
                column_data = copy.deepcopy(self.data[0][column_index])
                return column_data
        except Exception:
            print("Wrong input. Column not found")

    def set_values(self, values: list, column: int or str = 0):
        """
        Sets a list of data in the specified column
        """

        try:
            if type(column) == int:
                count = 0
                for row in self.data:
                    row[column] = values[count]
                    count += 1
            else:
                count = 0
                for row in self.data:
                    row[self.headers.index(column)] = values[count]
                    count += 1
        except Exception:
            print("Wrong input. Column not found")

    def set_value(self, value: str or int or float or date, column: int or str = 0):
        """
        Sets a list of data in the specified column
        """

        try:
            if type(column) == int:
                self.data[0][column] = value
            else:
                self.data[0][self.headers.index(column)] = value
        except Exception:
            print("Wrong input. Column not found")


data_raw = {
    "column1": ["1", date(2005, 1, 12), "three", 9, "1"],
    "column2": ["gool", "bench", 20, 12, None],
}

table = Table(data_raw)
val = [1, 2, 3, 4, "5"]
table.set_value(69)
print(table.print_table())
