"""
    Simple application to help make decisions about the suitability of the
    weather for a planned event. Second assignment for CSSE1001/7030.

    Event: Represents details about an event that may be influenced by weather.
    EventDecider: Determines if predicted weather will impact on a planned event.
    UserInteraction: Simple textual interface to drive program.
"""

__author__ = ""
__email__ = ""

from weather_data import WeatherData
from prediction import WeatherPrediction, YesterdaysWeather, SimplePrediction, SophisticatedPrediction
# Import your SimplePrediction and SophisticatedPrediction classes once defined.


# Define your Event Class here
class Event(object):
    """a class that holds data about a single event and provides access to that data"""
    def __init__(self, name, outdoors, cover_available, time):
        """
        parameter:
         name: a string representing the name of the event
         outdoors: a boolean value representing whether the event outdoors
         cover_available: a boolean value representing whether the event cover available
         time:an integer from 0 up to,but not including 24,indicating the closest hour to the starting time.
        """
        self._name = name
        self._outdoors = outdoors
        self._cover_available = cover_available
        self._time = time

    def get_name(self):
        """(str)return a event name"""
        return self._name
    def get_time(self):
        """(int)return time value """
        return self._time
    def get_outdoors(self):
        """(boolean) return outdoors value"""
        return self._outdoors
    def get_cover_available(self):
        """(boolean) return cover available value"""
        return self._cover_available
    def __str__(self):
        """a string representation of the event"""
        return "Event({} @ {}, {}, {})".format(self._name, self._time, self.get_outdoors(), self._cover_available)


class EventDecision(object):
    """Uses event details to decide if predicted weather suits an event."""

    def __init__(self, event, prediction_model):
        """
        Parameters:
            event (Event): The event to determine its suitability.
            prediction_model (WeatherPrediction): Specific prediction model.
                           An object of a subclass of WeatherPrediction used 
                           to predict the weather for the event.
        """
        self._event = event
        self._prediction_model = prediction_model

    def _temperature_factor(self):
        """Determines how advisable it is to continue with the event based on
        predicted temperature

        Return:
            (float) Temperature Factor
            """

        humidity = self._prediction_model.humidity()
        high_temperature = self._prediction_model.high_temperature()
        low_temperature = self._prediction_model.low_temperature()
        wind_speed = self._prediction_model.wind_speed()
        cloud_cover = self._prediction_model.cloud_cover()
        times = self._event.get_time()
        outdoors = self._event.get_outdoors()
        cover = self._event.get_cover_available()
        temperature_factor = 0
        if humidity > 70:
            humidity_factor = humidity/20
            if humidity_factor > 0:
                high_temperature += humidity_factor
                low_temperature += humidity_factor
            elif humidity_factor < 0:
                high_temperature -= humidity_factor
                low_temperature -= humidity_factor

        if (6 <= times <= 19 and outdoors and high_temperature >= 30) or high_temperature >= 45:
            temperature_factor = high_temperature/(-5) + 6

            if temperature_factor < 0:
                temperature_factor += 1 if cover else 0
                temperature_factor += 1 if 3 < wind_speed < 10 else 0
                temperature_factor += 1 if cloud_cover > 4 else 0

        if (0 <= times <= 5 or 20 <= times <= 23) and low_temperature < 5 and high_temperature <= 45:
            temperature_factor = low_temperature/5 -1.1

        if low_temperature > 15 and high_temperature < 30:
            temperature_factor = (high_temperature -low_temperature)/5

        return temperature_factor





    def _rain_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted rainfall

        Return:
            (float) Rain Factor
        """

        chance_of_rain = self._prediction_model.chance_of_rain()
        if chance_of_rain < 20:
            rain_factor = chance_of_rain/(-5) + 4
        elif chance_of_rain > 50:
            rain_factor = chance_of_rain/(-20) + 1
        else:
            rain_factor = 0

        wind_speed = self._prediction_model.wind_speed()
        if wind_speed < 5 and self._event.get_outdoors() and self._event.get_cover_available():
            rain_factor += 1
        if rain_factor < 2 and wind_speed > 15:
            rain_factor += (wind_speed/(-15))
        if rain_factor < -9:
            rain_factor = -9
        return rain_factor

    def advisability(self):
        """Determine how advisable it is to continue with the planned event.

        Return:
            (float) Value in range of -5 to +5,
                    -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        result = self._temperature_factor() + self._rain_factor()
        if result < -5:
            result = -5
        elif result > 5:
            result = 5

        return result



