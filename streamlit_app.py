import streamlit as st 
import requests

# Set the app title 
st.title('WELCOME TO MONEY CHANGER RATED') 

# Add a welcome message 
st.write('Welcome my money changer rate') 

# Create a text input 
widgetuser_input = st.text_input('Enter a custom message:', 'Hello, Streamlit!') 

# Display the customized message 
st.write('Customized Message:', MOTHER)

# Pilihan mata wang
currency_list = ['USD', 'MYR', 'EUR', 'GBP', 'SGD', 'JPY', 'THB', 'AUD']
base_currency = st.selectbox('Pilih mata wang asas (base currency):', currency_list)

# API call berdasarkan mata wang yang dipilih
url = f'https://api.vatcomply.com/rates?base={base_currency}'
response = requests.get(url)

# Tunjuk hasil
if response.status_code == 200:
    data = response.json()
    st.write(f'Kadar tukaran berdasarkan {base_currency}:')
    st.json(data)  # nicely formatted JSON output
else:
    st.error(f"API call failed with status code: {response.status_code}")
