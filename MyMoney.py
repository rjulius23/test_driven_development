#!/usr/bin/env python3.5
import argparse
import codecs
import csv
from locale import setlocale, atof, LC_ALL


def parse_commandline():
    usage = ("Usage: \n"
             "./{script} -P|--path <path to report csv> ")
    parser = argparse.ArgumentParser(
            usage=usage,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="CLI Tool to parse monthly financial reports.\n")
    parser.add_argument('-P', "--path", dest='path',
                        help=argparse.SUPPRESS, required=True)
    args_ret = parser.parse_args()
    return args_ret


class MyMoney(object):

    def __init__(self, **kwargs):
        self.transactions = []
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
                        self.transactions.append(self.parse_line(line))
                        count += 1

        return self.transactions

    @staticmethod
    def parse_line(transaction):
        result = {}
        items = [elem.strip() for elem in transaction]
        if len(items) == 9:
            result = {
                'acc_num': items[0],
                'currency': items[1],
                'date': items[2],
                'tr_type': items[3],
                'other_participant': items[4],
                'other_acc': items[5],
                'value': items[6],
                'note': items[7].split(),
                'unique_id': items[8]
            }
        else:
            raise Exception("Could not find any data in transaction line!")
        return result

    def calc_expense(self):
        pass

    def get_total_expenses(self):
        setlocale(LC_ALL, 'hu_HU.UTF8')
        result = {
            "total_expenses": 0,
            "total_earnings": 0,
        }
        for expense in self.get_transactions():
            money_value = atof(expense["value"])
            if money_value < 0:
                result["total_expenses"] += money_value
            else:
                result["total_earnings"] += money_value

        return result

    def print_results(self):
        summary = self.get_total_expenses()
        print("Total money spent: %f\nTotal money earned: %f\nEnd of month balance: %f"
              % (summary["total_expenses"], summary["total_earnings"],
                 (summary["total_expenses"] + summary["total_earnings"])))

if __name__ == '__main__':
    args = parse_commandline()
    if args.path:
        money = MyMoney(path=args.path)
        money.print_results()