class UserInteraction(object):
    """Simple textual interface to drive program."""

    def __init__(self):
        """store local reference to the given parameters"""
        self._event = None
        self._prediction_model = None
    def _get_user_answer(self,result = []):
        """
        1.get user's input
        2.write a question_list concluding name, outdoors, cover_available, time questions
        3.use enumerate method to traverse the question_list to get index and input number(i).
        4.return a list of user's input
        """
        question_list = [
            "What is the name of the event?",
            "Is the event outdoors?[Y/N]",
            "Is there covered shelter?[Y/N]",
            "What time is the event?[0~23]"]
        result = []
        for index, i in enumerate(question_list):
            value = input("{}".format(i))
            if index == 0:
                value = value.strip()
            elif index in [1,2]:
                value = True if value.upper() in ("Y", "YES") else False
            else:
                value = int(value.strip())
            result.append(value)
        return result

    def get_event_details(self):
        """Prompt the user to enter details for an event.

        Return:
            (Event): An Event object containing the event details.
        """
        name, outdoors, cover_available, time = self._get_user_answer()
        self._event = Event(name, outdoors, cover_available, time)
        return self._event

    def get_prediction_model(self, weather_data):
        """Prompt the user to select the model for predicting the weather.

        Parameter:
            weather_data (WeatherData): Data used for predicting the weather.

        Return:
            (WeatherPrediction): Object of the selected prediction model.
        """
        print("Select the weather prediction model you wish to use:")
        print("  1) Yesterday's weather.")
        print("  2) Simple prediction.")
        print("  3) Sophisticated prediction.")
        model_choice = input("> ")
        # Error handling can be added to this method.
        if model_choice == '1' :
            self._prediction_model = YesterdaysWeather(weather_data)
        elif model_choice == '2':
            days = input('Enter how many days of data you wish to use for making the prediction:')
            self._prediction_model = SimplePrediction(weather_data, int(days.strip()))
        elif model_choice == '3':
            days = input('Enter how many days of data you wish to use for making the prediction:')
            self._prediction_model = SophisticatedPrediction(weather_data, int(days.strip()))
        else:
            print('error select, please input integer in 1~3')
            return self.get_prediction_model(weather_data)
        # Cater for other prediction models when they are implemented.
        return self._prediction_model

    def output_advisability(self, impact):
        """Output how advisable it is to go ahead with the event.

        Parameter:
            impact (float): Impact of the weather on the event.
                            -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        # The following print statement is an example of printing out the
        # class name of an object, which you may use for making the
        # advisability output more meaningful.

        print("based on the", type(self._prediction_model).__name__, "model","the advisability of holding" ,self._event.get_name(), "is" ,impact,)


    def another_check(self):
        """Ask user if they want to check using another prediction model.

        Return:
            (bool): True if user wants to check using another prediction model.
        """
        user_choice = input("would you like to check again? ").strip()
        return True if user_choice.upper() in ["Y", "YES"] else False


def main():
    """Main application's starting point."""
    check_again = True
    weather_data = WeatherData()# collection of weather data
    weather_data.load("weather_data.csv") # load weather data
    user_interface = UserInteraction() # prepare user interface

    # starting user interface, get the event(name,time,outdoors,cover_avalable)
    print("Let's determine how suitable your event is for the predicted weather.")
    event = user_interface.get_event_details()

    while check_again:# use the while loop to predict,when a kind of prediction model finished,ask if enter the next prediction
        prediction_model = user_interface.get_prediction_model(weather_data)# user choose one of prediction models
        decision = EventDecision(event, prediction_model)#combine the event and chosen modle
        impact = decision.advisability() #  use impact class to outcome the impact
        user_interface.output_advisability(impact) #return the impact outcome to user
        check_again = user_interface.another_check() #ask for user  whether would like to check again


if __name__ == "__main__":
    main()
