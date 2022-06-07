import stock
import numpy as np
import pandas as pd
import time


def create_order(count: int) -> list:
    list_orders = []
    for i in range(count):
        order = {'id': i,
                 'type': np.random.choice(['sell', 'buy']),
                 'product': np.random.choice(['milk']),
                 'price': np.random.random() * 0.4 + 0.8,
                 'value': int(np.random.random() * 50 + 50)}
        if order['type'] == 'sell':
            order['price'] = round(0.9 * order['price'], 2)
        else:
            order['price'] = round(order['price'] * 1.1, 2)
        list_orders.append(order)
    return list_orders


stock = stock.Stock()

stock.append_orders(create_order(10))

stock.orders()




