import copy
from datetime import *

from table_class import Table


def concat(table1: Table, table2: Table) -> Table:
    """
    Concatination of two tables with the same headers
    """

    if table1.headers == table2.headers:
        data = copy.deepcopy(table1.data)
        for i in table2.data:
            data.append(i)
        data.insert(0, copy.deepcopy(table1.headers))
        new_table = Table(data)
        return new_table
    else:
        print("Different columns in tables")
        return False


data_raw = {
    "column1": ["1", date(2005, 1, 12), "three", 9, "1"],
    "column2": ["gool", "bench", 20, 12, None],
}

table1 = Table(data_raw)

data_raw2 = {
    "column1": ["uno", 89],
    "column2": [90, 80],
}

table2 = Table(data_raw2)

print(concat(table1, table2).data)