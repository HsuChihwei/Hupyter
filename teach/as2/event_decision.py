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
from prediction import WeatherPrediction, YesterdaysWeather
# Import your SimplePrediction and SophisticatedPrediction classes once defined.


# Define your Event Class here
class Event(object):
    pass


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
        raise NotImplementedError

    def _temperature_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted temperature

        Return:
            (float) Temperature Factor
        """
        raise NotImplementedError

    def _rain_factor(self):
        """
        Determines how advisable it is to continue with the event based on
        predicted rainfall

        Return:
            (float) Rain Factor
        """
        raise NotImplementedError

    def advisability(self):
        """Determine how advisable it is to continue with the planned event.

        Return:
            (float) Value in range of -5 to +5,
                    -5 is very bad, 0 is neutral, 5 is very beneficial
        """
        raise NotImplementedError


class UserInteraction(object):
    """Simple textual interface to drive program."""

    def __init__(self):
        """
        """
        self._event = None
        self._prediction_model = None

    def get_event_details(self):
        """Prompt the user to enter details for an event.

        Return:
            (Event): An Event object containing the event details.
        """
        raise NotImplementedError

    def get_prediction_model(self, weather_data):
        """Prompt the user to select the model for predicting the weather.

        Parameter:
            weather_data (WeatherData): Data used for predicting the weather.

        Return:
            (WeatherPrediction): Object of the selected prediction model.
        """
        print("Select the weather prediction model you wish to use:")
        print("  1) Yesterday's weather.")
        model_choice = input("> ")
        # Error handling can be added to this method.
        if model_choice == '1' :
            self._prediction_model = YesterdaysWeather(weather_data)
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
        print("based on", type(self._prediction_model).__name__, "model")
        raise NotImplementedError

    def another_check(self):
        """Ask user if they want to check using another prediction model.

        Return:
            (bool): True if user wants to check using another prediction model.
        """
        raise NotImplementedError


def main():
    """Main application's starting point."""
    check_again = True
    weather_data = WeatherData()
    weather_data.load("weather_data.csv")
    user_interface = UserInteraction()

    print("Let's determine how suitable your event is for the predicted weather.")
    event = user_interface.get_event_details()

    while check_again:
        prediction_model = user_interface.get_prediction_model(weather_data)
        decision = EventDecision(event, prediction_model)
        impact = decision.advisability()
        user_interface.output_advisability(impact)
        check_again = user_interface.another_check()


if __name__ == "__main__":
    main()
