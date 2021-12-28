import pandas as pd
import numpy as np


class Stock:

    def __init__(self):
        self.list_orders = []
        self.preponderance = ''
        self.volume = 0

    def append_orders(self, list_orders):
        for order in list_orders:
            self.list_orders.append(order)

    def funk(self, order: pd.Series, raz, price):
        if (order['type'] == 'sell') & (order['price'] < price):
            return order['value']
        elif (order['type'] == 'buy') & (order['price'] > price):
            return order['value']
        elif (order['price'] == price) & (self.volume != 0):
            if (((self.preponderance == 'sell') & (order['type'] == 'sell')) | (((self.preponderance == 'buy') & (order['type'] == 'buy')))):
                if self.volume >= order['value']:
                    self.volume -= order['value']
                    return order['value']
                else:
                    s = self.volume
                    self.volume == 0
                    return s
            else:
                return order['value']

        else:
            return 0

    def orders(self):
        orders_pd = pd.DataFrame(self.list_orders)
        products = orders_pd['product'].unique()
        for product in products:
            product_sell = orders_pd[(orders_pd['product'] == product) &
                                     (orders_pd['type'] == 'sell')]
            product_buy = orders_pd[(orders_pd['product'] == product) &
                                    (orders_pd['type'] == 'buy')]
            product_sell.sort_values(by=['price', 'value'], ascending=[True, False], inplace=True)
            product_buy.sort_values(by=['price', 'value'], ascending=[False, True], inplace=True)
            product_sell['cumsum_sell'] = product_sell['value'].cumsum()
            product_buy['cumsum_buy'] = product_buy['value'].cumsum()
            f = pd.concat([product_sell, product_buy]).sort_values(by=['price', 'cumsum_sell', 'cumsum_buy'],
                                                                   ascending=[True, True, False])
            f['cumsum_sell'].fillna(method='ffill', inplace=True)
            f['cumsum_sell'].fillna(0, inplace=True)
            f['cumsum_buy'].fillna(method='bfill', inplace=True)
            f['cumsum_buy'].fillna(0, inplace=True)

            f['max'] = f[['cumsum_sell', 'cumsum_buy']].min(axis=1)
            f['minraz'] = abs(f['cumsum_sell'] - f['cumsum_buy'])
            max_trade = f['max'].max()
            min_raz = f[f['max'] == max_trade]['minraz'].min()
            ffff = f[(f['max'] == max_trade) & (f['minraz'] == min_raz)]
            price = ffff.iloc[0]['price']
            if ffff.iloc[0]['cumsum_sell'] < ffff.iloc[0]['cumsum_buy']:
                self.preponderance = 'buy'
                self.volume = ffff.iloc[0]['cumsum_sell']
            else:
                self.preponderance = 'sell'
                self.volume = ffff.iloc[0]['cumsum_buy']


            f['trade'] = f.apply(self.funk, args=(min_raz, price), axis=1)
            print(f)

            print('max:', max_trade, 'min_rax:', min_raz, 'price:', price)
