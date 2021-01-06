import csv
import copy

from ..table_class import Table


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


def save_table(table: Table, base_name: str, max_rows=None):
    """
    Write data to a CSV file with specified name
    """

    headers = table.headers
    length_of_table = len(table.data)

    if max_rows is None or length_of_table / max_rows <= 1:
        with open(f"{base_name}.csv", "w") as out_file:
            writer = csv.writer(out_file)
            writer.writerow(headers)
            for line in table.data:
                writer.writerow(line)
            return True

    if length_of_table % max_rows == 0:
        num_files = length_of_table // max_rows
    else:
        num_files = length_of_table // max_rows + 1

    count = 1
    names = [base_name]
    while count < num_files:
        new_name = f"{base_name}_{count}"
        names.append(new_name)
        count += 1

    count = 0
    data_splited = []
    while count < num_files:
        splited_list = table.data[count * max_rows : (count + 1) * max_rows]
        data_splited.append(splited_list)
        count += 1

    for i in range(len(names)):
        with open(f"{names[i]}.csv", "w") as out_file:
            writer = csv.writer(out_file)
            writer.writerow(headers)
            for item in data_splited[i]:
                writer.writerow(item)
    return True


table = load_table("table", "table2")
save_table(table, "save", max_rows=2)
