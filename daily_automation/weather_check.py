"""
Weather check script with clothing recommendations.
Based on 26°C dressing rule.
"""

import requests
import json
from datetime import datetime


class WeatherAdvisor:
    """Simple weather-based clothing advisor."""
    
    # 26°C dressing rule
    CLOTHING_WARMTH = {
        'thick_down_jacket': 9,
        'thin_down_jacket': 6,
        'cotton_coat': 5,
        'thick_wool_sweater': 4,
        'fleece_hoodie': 3,
        'thick_cotton_shirt': 2,
        'thin_wool_sweater': 1,
    }
    
    COMFORT_TEMP = 26  # 人体舒适温度
    
    def __init__(self, city: str = "Shanghai"):
        self.city = city
    
    def get_weather(self) -> dict:
        """Get weather data from wttr.in (free, no API key needed)."""
        try:
            url = f"https://wttr.in/{self.city}?format=j1"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None
    
    def calculate_clothing_advice(self, temp: float, condition: str) -> str:
        """Generate clothing advice based on temperature."""
        warmth_needed = self.COMFORT_TEMP - temp
        
        if warmth_needed <= 0:
            return "🌞 很热，穿短袖/短裤即可，注意防晒"
        elif warmth_needed <= 3:
            return "🌤️ 偏热，短袖+薄外套或单穿长袖"
        elif warmth_needed <= 5:
            return "☁️ 舒适，薄毛衣/卫衣+长裤"
        elif warmth_needed <= 8:
            return "🌥️ 偏凉，毛衣/厚卫衣+外套"
        elif warmth_needed <= 12:
            return "❄️ 较冷，羽绒服/厚大衣"
        else:
            return "🥶 很冷，厚羽绒服+保暖内衣+围巾手套"
    
    def generate_report(self) -> str:
        """Generate full weather report."""
        weather = self.get_weather()
        if not weather:
            return "❌ 无法获取天气信息"
        
        current = weather['current_condition'][0]
        temp = float(current['temp_C'])
        feels_like = float(current['FeelsLikeC'])
        condition = current['lang_zh'][0]['value'] if 'lang_zh' in current else current['weatherDesc'][0]['value']
        humidity = current['humidity']
        wind = current['windspeedKmph']
        
        advice = self.calculate_clothing_advice(temp, condition)
        
        report = f"""
🌤️ 天气穿衣建议 | {self.city} | {datetime.now().strftime('%Y-%m-%d %H:%M')}

📊 天气数据
  温度: {temp}°C (体感 {feels_like}°C)
  天气: {condition}
  湿度: {humidity}%
  风速: {wind} km/h

👕 穿衣建议
  {advice}

💡 小贴士
  • 体感温度 {'高于' if feels_like > temp else '低于' if feels_like < temp else '等于'}实际温度
  • {'有风，注意防风' if int(wind) > 15 else '风力不大'}
  • {'湿度较高' if int(humidity) > 70 else '湿度适中'}
"""
        return report


if __name__ == "__main__":
    advisor = WeatherAdvisor()
    print(advisor.generate_report())
