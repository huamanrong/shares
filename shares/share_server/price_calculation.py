

def price_difference(buy_price, buy_amount, sell_price, sell_amount):
    '''
    计算做T的盈利
    :param buy_price:
    :param buy_amount:
    :param sell_price:
    :param sell_amount:
    :return: profit做T盈利
    '''


def price_calculation(cost, total_amount, type_, price, amount):
    '''
    计算新增交易后的持股成本
    :param cost: float 未新增交易前的持股成本
    :param total_amount: int 未新增交易前的持股数量
    :param type_: int 买入或卖出的类型，0买入，1卖出
    :param price: float 新增交易的价格
    :param amount: int 新增交易的数量
    :return: after_cost float 计算后的成本
    '''
    if type_:
        after_cost = round((cost*total_amount - price*amount)/(total_amount - amount), 3)
    else:
        after_cost = round((cost * total_amount + price * amount) / (total_amount + amount), 3)
    return after_cost


if __name__ == '__main__':
    print(price_calculation(100, 500, 0, 80, 500))

