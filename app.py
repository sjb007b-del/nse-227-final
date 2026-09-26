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
    # Clean
    df.iloc[:,0] = df.iloc[:,0].astype(str).str.strip()
    df.iloc[:,1] = df.iloc[:,1].astype(str).str.strip()
    return df

df = load_data()
st.success(f"✅ Loaded {len(df)} Stocks")

stock_col = df.columns[0]
symbol_col = df.columns[1]

# FIX: Select by INDEX not by name - no more IndexError
options = [f"{i+1}. {df.iloc[i,0]} ({df.iloc[i,1]})" for i in range(len(df))]
selected_idx = st.selectbox(f"Select Stock (1 to {len(df)})", range(len(df)), format_func=lambda x: options[x])

row = df.iloc[selected_idx]
selected_name = str(row[stock_col])
symbol = str(row[symbol_col]).upper().replace(".NS","").strip()

st.info(f"Selected: {selected_name} | Symbol: {symbol}")

# Fetch chart
with st.spinner(f"Loading {symbol}..."):
    hist = yf.Ticker(symbol + ".NS").history(period="6mo")

if hist.empty:
    st.error(f"No data for {symbol}.NS")
    st.stop()

fig = go.Figure(data=[go.Candlestick(
    x=hist.index, open=hist['Open'], high=hist['High'],
    low=hist['Low'], close=hist['Close']
)])

# Box
try:
    high_val = float(row[df.columns[2]])
    low_val = float(row[df.columns[3]])
    if high_val>0 and low_val>0:
        fig.add_hrect(y0=low_val, y1=high_val, fillcolor="red", opacity=0.25, line_color="red")
        st.write(f"BOX: High {high_val} | Low {low_val}")
except:
    pass

cmp_price = hist['Close'].iloc[-1]
fig.update_layout(title=f"{selected_name} | {symbol} | CMP {round(cmp_price,2)}",
                  xaxis_rangeslider_visible=False, height=650)

st.plotly_chart(fig, use_container_width=True)
