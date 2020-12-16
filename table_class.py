from typing import List, Dict
import typing


class Table:
    def __init__(self, data: List[dict] or Dict[str, list] or List[list]):
        if type(data) is dict:
            self.data = self.from_dict_to_list_lists(data)
        elif type(data[0]) is dict:
            try:
                self.data = self.from_list_dicts_to_list_lists(data)
            except Exception:
                print("Wrong formar")
                return None
        elif type(data[0]) is list:
            self.data = data
        else:
            print("Wrong formar")
            return None

    def from_list_dicts_to_list_lists(self, data: List[dict]) -> List[list]:
        if self.check_headers(data) is False:
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
                    dict_to_list.append('')
            new_data.append(dict_to_list)
        return new_data

    def check_headers(data: List[dict]) -> bool:
        oldheaders = list(data[0].keys())
        for line in data:
            headers = list(data.keys())
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



data_raw = {"column1":["1",2,"three",4.1],"column2":["gool","bench",12]}

table = Table(data_raw)

print(table.data)