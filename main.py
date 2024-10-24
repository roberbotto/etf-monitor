import yfinance as yf


ETF = "QQQ3.L"


def get_drawdown(last_price, max_price):
    """ Return a tuple containing the current drawdown and if its
        enought or not to call Telegram API """
    drawdown = (max_price - last_price) / max_price
    return (
        round(drawdown, 2),
        True if drawdown >= 0.3 else False
    )

def make_telegram_request():
    pass

def lambda_handler(event, context):
    try:
        ticker = yf.Ticker(ETF)
        data_52_weeks = ticker.history(period="1y")
        last_day_price = data_52_weeks['Close'].iloc[-1]
        max_price_52_weeks = data_52_weeks['High'].max()

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
    
    body = {
        'last_day_price': round(last_day_price, 2),
        'max_price_52_weeks': round(max_price_52_weeks, 2),
        'telegram_request': False
    }

    body['drawdown'], bigger_than_30 = get_drawdown(last_day_price, max_price_52_weeks)

    if bigger_than_30:
        make_telegram_request()
        body['telegram_request'] = True

    return {
        'statusCode': 200,
        'body': body
    }


if __name__ == "__main__":
    print(lambda_handler(None, None))
