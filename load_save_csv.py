import csv
import copy

from table_class import Table


def load_table(*args, types=False) -> Table:
    """
    Read name.csv file or multiple files
    """

    if not args:
        print("Please enter file names")
        return False

    names = []
    for name in args:
        names.append(name)

    try:
        count = 0
        table_list = []
        for name in names:
            count += 1
            with open(f"{name}.csv") as csvfile:
                reader = csv.reader(csvfile, delimiter=",")
                headers = next(reader)
                if count == 1:
                    global_headers = copy.deepcopy(headers)
                    length = len(global_headers)
                    table_list.append(global_headers)
                else:
                    if headers != global_headers:
                        print("Wrong csv files")
                        return False
                for line in reader:
                    table_line = []
                    for i in range(length):
                        try:
                            if line[i]:
                                table_line.append(line[i])
                            else:
                                table_line.append(None)
                        except Exception:
                            table_line.append(None)
                    table_list.append(table_line)
            count += 1
        table = Table(table_list)
        return table
    except Exception:
        print("Files not found")
        return False


table = load_table("table", "table2")
print(table.data)
print(table.headers)
