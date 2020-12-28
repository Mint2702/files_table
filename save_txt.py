from table_class import Table


def save(table: Table, name: str):
    f = open(f"{name}.txt", "w") 
    f.write(table.print_table())


# data_raw = {"column1": ["1", None, "three", 9], "column2": ["gool", "bench", 20, 12]}

# table = Table(data_raw)

# save(table, "text")
