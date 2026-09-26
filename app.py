import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="NSE 227 BOX", layout="wide")
st.title("NSE 227 - All in One Dashboard")

@st.cache_data
def load_data():
    df1 = pd.read_excel("Excel 113.xlsx")
    df2 = pd.read_excel("excel114_1.xlsx")
    df = pd.concat([df1, df2], ignore_index=True)
    return df

df = load_data()
st.success(f"✅ Loaded {len(df)} Stocks from 2 Excels")

# Show table
st.dataframe(df, use_container_width=True, height=400)

# Detect columns automatically
stock_col = df.columns[0]
symbol_col = df.columns[1]

stocks = df[stock_col].tolist()
selected = st.selectbox("Select Chart (1 to 227)", stocks)

row = df[df[stock_col]==selected].iloc[0]
symbol = str(row[symbol_col]).strip()

# Fetch chart
ticker = yf.Ticker(symbol + ".NS")
hist = ticker.history(period="6mo")

if hist.empty:
    st.error(f"No data for {symbol}")
    st.stop()

fig = go.Figure(data=[go.Candlestick(
    x=hist.index, open=hist['Open'], high=hist['High'],
    low=hist['Low'], close=hist['Close']
)])

# Try to draw BOX if your excel has BoxHigh/BoxLow columns
cols = [c.lower() for c in df.columns]
if 'boxhigh' in str(cols) or 'high' in str(cols):
    try:
        high_col = df.columns[2]
        low_col = df.columns[3]
        fig.add_hrect(y0=row[low_col], y1=row[high_col],
                      fillcolor="red", opacity=0.2, line_color="red")
    except:
        pass

cmp_price = hist['Close'].iloc[-1]
fig.update_layout(title=f"{selected} | {symbol} | CMP {round(cmp_price,2)}",
                  xaxis_rangeslider_visible=False, height=600)

st.plotly_chart(fig, use_container_width=True)
