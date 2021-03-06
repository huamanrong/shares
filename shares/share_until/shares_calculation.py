

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


def today_profit_calculation(now_price, yesterday_price, now_amount, transaction_data):
    '''
    计算当天盈利
    :param now_price: 当前价格或当天收盘价
    :param yesterday_price: 昨日收盘价
    :param now_amount: 当前股票数量
    :param transaction_data:当日交易数据,如：(('隆基股份', 0, 100, 100.0, None), ('隆基股份', 1, 100, None, 101.0))
    :return:
    '''
    today_profit = 0
    amount = 0  # 当天卖出股票的数量
    for sub in transaction_data:
        if sub[1]:  # 卖
            today_profit += (sub[4] - yesterday_price) * sub[2]
            amount -= sub[2]
            now_amount += sub[2]    # 为了得到昨日的股票数量
        elif not sub[1]:  # 买
            today_profit += (now_price - sub[3]) * sub[2]
            now_amount -= sub[2]    # 为了得到昨日的股票数量
    today_profit = today_profit + (now_price - yesterday_price) * (now_amount - amount)
    return today_profit


if __name__ == '__main__':
    print(price_calculation(100, 500, 0, 80, 500))

