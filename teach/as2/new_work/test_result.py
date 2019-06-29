Python 3.7.2 (tags/v3.7.2:9a3ffc0492, Dec 23 2018, 23:09:28) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> 
===== RESTART: C:\Users\Lenovo\Desktop\simple test new\test_a2_sample.py =====
/------------------------------------------------------------------------------\
|                              Summary of Results                              |
\------------------------------------------------------------------------------/
TestDesign
    + 1. test SimplePrediction class and methods defined correctly
    + 2. test Event class and methods defined correctly
    + 3. test EventDecision class and methods defined correctly
    - 4. test SophisticatedPrediction class and methods defined correctly
    + 5. test UserInteraction class and methods defined correctly
    + 6. test prediction and event_decision don't print on import
    - 7. test all classes and methods have documentation strings
TestFunctionality
    - 1. test SimplePrediction
    - 2. test Event
    ? 3. test EventDecision
    - 4. test SophisticatedPrediction
TestHighTempEdgeCases
    - 1. Test SimplePrediction with high temp, little rain, low humidity
    - 2. Test SophisticatedPrediction with high temp and high pressure
    - 3. Test SophisticatedPrediction with high temp and equal pressure
    - 4. Test SophisticatedPrediction with high temp and low pressure
TestEventDecisionEdgeCases
    - 1. Test ED._temp_factor rule 2a and _rain_factor rule 1a & 2a
    - 2. Test ED._temp_factor rule 2d and _rain_factor rule 1c
    - 3. Test ED._temp_factor rule 1 & 2a and _rain_factor rule 1c
    - 4. Test ED._temp_factor rule 2a & 3a and _rain_factor rule 1c
TestUserInterface
    - 1. test get event details
    + 2. test get prediction model
TestNoPrint
    + check for no unexpected prints
--------------------------------------------------------------------------------
/------------------------------------------------------------------------------\
|                             Failed/Skipped Tests                             |
\------------------------------------------------------------------------------/
================================================================================
FAIL: TestDesign 4. test SophisticatedPrediction class and methods defined correctly
--------------------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_a2_sample.py", line 136, in test_sophisticated_prediction_defined
        self.aggregate_tests()
    AssertionError: 
        2 != 3 : '__init__' does not have the correct number of parameters, expected 3 found 2

================================================================================
FAIL: TestDesign 7. test all classes and methods have documentation strings
--------------------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_a2_sample.py", line 181, in test_doc_strings
        self.aggregate_tests()
    AssertionError: 
        Documentation string is required for 'SimplePrediction'
        Documentation string is required for 'SophisticatedPrediction'
        Documentation string is required for 'SophisticatedPrediction.chance_of_rain'
        Documentation string is required for 'SophisticatedPrediction.cloud_cover'
        Documentation string is required for 'SophisticatedPrediction.get_number_days'
        Documentation string is required for 'SophisticatedPrediction.high_temperature'
        Documentation string is required for 'SophisticatedPrediction.humidity'
        Documentation string is required for 'SophisticatedPrediction.low_temperature'
        Documentation string is required for 'SophisticatedPrediction.wind_speed'
        Documentation string is required for 'Event'
        Documentation string is required for 'Event.__str__'
        Documentation string is required for 'Event.get_cover_available'
        Documentation string is required for 'Event.get_name'
        Documentation string is required for 'Event.get_outdoors'
        Documentation string is required for 'Event.get_time'
        Documentation string is required for 'UserInteraction.__init__'

================================================================================
ERROR: TestFunctionality 1. test SimplePrediction
--------------------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_a2_sample.py", line 188, in test_simple_prediction
        sp = self.prediction.SimplePrediction(self.data, 4)
      File "prediction.py", line 132, in __init__
        self.days = self._weather_data.size if self.days > self._weather_data.size else days
    AttributeError: 'SimplePrediction' object has no attribute 'days'

================================================================================
ERROR: TestFunctionality 2. test Event
--------------------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_a2_sample.py", line 205, in test_event
        self.aggregate(self.assertEqual, event.get_name(), 'My Event', tag='get_name')
      File "event_decision.py", line 34, in get_name
        return self._name()
    TypeError: 'str' object is not callable

