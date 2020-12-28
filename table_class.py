from typing import List, Dict, Any


class Table:
    __slots__ = ("data", "headers")

    def __init__(self, data: List[dict] or Dict[str, list] or List[list]):
        if self.check_type(data) == "dict":
            self.headers = list(data.keys())
            self.data = self.from_dict_to_list_lists(data)
        elif self.check_type(data) == "list of dicts":
            try:
                self.headers = list(data[0].keys())
                self.data = self.from_list_dicts_to_list_lists(data)
            except Exception:
                print("Wrong format")
                return None
        elif self.check_type(data) == "list of lists":
            self.headers = data[0]
            self.data = data[1:]
        else:
            print("Wrong format")
            return None

    def from_list_dicts_to_list_lists(self, data: List[dict]) -> List[list]:
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
        oldheaders = list(data[0].keys())
        for line in data:
            headers = list(line.keys())
            if headers != oldheaders:
                return False
        return True

    def max_length(self, data: Dict[str, list]) -> int:
        headers = list(data.keys())
        leng = len(data[headers[0]])
        for header in headers:
            if len(data[header]) > leng:
                leng = len(header)
        return leng

    def check_type(self, data: Any) -> str:
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

        def get_column_types(self):
            pass


data_raw = {"column1": ["1", 2, "three", 4.1], "column2": ["gool", "bench", 20, 12]}

table = Table(data_raw)

# print(table.data)
