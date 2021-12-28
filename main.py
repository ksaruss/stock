import stock
import numpy as np
import pandas as pc
import pandas as pd


def create_order(count: int) -> list:
    list_orders = []
    for i in range(count):
        order = {'type': np.random.choice(['sell', 'buy']),
                 'product': np.random.choice(['milk']),
                 'price': round(np.random.random() * 0.4 + 0.8, 2),
                 'value': int(np.random.random() * 50 + 50)}
        list_orders.append(order)
    return list_orders


stock = stock.Stock()

stock.append_orders(create_order(20))

stock.orders()
