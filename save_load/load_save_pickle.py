import pickle
import copy

from ..table_class import Table


def load_table(*args, types=False) -> dict:
    """
    Read name.pickle file or files
    """

    if not args:
        print("Please enter file names")
        return False

    names = []
    for name in args:
        names.append(name)

    try:
        data_new = []
        count = -1
        for name in names:
            count += 1
            with open(f"{name}.pickle", "rb") as f:
                if count == 0:
                    data = pickle.load(f)
                    data_new = Table(data)
                    headers = copy.deepcopy(data[0])
                else:
                    data = pickle.load(f)
                    if headers != data[0]:
                        print("Wrong format")
                        return False
                    count1 = 0
                    for item in data:
                        if count1 > 0:
                            data_new.data.append(item)
                        count1 += 1

        return data_new
    except Exception:
        print("Files not found")


def save_table(table: Table, name: str, max_rows=None):
    """
    Write data to pickle files with specified name
    """

    length = len(table.data)
    headers = table.headers

    if max_rows is None or length / max_rows <= 1:
        with open(f"{name}.pickle", "wb") as f:
            full_data = []
            full_data.append(headers)
            for element in table.data:
                full_data.append(element)
            pickle.dump(full_data, f)
            return True

    if length % max_rows == 0:
        num_files = length // max_rows
    else:
        num_files = length // max_rows + 1
    count = 1
    names = [name]
    while count < num_files:
        new_name = f"{name}_{count}"
        names.append(new_name)
        count += 1

    count = 0
    data_splited = []
    while count < num_files:
        splited_list = table.data[count * max_rows : (count + 1) * max_rows]
        data_splited.append(splited_list)
        count += 1

    for i in range(len(names)):
        with open(f"{names[i]}.pickle", "wb") as f:
            out_data = []
            out_data.append(headers)
            for item in data_splited[i]:
                out_data.append(item)
            pickle.dump(out_data, f)
    return True


"""
data_raw = {"column1": ["1", 2, "three", 4.1], "column2": ["gool", "bench", 20, 12]}
table = Table(data_raw)
save_table(table, "table", max_rows=2)
table1 = load_table("table", "table_1")
print(table1.data)
"""
