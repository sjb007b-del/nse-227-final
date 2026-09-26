import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="NSE 227 FINAL", layout="wide")
st.title("NSE 227 - FINAL BOX Dashboard")

@st.cache_data
def load_data():
    df1 = pd.read_excel("excel111.xlsx", engine="openpyxl")
    df2 = pd.read_excel("excel114_1.xlsx", engine="openpyxl")
    df = pd.concat([df1, df2], ignore_index=True)
    return df

df = load_data()
st.success(f"✅ Loaded {len(df)} Stocks Successfully - No More BadZip!")

st.dataframe(df, use_container_width=True, height=400)

stock_col = df.columns[0]
symbol_col = df.columns[1]

stocks = df[stock_col].astype(str).tolist()
selected = st.selectbox(f"Select Stock (1 to {len(df)})", stocks)

row = df[df[stock_col]==selected].iloc[0]
symbol = str(row[symbol_col]).strip().upper().replace(".NS","")

# Fetch chart
with st.spinner(f"Loading {symbol}..."):
    hist = yf.Ticker(symbol + ".NS").history(period="6mo")

if hist.empty:
    st.error(f"No chart data for {symbol}")
    st.stop()

fig = go.Figure(data=[go.Candlestick(
    x=hist.index, open=hist['Open'], high=hist['High'],
    low=hist['Low'], close=hist['Close']
)])

# Box
try:
    high = float(row[df.columns[2]])
    low = float(row[df.columns[3]])
    if high>0 and low>0:
        fig.add_hrect(y0=low, y1=high, fillcolor="red", opacity=0.25, line_color="red")
except:
    pass

cmp_price = hist['Close'].iloc[-1]
fig.update_layout(title=f"{selected} | {symbol} | CMP {round(cmp_price,2)}",
                  xaxis_rangeslider_visible=False, height=650)

st.plotly_chart(fig, use_container_width=True)
