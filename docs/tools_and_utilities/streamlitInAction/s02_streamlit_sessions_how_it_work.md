# Streamlit How it work

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Streamlit How it work](#streamlit-how-it-work)
    - [Widgets and Elements Session Triggers](#widgets-and-elements-session-triggers)
        - [**Streamlit Widgets and Their State Management**](#streamlit-widgets-and-their-state-management)
        - [**Key Notes:**](#key-notes)
    - [Concept and Philosophy](#concept-and-philosophy)
        - [Key Points About Sidebar Widgets:](#key-points-about-sidebar-widgets)
        - [Example: Button in the Sidebar](#example-button-in-the-sidebar)
        - [What Happens Here:](#what-happens-here)
        - [Sidebar and Stateful Widgets (`st.session_state`)](#sidebar-and-stateful-widgets-stsession_state)
            - [Example: Persisting Sidebar Button State](#example-persisting-sidebar-button-state)
        - [Explanation:](#explanation)
    - [Checking Question](#checking-question)
        - [Improvements: Why and How to Use `st.session_state` in This Code](#improvements-why-and-how-to-use-stsession_state-in-this-code)
        - [Suggested Improvements to the Code](#suggested-improvements-to-the-code)
        - [Key Improvements:](#key-improvements)

<!-- markdown-toc end -->


## Widgets and Elements Session Triggers

Create a table grouping widgets requiring cautious use of `session.state` and
alternatives that retrieve the last saved value, ensuring consistency without
omissions.
Here’s a comprehensive table categorizing Streamlit widgets based on whether
they require `st.session_state` for state preservation or can retrieve the last
value without explicit session management.

---

### **Streamlit Widgets and Their State Management**

| **Widget**                   | **Preserves Last Value Without `st.session_state`?** | **Needs `st.session_state` for Persistent State?** | **Remarks**                                                                                    |
| ---------------------------- | ---------------------------------------------------- | -------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **st.button**                | No                                                   | Yes                                                | Returns `True` only on the interaction cycle when clicked, resets to `False` after rerun.      |
| **st.checkbox**              | Yes                                                  | Optional                                           | Retains last value by default but can use `st.session_state` for controlled interactions.      |
| **st.radio**                 | Yes                                                  | Optional                                           | Remembers last selected option without needing `st.session_state`.                             |
| **st.selectbox**             | Yes                                                  | Optional                                           | Remembers last selected value automatically.                                                   |
| **st.multiselect**           | Yes                                                  | Optional                                           | Retains selected values by default.                                                            |
| **st.slider**                | Yes                                                  | Optional                                           | Retains last slider position without `st.session_state`.                                       |
| **st.text_input**            | Yes                                                  | Optional                                           | Input persists automatically unless `value` is dynamically set each rerun.                     |
| **st.text_area**             | Yes                                                  | Optional                                           | Works like `st.text_input` and remembers the last input value.                                 |
| **st.number_input**          | Yes                                                  | Optional                                           | Remembers last number entered.                                                                 |
| **st.date_input**            | Yes                                                  | Optional                                           | Retains last selected date automatically.                                                      |
| **st.time_input**            | Yes                                                  | Optional                                           | Works similarly to `st.date_input` for time selection.                                         |
| **st.file_uploader**         | No                                                   | Yes                                                | Uploaded file is cleared after a script rerun unless stored in `st.session_state`.             |
| **st.color_picker**          | Yes                                                  | Optional                                           | Remembers last selected color without needing `st.session_state`.                              |
| **st.download_button**       | No                                                   | Yes                                                | Button resets after the first interaction; use `st.session_state` to track download clicks.    |
| **st.form_submit_button**    | No                                                   | Yes                                                | State is not persistent; must be stored in `st.session_state` if needed after form submission. |
| **st.slider (range)**        | Yes                                                  | Optional                                           | Retains selected range automatically.                                                          |
| **st.toggle**                | Yes                                                  | Optional                                           | Works like `st.checkbox` and retains state automatically.                                      |
| **st.file_uploader (multi)** | No                                                   | Yes                                                | Uploaded files are cleared on rerun without `st.session_state`.                                |

---

### **Key Notes:**

- **Widgets That Need `st.session_state`**:

  - Use `st.session_state` for widgets like `st.button`, `st.file_uploader`, and `st.download_button` because their state resets with each script rerun.
  - For complex interactions (e.g., keeping track of a button toggle or a file upload), `st.session_state` provides persistence.

- **Widgets That Don't Need `st.session_state`**:
  - Most input widgets (e.g., `st.selectbox`, `st.slider`, `st.text_input`) inherently retain their state between interactions, so `st.session_state` is optional unless you need additional control over behavior.

---


## Concept and Philosophy

Let's learn more about Streamlit dashboards. I want to know about advanced concepts.

First, about which element reruns the script from start to end each time we
interact with it? I think if I click a button, it will be true. And if I click a
second button below it, it will be true while the first one goes back to false.
Let's start here and skip the basics of Streamlit.

---

- **sidebar widgets** in Streamlit behave the same as main area widgets—they are also stateless by default.

### Key Points About Sidebar Widgets:

1. **Script Rerun**: Interacting with a widget in the sidebar (e.g., clicking a
   button, changing a slider, or selecting a dropdown) triggers a full rerun of
   the script from start to end, just like widgets in the main area.

2. **Stateless Behavior**: Buttons in the sidebar reset to `False` after the
   script reruns, just like buttons in the main area.

---

### Example: Button in the Sidebar

```python
import streamlit as st

st.sidebar.title("Sidebar Interaction")

# Sidebar Button
if st.sidebar.button("Sidebar Button"):
    st.sidebar.write("You clicked the sidebar button!")

# Main Area Button
if st.button("Main Area Button"):
    st.write("You clicked the main area button!")
```

### What Happens Here:

1. If you click the **"Sidebar Button"**, the script reruns:
   - The sidebar button returns `True` for that cycle, displaying "You clicked
     the sidebar button!" in the sidebar.
   - After the script reruns, the sidebar button resets to `False`.
2. If you click the **"Main Area Button"**, the same behavior applies: the
   sidebar button resets to `False`, and "You clicked the main area button!" is
   shown in the main area.

---

### Sidebar and Stateful Widgets (`st.session_state`)

If you want to preserve the state of the sidebar widget (or any widget), you can
use `st.session_state`. This allows you to track and persist widget interactions
across script reruns.

#### Example: Persisting Sidebar Button State

```python
import streamlit as st

# Initialize state if it doesn't exist
if "sidebar_button_clicked" not in st.session_state:
    st.session_state.sidebar_button_clicked = False

def handle_sidebar_click():
    st.session_state.sidebar_button_clicked = True

# Sidebar Button with State
st.sidebar.title("Sidebar Interaction with State")
st.sidebar.button("Sidebar Button", on_click=handle_sidebar_click)

# Show Persistent State
if st.session_state.sidebar_button_clicked:
    st.sidebar.write("Sidebar button has been clicked!")
```

### Explanation:

1. **`st.session_state`**:
   - Tracks the state of the button click (`sidebar_button_clicked`).
   - This state persists across reruns, so the button click can trigger a
     persistent effect.
2. **`on_click` Callback**:
   - Updates the `st.session_state` when the sidebar button is clicked.

Would you like to explore more about using `st.session_state` for advanced state
management or dive into other Streamlit topics?

## Checking Question

For the following `Simple` dashboard

- Explain why the author chose not to use `st.session` to store sidebar values.
- Additionally, assess if the provided code is flawed and requires improvements.

```py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import ta

##########################################################################################
## PART 1: Define Functions for Pulling, Processing, and Creating Techincial Indicators ##
##########################################################################################

# Fetch stock data based on the ticker, period, and interval
def fetch_stock_data(ticker, period, interval):
    end_date = datetime.now()
    if period == '1wk':
        start_date = end_date - timedelta(days=7)
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    else:
        data = yf.download(ticker, period=period, interval=interval)
    return data

# Process data to ensure it is timezone-aware and has the correct format
def process_data(data):
    if data.index.tzinfo is None:
        data.index = data.index.tz_localize('UTC')
    data.index = data.index.tz_convert('US/Eastern')
    data.reset_index(inplace=True)
    data.rename(columns={'Date': 'Datetime'}, inplace=True)
    return data

# Calculate basic metrics from the stock data
def calculate_metrics(data):
    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[0]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    high = data['High'].max()
    low = data['Low'].min()
    volume = data['Volume'].sum()
    return last_close, change, pct_change, high, low, volume

# Add simple moving average (SMA) and exponential moving average (EMA) indicators
def add_technical_indicators(data):
    data['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
    data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)
    return data

###############################################
## PART 2: Creating the Dashboard App layout ##
###############################################


# Set up Streamlit page layout
st.set_page_config(layout="wide")
st.title('Real Time Stock Dashboard')


# 2A: SIDEBAR PARAMETERS ############

# Sidebar for user input parameters
st.sidebar.header('Chart Parameters')
ticker = st.sidebar.text_input('Ticker', 'ADBE')
time_period = st.sidebar.selectbox('Time Period', ['1d', '1wk', '1mo', '1y', 'max'])
chart_type = st.sidebar.selectbox('Chart Type', ['Candlestick', 'Line'])
indicators = st.sidebar.multiselect('Technical Indicators', ['SMA 20', 'EMA 20'])

# Mapping of time periods to data intervals
interval_mapping = {
    '1d': '1m',
    '1wk': '30m',
    '1mo': '1d',
    '1y': '1wk',
    'max': '1wk'
}


# 2B: MAIN CONTENT AREA ############

# Update the dashboard based on user input
if st.sidebar.button('Update'):
    data = fetch_stock_data(ticker, time_period, interval_mapping[time_period])
    data = process_data(data)
    data = add_technical_indicators(data)

    last_close, change, pct_change, high, low, volume = calculate_metrics(data)

    # Display main metrics
    st.metric(label=f"{ticker} Last Price", value=f"{last_close:.2f} USD", delta=f"{change:.2f} ({pct_change:.2f}%)")

    col1, col2, col3 = st.columns(3)
    col1.metric("High", f"{high:.2f} USD")
    col2.metric("Low", f"{low:.2f} USD")
    col3.metric("Volume", f"{volume:,}")

    # Plot the stock price chart
    fig = go.Figure()
    if chart_type == 'Candlestick':
        fig.add_trace(go.Candlestick(x=data['Datetime'],
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close']))
    else:
        fig = px.line(data, x='Datetime', y='Close')

    # Add selected technical indicators to the chart
    for indicator in indicators:
        if indicator == 'SMA 20':
            fig.add_trace(go.Scatter(x=data['Datetime'], y=data['SMA_20'], name='SMA 20'))
        elif indicator == 'EMA 20':
            fig.add_trace(go.Scatter(x=data['Datetime'], y=data['EMA_20'], name='EMA 20'))

    # Format graph
    fig.update_layout(title=f'{ticker} {time_period.upper()} Chart',
                      xaxis_title='Time',
                      yaxis_title='Price (USD)',
                      height=600)
    st.plotly_chart(fig, use_container_width=True)

    # Display historical data and technical indicators
    st.subheader('Historical Data')
    st.dataframe(data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']])

    st.subheader('Technical Indicators')
    st.dataframe(data[['Datetime', 'SMA_20', 'EMA_20']])


# 2C: SIDEBAR PRICES ############

# Sidebar section for real-time stock prices of selected symbols
st.sidebar.header('Real-Time Stock Prices')
stock_symbols = ['AAPL', 'GOOGL', 'AMZN', 'MSFT']
for symbol in stock_symbols:
    real_time_data = fetch_stock_data(symbol, '1d', '1m')
    if not real_time_data.empty:
        real_time_data = process_data(real_time_data)
        last_price = real_time_data['Close'].iloc[-1]
        change = last_price - real_time_data['Open'].iloc[0]
        pct_change = (change / real_time_data['Open'].iloc[0]) * 100
        st.sidebar.metric(f"{symbol}", f"{last_price:.2f} USD", f"{change:.2f} ({pct_change:.2f}%)")

# Sidebar information section
st.sidebar.subheader('About')
```

---

The author did not use `st.session_state` in the code for storing sidebar values because the script works fine without it, given Streamlit’s default behavior. Here’s why:

1. **No Persistent State is Required**:

   - The sidebar widgets (like `st.text_input`, `st.selectbox`, and `st.multiselect`) return the latest values directly during each script rerun. These values are immediately used to fetch stock data, calculate metrics, or update the chart.
   - Since the widgets' values are inherently tied to user input and the script execution happens from top to bottom, there was no need for `st.session_state` to persist these values explicitly.

2. **Stateless Design**:
   - The current implementation follows Streamlit's default stateless approach, where the entire script reruns and updates based on the user's interaction with widgets. This works well if there's no need for persistent state management across interactions.

---

### Improvements: Why and How to Use `st.session_state` in This Code

Although the code works, **using `st.session_state` can improve efficiency and user experience** in the following ways:

1. **Preserve User Input Across Reruns**:

   - If a user clicks "Update" to refresh the chart, the script will rerun. However, if the user had made specific adjustments (e.g., selected `SMA 20` and `EMA 20` indicators), these settings could be lost if the logic isn’t carefully handled.
   - By storing these values in `st.session_state`, the selections can persist across reruns.

2. **Prevent Redundant API Calls**:

   - If a user repeatedly clicks "Update" with the same settings, the script unnecessarily fetches the same data again from Yahoo Finance. By caching the results using `st.session_state`, you can avoid redundant calls and speed up the dashboard.

3. **Improved Sidebar Real-Time Price Updates**:
   - Instead of fetching real-time prices for multiple stocks (e.g., AAPL, MSFT) on every interaction, store these values in `st.session_state` and update them only when necessary (e.g., after a fixed interval).

---

### Suggested Improvements to the Code

Here’s the improved code using `st.session_state`:

```python
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import ta

##########################################################################################
## PART 1: Define Functions for Pulling, Processing, and Creating Techincial Indicators ##
##########################################################################################

# Fetch stock data based on the ticker, period, and interval
@st.cache_data
def fetch_stock_data(ticker, period, interval):
    end_date = datetime.now()
    if period == '1wk':
        start_date = end_date - timedelta(days=7)
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    else:
        data = yf.download(ticker, period=period, interval=interval)
    return data

# Process data to ensure it is timezone-aware and has the correct format
def process_data(data):
    if data.index.tzinfo is None:
        data.index = data.index.tz_localize('UTC')
    data.index = data.index.tz_convert('US/Eastern')
    data.reset_index(inplace=True)
    data.rename(columns={'Date': 'Datetime'}, inplace=True)
    return data

# Calculate basic metrics from the stock data
def calculate_metrics(data):
    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[0]
    change = last_close - prev_close
    pct_change = (change / prev_close) * 100
    high = data['High'].max()
    low = data['Low'].min()
    volume = data['Volume'].sum()
    return last_close, change, pct_change, high, low, volume

# Add simple moving average (SMA) and exponential moving average (EMA) indicators
def add_technical_indicators(data):
    data['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
    data['EMA_20'] = ta.trend.ema_indicator(data['Close'], window=20)
    return data

###############################################
## PART 2: Creating the Dashboard App layout ##
###############################################

# Set up Streamlit page layout
st.set_page_config(layout="wide")
st.title('Real Time Stock Dashboard')

# Initialize session state for ticker and parameters
if 'ticker' not in st.session_state:
    st.session_state.ticker = 'ADBE'
if 'time_period' not in st.session_state:
    st.session_state.time_period = '1d'
if 'chart_type' not in st.session_state:
    st.session_state.chart_type = 'Candlestick'
if 'indicators' not in st.session_state:
    st.session_state.indicators = []

# Sidebar for user input parameters
st.sidebar.header('Chart Parameters')
st.session_state.ticker = st.sidebar.text_input('Ticker', st.session_state.ticker)
st.session_state.time_period = st.sidebar.selectbox('Time Period', ['1d', '1wk', '1mo', '1y', 'max'], index=['1d', '1wk', '1mo', '1y', 'max'].index(st.session_state.time_period))
st.session_state.chart_type = st.sidebar.selectbox('Chart Type', ['Candlestick', 'Line'], index=['Candlestick', 'Line'].index(st.session_state.chart_type))
st.session_state.indicators = st.sidebar.multiselect('Technical Indicators', ['SMA 20', 'EMA 20'], default=st.session_state.indicators)

interval_mapping = {
    '1d': '1m',
    '1wk': '30m',
    '1mo': '1d',
    '1y': '1wk',
    'max': '1wk'
}

if st.sidebar.button('Update'):
    data = fetch_stock_data(st.session_state.ticker, st.session_state.time_period, interval_mapping[st.session_state.time_period])
    data = process_data(data)
    data = add_technical_indicators(data)
    st.session_state.data = data
    st.session_state.last_close, st.session_state.change, st.session_state.pct_change, \
    st.session_state.high, st.session_state.low, st.session_state.volume = calculate_metrics(data)

# Display results if data exists
if 'data' in st.session_state:
    st.metric(label=f"{st.session_state.ticker} Last Price", value=f"{st.session_state.last_close:.2f} USD", delta=f"{st.session_state.change:.2f} ({st.session_state.pct_change:.2f}%)")

    col1, col2, col3 = st.columns(3)
    col1.metric("High", f"{st.session_state.high:.2f} USD")
    col2.metric("Low", f"{st.session_state.low:.2f} USD")
    col3.metric("Volume", f"{st.session_state.volume:,}")

    # Plot the stock price chart
    fig = go.Figure()
    if st.session_state.chart_type == 'Candlestick':
        fig.add_trace(go.Candlestick(x=st.session_state.data['Datetime'],
                                     open=st.session_state.data['Open'],
                                     high=st.session_state.data['High'],
                                     low=st.session_state.data['Low'],
                                     close=st.session_state.data['Close']))
    else:
        fig = px.line(st.session_state.data, x='Datetime', y='Close')

    for indicator in st.session_state.indicators:
        if indicator == 'SMA 20':
            fig.add_trace(go.Scatter(x=st.session_state.data['Datetime'], y=st.session_state.data['SMA_20'], name='SMA 20'))
        elif indicator == 'EMA 20':
            fig.add_trace(go.Scatter(x=st.session_state.data['Datetime'], y=st.session_state.data['EMA_20'], name='EMA 20'))

    fig.update_layout(title=f"{st.session_state.ticker} {st.session_state.time_period.upper()} Chart",
                      xaxis_title='Time',
                      yaxis_title='Price (USD)',
                      height=600)
    st.plotly_chart(fig, use_container_width=True)
```

---

### Key Improvements:

1. **Persisting Sidebar Selections**:

   - The user's ticker, time period, chart type, and selected indicators persist
     between interactions.

2. **Preventing Redundant Fetching**:

   - The stock data is fetched only when the "Update" button is clicked and
     stored in `st.session_state`.

3. **Caching Stock Data**:

   - `@st.cache_data` ensures data fetching is efficient and avoids repeated
     calls for the same parameters.

4. **Improved User Experience**:
   - State preservation avoids user frustration from losing settings after each
     interaction.


------

