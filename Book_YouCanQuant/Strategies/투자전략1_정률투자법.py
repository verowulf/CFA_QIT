'''
투자전략 1 정률투자법

책 [할수있다 퀀트투자] p.73
'''

def initialize(context):
    # set_benchmark(symbol('SPY'))
    
    context.spy = sid(8554)  # SPDR S&P500 ETF
    
    context.ief = sid(23870) # IEF: iShares 7-10 Year Treasury Bond ETF
    # Inception date: Jul 22, 2002
    # https://www.ishares.com/us/products/239456/ishares-710-year-treasury-bond-etf
    
    '''
    # List of US Treasury Bond ETFs
    # https://www.thebalance.com/list-of-us-treasury-bond-etfs-1214724
    
    from quantopian.pipeline.data.quandl import fred_dgs10
    # 10-Year Treasury Constant Maturity Rate
    # 더 이상 지원 안함
    
    # fetch_csv('https://yourserver.com/10yr.csv', symbol='10yr')
    # https://www.quantopian.com/help#overview-fetcher
    '''
    
    schedule_function(rebalance,
                      date_rules.month_start(days_offset=1),
                      time_rules.market_open(hours=0, minutes=30),
                      half_days=True
                     )
    
    schedule_function(record_vars, date_rules.every_day(), time_rules.market_close())
    
def rebalance(context, data):
    # Hold 49.5% SPY, 49.5% IEF, 1% Cash
    order_target_percent(context.spy, .495)
    order_target_percent(context.ief, .495)
    
def record_vars(context, data):
    record(IEF=data.current(context.ief, 'price'),
           SPY=data.current(context.spy, 'price'))
    
# def handle_data(context, data):
