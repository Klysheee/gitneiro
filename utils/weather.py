import requests

async def fetch_weather(ctx, city: str, api_key: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        await ctx.send(f"Погода в {city}: {temperature}°C, {description}.")
    else:
        await ctx.send(f"Не удалось получить данные о погоде для {city}.")
