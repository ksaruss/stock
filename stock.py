import pandas as pd
import numpy as np


class Stock:

    def __init__(self):
        self.list_orders = []

    def append_orders(self, list_orders):
        for order in list_orders:
            self.list_orders.append(order)

    def funk(self, order, raz, price):
        if order['type'] == 'buy':
            if order['price'] > price:
                return order['value']
        elif order['type'] == 'sell' and order['price'] < price:
            return order['value']
        elif order['price'] == price and order['minraz'] == raz:

            return order['value'] - raz
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
            product_buy.sort_values(by=['price', 'value'], ascending=False, inplace=True)
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
            try:
                price = float(f[(f['max'] == max_trade) & (f['minraz'] == min_raz)]['price'])
            except:
                print(float(f[(f['max'] == max_trade) & (f['minraz'] == min_raz)]['price']))
                price = float(f[(f['max'] == max_trade) & (f['minraz'] == min_raz)]['price'][0])


            print(f.groupby(by='price').agg({'value': 'sum',
                                             'cumsum_sell': 'max',
                                             'cumsum_buy': 'max',
                                             'max': 'max',
                                             'minraz': 'min'}))
            print(price, max_trade, min_raz)

            f['trade'] = f.apply(func=self.funk, axis=1, args=(min_raz, price))
            # print(product_sell)
            # print(product_buy)
            print('sell', f[f['type'] == 'sell']['trade'].sum(), 'buy', f[f['type'] == 'buy']['trade'].sum())
            print(f.groupby(['price', 'type'].sum()))
