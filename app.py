import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="NSE 227 FINAL", layout="wide")
st.title("NSE 227 - FINAL BOX Dashboard")

@st.cache_data
def load_data():
    df1 = pd.read_excel("final113.xlsx", engine="openpyxl")
    df2 = pd.read_excel("excel114_1.xlsx", engine="openpyxl")
    df = pd.concat([df1, df2], ignore_index=True)
    return df

df = load_data()
st.success(f"✅ Total Loaded: {len(df)} Stocks")

st.dataframe(df, use_container_width=True, height=400)

# Auto detect columns
stock_col = df.columns[0]
symbol_col = df.columns[1]

stocks = df[stock_col].astype(str).tolist()
selected = st.selectbox("Select Chart (1 to 227)", stocks)

row = df[df[stock_col]==selected].iloc[0]
symbol = str(row[symbol_col]).strip().upper().replace(".NS","")

# Fetch 6 month data
hist = yf.Ticker(symbol + ".NS").history(period="6mo")

if hist.empty:
    st.error(f"No chart data for {symbol}")
    st.stop()

fig = go.Figure(data=[go.Candlestick(
    x=hist.index,
    open=hist['Open'], high=hist['High'],
    low=hist['Low'], close=hist['Close']
)])

# Try BOX drawing
try:
    high_col = df.columns[2]
    low_col = df.columns[3]
    fig.add_hrect(y0=float(row[low_col]), y1=float(row[high_col]),
                  fillcolor="red", opacity=0.2, line_color="red")
except:
    pass

cmp_price = hist['Close'].iloc[-1]
fig.update_layout(title=f"{selected} | {symbol} | CMP {round(cmp_price,2)}",
                  xaxis_rangeslider_visible=False, height=650)

st.plotly_chart(fig, use_container_width=True)
