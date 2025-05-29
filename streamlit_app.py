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

# Panggil API kadar tukaran
url = f'https://api.vatcomply.com/rates?base={from_currency}'
response = requests.get(url)

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

# Cadangan pelancongan + harga tiket
travel_info = {
    'USD': {
        'dest': 'New York, USA 🇺🇸',
        'flight': 3500,
        'bus': None,
        'ship': 1800
    },
    'MYR': {
        'dest': 'Langkawi, Malaysia 🇲🇾',
        'flight': 200,
        'bus': 80,
        'ship': 90
    },
    'EUR': {
        'dest': 'Paris, France 🇫🇷',
        'flight': 3200,
        'bus': None,
        'ship': None
    },
    'GBP': {
        'dest': 'London, UK 🇬🇧',
        'flight': 3300,
        'bus': None,
        'ship': None
    },
    'SGD': {
        'dest': 'Singapore 🇸🇬',
        'flight': 250,
        'bus': 100,
        'ship': None
    },
    'JPY': {
        'dest': 'Tokyo, Japan 🇯🇵',
        'flight': 2700,
        'bus': None,
        'ship': None
    },
    'THB': {
        'dest': 'Bangkok, Thailand 🇹🇭',
        'flight': 400,
        'bus': 120,
        'ship': None
    },
    'AUD': {
        'dest': 'Sydney, Australia 🇦🇺',
        'flight': 2900,
        'bus': None,
        'ship': 1700
    }
}

# Papar maklumat pelancongan dan harga tiket
if to_currency in travel_info:
    info = travel_info[to_currency]
    st.subheader("Cadangan Destinasi Pelancongan 🎒✈️")
    st.info(f"Jika anda tukar ke {to_currency}, anda boleh melancong ke: **{info['dest']}**")

    st.subheader("💸 Anggaran Harga Tiket Perjalanan dari Malaysia:")
    if info['flight']:
        st.write(f"✈️ **Kapal Terbang**: RM {info['flight']}")
    if info['bus']:
        st.write(f"🚌 **Bas**: RM {info['bus']}")
    if info['ship']:
        st.write(f"🚢 **Kapal**: RM {info['ship']}")
