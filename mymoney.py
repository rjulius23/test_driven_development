#!/usr/bin/env python3.5
import argparse
import codecs
import csv
from locale import setlocale, atof, LC_ALL
from mydataprovider import DataProvider, CSVDataProvider


def parse_commandline():
    usage = ("Usage: \n"
             "./{script} [--csv] -P|--path <path to report file> ")
    parser = argparse.ArgumentParser(
            usage=usage,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="CLI Tool to parse monthly financial reports.\n")
    parser.add_argument('-P', "--path", dest='path',
                        help=argparse.SUPPRESS, required=True)
    parser.add_argument("--csv", dest='csv', action='store_true',
                        help=argparse.SUPPRESS)
    args_ret = parser.parse_args()
    return args_ret


class MyMoney(object):

    def __init__(self, **kwargs):
        self.provider = kwargs.get("provider", DataProvider())

    def calc_expense(self):
        pass

    def get_total_expenses(self):
        setlocale(LC_ALL, 'hu_HU.UTF8')
        result = {
            "total_expenses": 0,
            "total_earnings": 0,
        }
        for expense in self.provider.get_transactions():
            money_amount = atof(expense.get_dict()["amount"])
            if money_amount < 0:
                result["total_expenses"] += money_amount
            else:
                result["total_earnings"] += money_amount

        return result

    def print_results(self):
        summary = self.get_total_expenses()
        print("Total money spent: %f\nTotal money earned: %f\nEnd of month balance: %f"
              % (summary["total_expenses"], summary["total_earnings"],
                 (summary["total_expenses"] + summary["total_earnings"])))

if __name__ == '__main__':
    args = parse_commandline()
    if args.path and args.csv:
        provider = CSVDataProvider(path=args.path)
        money = MyMoney(provider=provider)
        money.print_results()
    else:
        print("Only supports CSV format for report files at the moment!")
        exit(1)
