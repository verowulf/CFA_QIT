'''
투자전략 3 추세투자법

책 [할수있다 퀀트투자] p.80
'''

def initialize(context):
    context.spy = sid(8554)  # SPDR S&P500 ETF
    context.flag = 0  # Initially no position
    
    schedule_function(sma_check,
                      date_rules.month_start(days_offset=1),
                      time_rules.market_open(hours=0, minutes=30),
                      half_days=True
                     )

def sma_check(context, data):
    # Note that history() includes the current price for the current day.
    hist = data.history(context.spy, 'price', 81, '1d')
    
    sma_60   = hist[21:].mean()   # SMA60 of yesterday
    sma_60_p = hist[:-21].mean()  # SMA60 of a month before yesterday
    
    ''' 다른 방법
    이동평균이 상승 또는 하락추세를 n회 유지한 종목.
    또는 이동평균이 하락추세에서 상승추세로 반전하거나
    상승추세에서 하락추세로 반전한 종목 검색.
    https://download.kiwoom.com/hero3_help_new/KiwoomHero3_AdvancedSearch.htm
    '''
    
    if context.flag == 0:
        if sma_60 > sma_60_p:
            # Long
            order_target_percent(context.spy, .99)
            context.flag = 1
            
    elif context.flag == 1:
        if sma_60 < sma_60_p:
            # Short
            order_target_percent(context.spy, .00)
            context.flag = 0
    
    record(SMA_60=sma_60,
           SMA_60_P=sma_60_p)
