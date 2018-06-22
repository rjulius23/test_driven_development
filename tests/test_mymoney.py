from mymoney import MyMoney
from unittest import TestCase
from mydataprovider import DataProvider, CSVDataProvider


class TestMyMoney(TestCase):

    def test_parse_line(self):
        print(self.test_parse_line.__name__)
        provider = CSVDataProvider()
        transcation_line = [
                                '1234',
                                'HUF',
                                '20180503',
                                'Kártyatranzakció',
                                '+CMS CLT-1819078489',
                                '          -990,00',
                                'Vásárlás(2018.05.01) Card:123123123  ',
                                'GBR-g.co/helppay# GOOGLE *Google Play Ap 990,00 HUF',
                                '0000000123123123'
                            ]
        result = provider._parse_line(transcation_line)
        self.assertNotEqual(result, {}, "Failure, empty result!")

    def test_cant_parse_line(self):
        print(self.test_cant_parse_line.__name__)
        provider = CSVDataProvider()
        transaction_line = ''
        self.assertRaises(Exception, provider._parse_line, transaction_line)

    def test_empty_report_path(self):
        print(self.test_empty_report_path.__name__)
        provider = CSVDataProvider()
        self.assertRaises(FileNotFoundError, provider.get_transactions)

    def test_get_transactions_csv(self):
        print(self.test_get_transactions_csv.__name__)
        money = CSVDataProvider(path="/home/egyuhal/PycharmProjects/MyMny/test_report.csv")
        self.assertTrue(len(money.get_transactions()) > 1)

    def test_get_expenses_csv(self):
        print(self.test_get_expenses_csv.__name__)
        provider = CSVDataProvider(path="/home/egyuhal/PycharmProjects/MyMny/test_report.csv")
        money = MyMoney(provider=provider)
        expenses = money.get_total_expenses()
        self.assertTrue(expenses["total_expenses"] != 0)
        self.assertTrue(expenses["total_earnings"] != 0)
