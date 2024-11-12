import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "instant": "nunique",
        "cnt": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "instant": "order_count",
        "cnt": "jumlah"
    }, inplace=True)
    
    return daily_orders_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season").cnt.sum().reset_index()
    byseason_df.rename(columns={
        "cnt": "order_count"
    }, inplace=True)
    
    return byseason_df

def create_weathersit_df(df):
    weathersit_df = df.groupby(by="weathersit").cnt.sum().reset_index()
    weathersit_df.rename(columns={
        "cnt": "order_count"
    }, inplace=True)
    
    return weathersit_df

all_df = pd.read_csv(".\main_data.csv")
all_df['dteday'] = pd.to_datetime(all_df['dteday'])
all_df.sort_values(by="dteday", inplace=True, ascending=True)
all_df.reset_index(inplace=True)
min_date = all_df['dteday'].min()
max_date = all_df['dteday'].max()

#HEADER
st.header(':bike: Bike Sharing Dashboard :bike:')

#SIDE BAR (GAMBAR + FILTER)
st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #FFFFFF;
        }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://t4.ftcdn.net/jpg/07/94/13/63/360_F_794136348_J8jmI8qjv1WCQWm7IzXWdAluyY7IGZEp.jpg")
    
    # Mengambil start_date & end_date dari date_input
    selected_dates = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    # Jika hanya satu tanggal yang dipilih
    if len(selected_dates) == 1:
        start_date = selected_dates[0]
        end_date = selected_dates[0]
        st.warning("Hanya satu tanggal yang dipilih. Rentang waktu dianggap satu hari.")
    else:
        start_date, end_date = selected_dates

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

#FUNC
daily_orders_df = create_daily_orders_df(main_df)
byseason_df = create_byseason_df(main_df)
byweathersit_df = create_weathersit_df(main_df)

#PLOT1
st.subheader('Daily Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    Jumlah_hari = daily_orders_df.order_count.sum()
    st.metric("Number of Days", value=Jumlah_hari)
 
with col2:
    jumlah_rental = daily_orders_df.jumlah.sum()
    formatted_rental = f"{jumlah_rental:,}".replace(",", ".")
    st.metric("Number of Bikes Rent", value=formatted_rental)

fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(
    daily_orders_df["dteday"],
    daily_orders_df["jumlah"],
    marker='o', 
    linewidth=2,
    color="#023047"
)
ax.tick_params(axis='y', labelsize=30)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)


#PLOT2
st.subheader("Order Distribution")
 
col1, col2 = st.columns(2)
 
colors = ["#FFB703", "#FB8500", "#023047","#219EBC"] 
colors2 = ["#90E0EF", "#00B4D8", "#0077B6","#03045E"] 
# Plot menggunakan seaborn
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    # Plot data
    sns.barplot(
        y="order_count", 
        x="season", 
        data=byseason_df,
        ax=ax,
        palette=colors
    )
    
    # Set judul
    ax.set_title("Number of Customer by Season", loc="center", fontsize=50)
    
    # Menghilangkan label sumbu X dan Y default
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    desired_labels = ["spring", "summer", "Fall", "winter"]
    # Mengubah label X dengan label yang diinginkan
    ax.set_xticks(range(len(desired_labels)))  # Mengatur posisi ticks sumbu X
    ax.set_xticklabels(desired_labels, fontsize=35)  # Menentukan label yang diinginkan

    for p in ax.patches:
        # Menambahkan teks tepat di atas bar, memberi sedikit jarak
        ax.text(
            p.get_x() + p.get_width() / 2,  # Posisi X (di tengah bar)
            p.get_height() + 5,  # Posisi Y (sedikit di atas bar, memberi jarak)
            f'{int(p.get_height())}',  # Menampilkan nilai di atas bar (gunakan int untuk membulatkan angka)
            ha='center',  # Horizontal alignment untuk teks
            va='bottom',  # Vertical alignment untuk memastikan teks berada di atas bar
            fontsize=25,  # Ukuran font
            color='black'  # Warna teks (warna hitam agar kontras dengan warna bar)
        )

    # Mengubah ukuran font untuk ticks di sumbu X dan Y
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)

    # Tampilkan plot
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    # Plot data
    sns.barplot(
        y="order_count", 
        x="weathersit", 
        data=byweathersit_df,
        ax=ax,
        palette=colors2
    )
    
    # Set judul
    ax.set_title("Number of Customer by Weather", loc="center", fontsize=50)
    
    # Menghilangkan label sumbu X dan Y default
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    desired_labels2 = ["clear", "cloudy", "light rain", "heavy rain"]
    # Mengubah label X dengan label yang diinginkan
    ax.set_xticks(range(len(desired_labels2)))  # Mengatur posisi ticks sumbu X
    ax.set_xticklabels(desired_labels2, fontsize=35)  # Menentukan label yang diinginkan

    for p in ax.patches:
        # Menambahkan teks tepat di atas bar, memberi sedikit jarak
        ax.text(
            p.get_x() + p.get_width() / 2,  # Posisi X (di tengah bar)
            p.get_height() + 5,  # Posisi Y (sedikit di atas bar, memberi jarak)
            f'{int(p.get_height())}',  # Menampilkan nilai di atas bar (gunakan int untuk membulatkan angka)
            ha='center',  # Horizontal alignment untuk teks
            va='bottom',  # Vertical alignment untuk memastikan teks berada di atas bar
            fontsize=25,  # Ukuran font
            color='black'  # Warna teks (warna hitam agar kontras dengan warna bar)
        )

    # Mengubah ukuran font untuk ticks di sumbu X dan Y
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)

    # Tampilkan plot
    st.pyplot(fig)