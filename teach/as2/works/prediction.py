"""
    Prediction model classes used in the second assignment for CSSE1001/7030.

    WeatherPrediction: Defines the super class for all weather prediction models.
    YesterdaysWeather: Predict weather to be similar to yesterday's weather.
"""

__author__ = ""
__email__ = ""

from weather_data import WeatherData


class WeatherPrediction(object):
    """Superclass for all of the different weather prediction models."""

    def __init__(self, weather_data):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        self._weather_data = weather_data

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        raise NotImplementedError

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        raise NotImplementedError

    def high_temperature(self):
        """(float) Expected high temperature."""
        raise NotImplementedError

    def low_temperature(self):
        """(float) Expected low temperature."""
        raise NotImplementedError

    def humidity(self):
        """(int) Expected humidity."""
        raise NotImplementedError

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        raise NotImplementedError

    def wind_speed(self):
        """(int) Expected average wind speed."""
        raise NotImplementedError


class YesterdaysWeather(WeatherPrediction):
    """Simple prediction model, based on yesterday's weather."""

    def __init__(self, weather_data):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)
        self._yesterdays_weather = self._weather_data.get_data(1)
        self._yesterdays_weather = self._yesterdays_weather[0]

    def get_number_days(self):
        """(int) Number of days of data being used in prediction"""
        return 1

    def chance_of_rain(self):
        """(int) Percentage indicating chance of rain occurring."""
        # Amount of yesterday's rain indicating chance of it occurring.
        NO_RAIN = 0.1
        LITTLE_RAIN = 3
        SOME_RAIN = 8
        # Chance of rain occurring.
        NONE = 0
        MILD = 40
        PROBABLE = 75
        LIKELY = 90

        if self._yesterdays_weather.get_rainfall() < NO_RAIN:
            chance_of_rain = NONE
        elif self._yesterdays_weather.get_rainfall() < LITTLE_RAIN:
            chance_of_rain = MILD
        elif self._yesterdays_weather.get_rainfall() < SOME_RAIN:
            chance_of_rain = PROBABLE
        else:
            chance_of_rain = LIKELY

        return chance_of_rain

    def high_temperature(self):
        """(float) Expected high temperature."""
        return self._yesterdays_weather.get_high_temperature()

    def low_temperature(self):
        """(float) Expected low temperature."""
        return self._yesterdays_weather.get_low_temperature()

    def humidity(self):
        """(int) Expected humidity."""
        return self._yesterdays_weather.get_humidity()

    def wind_speed(self):
        """(int) Expected average wind speed."""
        return self._yesterdays_weather.get_average_wind_speed()

    def cloud_cover(self):
        """(int) Expected amount of cloud cover."""
        return self._yesterdays_weather.get_cloud_cover()


# Your implementations of the SimplePrediction and SophisticatedPrediction
# classes should go here.

class SimplePrediction(WeatherPrediction):
    """ pass """
    
    def __init__(self,weather_data,days):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.
            days (int): Days of data to use for making the prediction.

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)       
        self.days = self._weather_data.size() if days > self._weather_data.size() else days
        self._weather_data = self._weather_data.get_data(self.days)
        
    def get_number_days(self):
        """(int)number of days being used in predaction"""
        return self.days
    
    def chance_of_rain(self):
        """(int)percentage indacating chance of rain occuring"""
        result = sum([i.get_rainfall() for i in self._weather_data])/self.days * 9
        return 100 if result > 100 else round(result)

    def high_temperature(self):
        """(float)expected high temperature"""
        return max([i.get_high_temperature() for i in self._weather_data])

    def low_temperature(self):
        """(float)expected low temperature"""
        return min([i.get_low_temperature() for i in self._weather_data])

    def humidity(self):
        """(int)expected humidity"""
        return round(sum([i.get_humidity() for i in self._weather_data])/self.days)

    def cloud_cover(self):
        """(int)expected cloud cover"""
        return round(sum([i.get_cloud_cover() for i in self._weather_data])/self.days)

    def wind_speed(self):
        """(int)expected wind speed"""
        return round(sum([i.get_average_wind_speed() for i in self._weather_data])/self.days)


class SophisticatedPrediction(WeatherPrediction):
    """ pass """
    def __init__(self,weather_data, days):
        """
        Parameters:
            weather_data (WeatherData): Collection of weather data.
            days(int): Days of data to use for making the prediction.

        Pre-condition:
            weather_data.size() > 0
        """
        super().__init__(weather_data)
        self.days = self._weather_data.size() if days > self._weather_data.size() else days
        self._weather_data = self._weather_data.get_data(self.days)
        self.yesterday_air_pressure = self._weather_data[-1].get_air_pressure()
        self.average_air_pressure = sum([i.get_air_pressure() for i in self._weather_data])/self.days
        self.yesterday_wind_direction = self._weather_data[-1].get_wind_direction()
        self.yesterday_maximum_wind_speed = self._weather_data[-1].get_maximum_wind_speed()

    def get_number_days(self):
        """(int)number of days being used in predaction"""
        return self.days

    def chance_of_rain(self):
        """(int)percentage indacating chance of rain occuring"""
        average_rainfall = sum([i.get_rainfall() for i in self._weather_data])/self.days
        if self.yesterday_air_pressure < self.average_air_pressure:
            average_rainfall = average_rainfall * 10
        elif self.yesterday_air_pressure >= self.average_air_pressure:
            average_rainfall = average_rainfall * 7
        
        if 'E' in self.yesterday_wind_direction:
            average_rainfall = average_rainfall * 1.2
        
        if average_rainfall > 100:
            average_rainfall = 100
        
        return round(average_rainfall)

    def high_temperature(self):
        """(float)expected high temperature"""
        average_high_temperature = sum([i.get_high_temperature() for i in self._weather_data])/self.days
        if self.yesterday_air_pressure > self.average_air_pressure:
            average_high_temperature += 2
        return average_high_temperature
    
    def low_temperature(self):
        """(float)expected low temperature"""
        average_low_temperature = sum([i.get_low_temperature() for i in self._weather_data])/self.days
        if self.yesterday_air_pressure < self.average_air_pressure:
            average_low_temperature -= 2
        return average_low_temperature
    
    def humidity(self):
        """(int)expected humidity"""
        average_humidity = sum([i.get_humidity() for i in self._weather_data])/self.days
        if self.yesterday_air_pressure < self.average_air_pressure:
            average_humidity += 15
        elif self.yesterday_air_pressure > self.average_air_pressure:
            average_humidity -= 15
        if average_humidity < 0:
            average_humidity = 0
        elif average_humidity > 100:
            average_humidity = 100
        return round(average_humidity)
    
    def cloud_cover(self):
        """(int)expected cloud cover"""
        average_cloud_cover = sum([i.get_cloud_cover() for i in self._weather_data])/self.days
        if self.yesterday_air_pressure < self.average_air_pressure:
            average_cloud_cover += 2
        if average_cloud_cover > 9:
            average_cloud_cover = 9
        return  round(average_cloud_cover)
    
    def wind_speed(self):
        """(int)expected wind speed"""
        average_wind_speed = sum([i.get_average_wind_speed() for i in self._weather_data])/self.days
        # self._weather_data[-3] indacated yesterday wind speed
        if self.yesterday_maximum_wind_speed > 4 * average_wind_speed:
            average_wind_speed *= 1.2
        return  round(average_wind_speed)


if __name__ == "__main__":
    print("This module provides the weather prediction models",
          "and is not meant to be executed on its own.")
