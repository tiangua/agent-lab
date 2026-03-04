"""
Weather check script with clothing recommendations.
Based on 26C dressing rule.
"""

import requests
from datetime import datetime


class WeatherAdvisor:
    """Simple weather-based clothing advisor."""
    
    COMFORT_TEMP = 26  # Comfortable body temperature
    
    def __init__(self, city="Shanghai"):
        self.city = city
    
    def get_weather(self):
        """Get weather from wttr.in (free API)."""
        try:
            url = f"https://wttr.in/{self.city}?format=j1"
            response = requests.get(url, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def clothing_advice(self, temp):
        """Get clothing advice based on temp."""
        diff = self.COMFORT_TEMP - temp
        
        if diff <= 0:
            return "Hot! Short sleeves and shorts OK."
        elif diff <= 3:
            return "Warm. Short sleeves + light jacket."
        elif diff <= 5:
            return "Comfortable. Light sweater + pants."
        elif diff <= 8:
            return "Cool. Sweater + coat."
        elif diff <= 12:
            return "Cold. Down jacket needed."
        else:
            return "Very cold! Thick coat + warm layers."
    
    def report(self):
        """Generate weather report."""
        weather = self.get_weather()
        if not weather:
            return "Failed to get weather data"
        
        current = weather['current_condition'][0]
        temp = float(current['temp_C'])
        feels = float(current['FeelsLikeC'])
        desc = current.get('lang_zh', [{}])[0].get('value') or current['weatherDesc'][0]['value']
        
        advice = self.clothing_advice(temp)
        
        return f"""
Weather Report | {self.city} | {datetime.now().strftime('%Y-%m-%d %H:%M')}

Temperature: {temp}C (feels like {feels}C)
Condition: {desc}

Clothing Advice:
  {advice}
"""


if __name__ == "__main__":
    print(WeatherAdvisor().report())
