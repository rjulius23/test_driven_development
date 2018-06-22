from abc import abstractmethod
import codecs
import csv


class DataProvider():
    def __init__(self):
        self.transactions = []  # type: List[Transaction]

    @abstractmethod
    def get_transactions(self):
        pass


class Transaction():
    def __init__(self):
        self.attributes = {
            'own_account': None,
            'currency': None,
            'date': None,
            'type': None,
            'from': None,
            'from_account': None,
            'amount': None,
            'details': None,
            'id': None
        }

    def set_item(self, key, value):
        if key in self.attributes.keys():
            self.attributes[key] = value
        else:
            raise Exception("Wrong key [%s] not in %s !" % (key, self.attributes.keys()))

    def get_dict(self):
        return self.attributes


class CSVDataProvider(DataProvider):
    def __init__(self, **kwargs):
        super().__init__()
        self.report_path = kwargs.get("path", "")

    def get_transactions(self):
        if self.transactions is not []:
            with codecs.open(self.report_path, 'r', encoding='latin-1') as report:
                count = 0
                # Skip the first line as those are the columns, and
                # are not required
                for line in csv.reader(report, delimiter=";"):
                    if count == 0:
                        count += 1
                        continue
                    else:
                        self.transactions.append(self._parse_line(line))
                        count += 1

        return self.transactions

    @staticmethod
    def _parse_line(transaction):
        result = Transaction()
        items = [elem.strip() for elem in transaction]
        if len(items) == 9:
            # Assuming the order of the keys is matching the order
            # of the items only true for the Unicredit CSV
            keys = [
                "own_account",
                "currency",
                "date",
                "type",
                "from",
                "from_account",
                "amount",
                "details",
                "id"
            ]
            for key, val in zip(keys, items):
                # For DEBUG print("Key: %s, Val: %s" % (key, val))
                result.set_item(key, val)

        else:
            raise Exception("Could not find any data in transaction line!")
        return result

