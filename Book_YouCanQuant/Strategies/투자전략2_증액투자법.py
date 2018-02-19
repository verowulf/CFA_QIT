'''
투자전략 2 증액투자법

책 [할수있다 퀀트투자] p.75
'''

def initialize(context):
    
    context.min_ief = 1e6 * .99
    # Note that if greater than 1e6, difficult to buy enough of Treasury ETF
    
    context.flag = 0
    
    context.spy = sid(8554)  # SPDR S&P500 ETF
    
    context.ief = sid(23870) # iShares 7-10 Year Treasury Bond ETF
    # Inception date: Jul 22, 2002
    # https://www.ishares.com/us/products/239456/ishares-710-year-treasury-bond-etf
    
    schedule_function(rebalance,
                      date_rules.month_start(days_offset=1),
                      time_rules.market_open(hours=0, minutes=30),
                      half_days=True
                     )
    
    schedule_function(record_vars, date_rules.every_day(), time_rules.market_close())

def rebalance(context, data):
    # if bought Treasury ETF
    if context.flag == 1:
        if context.portfolio.positions[context.ief] < context.min_ief:
            order_target_percent(context.ief, .99)
            order_target_percent(context.spy, .00)
        else:
            order_target_value(context.ief, context.min_ief)
            order_target_value(context.spy,
                               context.portfolio.portfolio_value * .99 - context.min_ief)
    
    # if never bought Treasury ETF
    elif context.flag == 0:
        order_target_percent(context.ief, .99)
        context.flag = 1
        
def record_vars(context, data):
    record(IEF=data.current(context.ief, 'price'),
           SPY=data.current(context.spy, 'price'))
