import requests, os

def get_weather(app):
    key_file = os.path.join(app.static_folder, 'key/openweather.txt')
    with open(key_file) as f:
        weather_key = f.read()
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    lat, lon = 37.295, 127.045          # 수원 중심부 좌표
    url = f'{base_url}?lat={lat}&lon={lon}&appid={weather_key}&units=metric&lang=kr'
    result = requests.get(url).json()
    desc = result['weather'][0]['description']
    icon_code = result['weather'][0]['icon']
    icon_url = f'http://api.openweathermap.org/img/w/{icon_code}.png'
    temp_ = result['main']['temp']
    temp = round(float(temp_) + 0.01, 1)
    html = f'''<img src="{icon_url}" height="32"><strong>{desc}</strong>,
            온도: <strong>{temp}</strong>&#8451'''
    return html

def get_weather_by_coord(app, lat, lng):
    key_file = os.path.join(app.static_folder, 'key/openweather.txt')
    with open(key_file) as f:
        weather_key = f.read()
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    url = f'{base_url}?lat={lat}&lon={lng}&appid={weather_key}&units=metric&lang=kr'
    result = requests.get(url).json()
    desc = result['weather'][0]['description']
    icon_code = result['weather'][0]['icon']
    icon_url = f'http://api.openweathermap.org/img/w/{icon_code}.png'
    temp_ = result['main']['temp']
    temp = round(float(temp_) + 0.01, 1)
    html = f'''<img src="{icon_url}" height="32"><strong>{desc}</strong>,
            온도: <strong>{temp}</strong>&#8451'''
    return html