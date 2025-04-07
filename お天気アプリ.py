import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# 選択肢を作成
city_code_list = {
    "東京都":"130010",
    "大阪" : "270000",
}
city_code_index = "東京都"

st.title("天気アプリ")
st.write("調べたい地域を選んでください。")
city_code_index = st.selectbox("地域を選んでください。", city_code_list.keys())
city_code = city_code_list[city_code_index]
current_city_code = st.empty()
current_city_code.write("選択中の地域:" + city_code_index)

url = f"https://weather.tsukumijima.net/api/forecast/city/{city_code}"

response = requests.get(url)
weather_json = response.json()
now_hour = datetime.now().hour

if 0 <= now_hour < 6:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T00_06']
elif 6 <= now_hour < 12:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T06_12']
elif 12 <= now_hour < 18:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T12_18']
else:
    weather_now = weather_json['forecasts'][0]['chanceOfRain']['T18_24']

weather_now_text = f"現在の降水確率 : {weather_now}"
st.write(weather_now_text)

df1 = pd.DataFrame(weather_json['forecasts'][0]['chanceOfRain'], index=["今日"])
df2 = pd.DataFrame(weather_json['forecasts'][1]['chanceOfRain'], index=["明日"])
df3 = pd.DataFrame(weather_json['forecasts'][2]['chanceOfRain'], index=["明後日"])

df = pd.concat([df1, df2, df3])
st.dataframe(df)
