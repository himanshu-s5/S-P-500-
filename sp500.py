import streamlit as st 
import pandas as pd 
import yfinance as yf 
import base64
import matplotlib.pyplot as plt

st.title('S&P 500 SP')

st.markdown("""
This app retrieves the list of the **S&P 500** (from Wikipedia).
**Python libraries used:** `base64`, `pandas`, `streamlit`, `numpy`, `matplotlib`.
**Data source:** [Wikipedia](https://www.wikipedia.org/)
""")

st.sidebar.header("user input feature")

@st.cache_data
def load_data():
    
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    html = pd.read_html(url, header=0)
    df = html[0]
    return df

df = load_data()
st.write(pd.DataFrame(df))

sector = df.groupby('GICS Sector')
sector_unique = df['GICS Sector'].unique()
sorted_sector = sorted(sector_unique)

selected_sector = st.sidebar.multiselect('Sector', sorted_sector)

filtered_data = df[(df['GICS Sector'].isin(selected_sector))]

if not filtered_data.empty:
    st.header("Filtered data are display here")
    st.write(f" data filtered {filtered_data.shape[0]} rows and {filtered_data.shape[1]} colomns")
    st.write(filtered_data)

def file_download(df):
    
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown("""
                ### Download the file
                """)
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href


if not filtered_data.empty:
    st.markdown(file_download(filtered_data), unsafe_allow_html=True)

if not filtered_data.empty:
    symbols = filtered_data['Symbol'].tolist()  
    data = yf.download(
        tickers=symbols[:10],
        period="ytd",
        interval="1d",
        group_by="ticker",
        auto_adjust=True,
        threads=True,
        proxy=None
    )

def price_plot(symbol):
        df = pd.DataFrame(data[symbol]['Close'])
        df['Date'] = df.index


        fig, ax = plt.subplots()

        ax.fill_between(df.Date, df.Close, color='skyblue', alpha=0.8)
        ax.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
        ax.set_xticks(df.Date[::len(df.Date)//10])
        ax.tick_params(axis='x', rotation=90)
        ax.set_title(symbol, fontweight ='bold')
        ax.set_xlabel('Date', fontweight='bold')
        ax.set_ylabel('Closing Price', fontweight='bold')

        st.pyplot(fig)


if not filtered_data.empty:
    
    num_company = st.sidebar.slider('Select number of **companies** you want to show plots', 1, min(10,len(filtered_data)))

    if st.button("Show plots"):
        st.header('Stock Closing Price')
        for symbol in symbols[:num_company]:
            price_plot(symbol)