================================================================================
SKIP: TestFunctionality 3. test EventDecision
--------------------------------------------------------------------------------
    Skipped due to failing/skipping TestFunctionality.test_simple_prediction

================================================================================
ERROR: TestFunctionality 4. test SophisticatedPrediction
--------------------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_a2_sample.py", line 231, in test_sophisticated_prediction
        sp = self.prediction.SophisticatedPrediction(self.data, 10)
    TypeError: __init__() takes 2 positional arguments but 3 were given

================================================================================
ERROR: TestHighTempEdgeCases 1. Test SimplePrediction with high temp, little rain, low humidity
--------------------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_a2_sample.py", line 262, in test_simple_prediction
        len(TestHighTempEdgeCases.weather_data._weather_data))
      File "prediction.py", line 132, in __init__
        self.days = self._weather_data.size if self.days > self._weather_data.size else days
    AttributeError: 'SimplePrediction' object has no attribute 'days'

================================================================================
ERROR: TestHighTempEdgeCases 2. Test SophisticatedPrediction with high temp and high pressure
--------------------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_a2_sample.py", line 281, in test_sophisticated_prediction_high_pressure
        len(TestHighTempEdgeCases.weather_data._weather_data))
    TypeError: __init__() takes 2 positional arguments but 3 were given

================================================================================
ERROR: TestHighTempEdgeCases 3. Test SophisticatedPrediction with high temp and equal pressure
--------------------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_a2_sample.py", line 300, in test_sophisticated_prediction_equal_pressure
        len(TestHighTempEdgeCases.weather_data._weather_data))
    TypeError: __init__() takes 2 positional arguments but 3 were given

================================================================================
ERROR: TestHighTempEdgeCases 4. Test SophisticatedPrediction with high temp and low pressure
--------------------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_a2_sample.py", line 319, in test_sophisticated_prediction_low_pressure
        len(TestHighTempEdgeCases.weather_data._weather_data))
    TypeError: __init__() takes 2 positional arguments but 3 were given

================================================================================
ERROR: TestEventDecisionEdgeCases 1. Test ED._temp_factor rule 2a and _rain_factor rule 1a & 2a
--------------------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_a2_sample.py", line 340, in test_event_decision1
        sp = self.prediction.SimplePrediction(weather_data, 1)
      File "prediction.py", line 132, in __init__
        self.days = self._weather_data.size if self.days > self._weather_data.size else days
    AttributeError: 'SimplePrediction' object has no attribute 'days'

================================================================================
ERROR: TestEventDecisionEdgeCases 2. Test ED._temp_factor rule 2d and _rain_factor rule 1c
--------------------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_a2_sample.py", line 356, in test_event_decision2
        sp = self.prediction.SimplePrediction(weather_data, 1)
      File "prediction.py", line 132, in __init__
        self.days = self._weather_data.size if self.days > self._weather_data.size else days
    AttributeError: 'SimplePrediction' object has no attribute 'days'

================================================================================
ERROR: TestEventDecisionEdgeCases 3. Test ED._temp_factor rule 1 & 2a and _rain_factor rule 1c
--------------------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_a2_sample.py", line 372, in test_event_decision3
        sp = self.prediction.SimplePrediction(weather_data, 1)
      File "prediction.py", line 132, in __init__
        self.days = self._weather_data.size if self.days > self._weather_data.size else days
    AttributeError: 'SimplePrediction' object has no attribute 'days'

================================================================================
ERROR: TestEventDecisionEdgeCases 4. Test ED._temp_factor rule 2a & 3a and _rain_factor rule 1c
--------------------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_a2_sample.py", line 388, in test_event_decision4
        sp = self.prediction.SimplePrediction(weather_data, 1)
      File "prediction.py", line 132, in __init__
        self.days = self._weather_data.size if self.days > self._weather_data.size else days
    AttributeError: 'SimplePrediction' object has no attribute 'days'

================================================================================
ERROR: TestUserInterface 1. test get event details
--------------------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_a2_sample.py", line 406, in test_get_event_details
        event = ui.get_event_details()
      File "event_decision.py", line 187, in get_event_details
        name, outdoors, cover_available, time = self._get_user_answer()
    ValueError: too many values to unpack (expected 4)

--------------------------------------------------------------------------------
Ran 22 tests in 0.033 seconds with 7 passed/1 skipped/14 failed.
>>> 
