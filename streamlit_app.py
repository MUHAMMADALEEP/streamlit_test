import streamlit as st 
import requests

# Set the app title 
st.title('HELLO MOTHER FATHER') 

# Add a welcome message 
st.write('Welcome my AKU,KITA,KAU,FIK NGN ALIFF') 

# Create a text input 
widgetuser_input = st.text_input('Enter a custom message:', 'Hello, Streamlit!') 
st.write('Customized Message:', widgetuser_input)

# Senarai mata wang
currency_list = ['USD', 'MYR', 'EUR', 'GBP', 'SGD', 'JPY', 'THB', 'AUD']

# Pilihan mata wang FROM dan TO
from_currency = st.selectbox('Dari mata wang (FROM):', currency_list)
to_currency = st.selectbox('Ke mata wang (TO):', currency_list)

# Masukkan amaun
amount = st.number_input('Masukkan amaun yang ingin ditukar:', min_value=0.0, value=100.0)

# Panggil API untuk kadar tukaran
url = f'https://api.vatcomply.com/rates?base={from_currency}'
response = requests.get(url)

# Proses data
if response.status_code == 200:
    data = response.json()
    rates = data['rates']

    if to_currency in rates:
        rate = rates[to_currency]
        converted_amount = amount * rate

        st.success(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
    else:
        st.warning(f"Kadar tukaran ke {to_currency} tidak tersedia.")
else:
    st.error(f"API gagal dengan kod status: {response.status_code}")

# Saranan tempat pelancongan berdasarkan mata wang sasaran
travel_suggestions = {
    'USD': 'New York, USA 🇺🇸',
    'MYR': 'Langkawi, Malaysia 🇲🇾',
    'EUR': 'Paris, France 🇫🇷',
    'GBP': 'London, UK 🇬🇧',
    'SGD': 'Singapore 🇸🇬',
    'JPY': 'Tokyo, Japan 🇯🇵',
    'THB': 'Bangkok, Thailand 🇹🇭',
    'AUD': 'Sydney, Australia 🇦🇺'
}

if to_currency in travel_suggestions:
    st.subheader("Cadangan Destinasi Pelancongan 🎒✈️")
    st.info(f"Jika anda tukar ke {to_currency}, anda boleh melancong ke: **{travel_suggestions[to_currency]}**")
