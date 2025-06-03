import pandas as pd

def human_format(num):
    if num is None or pd.isna(num):
        return "N/A"
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return f"{num:.2f}{['', 'K', 'M', 'B', 'T'][magnitude]}"

def get_financial_metrics(ticker):

    income_statement = ticker.financials.T
    cashflow_stmt = ticker.cashflow.T
    info = ticker.info

    revenue_ttm = net_income = profit_margin = fcf = eps_ttm = pe_ratio = dividend_yield = None

    try:

        revenue_cols = ['Total Revenue', 'Revenue']
        for col in revenue_cols:
            if col in income_statement.columns:
                recent_revenues = income_statement[col].dropna().iloc[:4]
                if not recent_revenues.empty:
                    revenue_ttm = recent_revenues.sum()
                    break

        net_income = income_statement['Net Income'].dropna().iloc[0] if 'Net Income' in income_statement else None

        profit_margin = (net_income / revenue_ttm) if (revenue_ttm and net_income) else None

        if 'Free Cash Flow' in cashflow_stmt.columns:
            fcf = cashflow_stmt['Free Cash Flow'].dropna().iloc[0]
        elif 'Operating Cash Flow' in cashflow_stmt.columns and 'Capital Expenditure' in cashflow_stmt.columns:
            ocf = cashflow_stmt['Operating Cash Flow'].dropna().iloc[0]
            capex = cashflow_stmt['Capital Expenditure'].dropna().iloc[0]
            fcf = ocf - capex

        eps_ttm = info.get('trailingEps')
        pe_ratio = info.get('trailingPE')
        dividend_yield = info.get('dividendYield')

    except Exception as e:
        print(f"Error: {e}")

    revenue_display = human_format(revenue_ttm)
    net_income_display = human_format(net_income)
    profit_margin_display = f"{profit_margin:.2%}" if profit_margin else "N/A"
    fcf_display = human_format(fcf)
    eps_display = f"{eps_ttm:.2f}" if eps_ttm else "N/A"
    pe_display = f"{pe_ratio:.2f}" if pe_ratio else "N/A"
    dividend_display = f"{dividend_yield * 100:.2f}%" if dividend_yield else "N/A"

    return revenue_display, net_income_display, profit_margin_display, fcf_display, eps_display, pe_display, dividend_display