"""Dyson v2 pure cool devices."""

# pylint: disable=too-many-public-methods,too-many-instance-attributes

import json
from .utils import printable_fields


class DysonPureCoolV2State:
    """Dyson device state."""

    @staticmethod
    def is_state_message(payload):
        """Return true if this message is a Dyson Pure state message."""
        return json.loads(payload)['msg'] in ["CURRENT-STATE", "STATE-CHANGE"]

    @staticmethod
    def _get_field_value(state, field):
        """Get field value."""
        return state[field][1] if isinstance(state[field], list) else state[
            field]

    def __init__(self, payload):
        """Create a new state.

        :param payload: Message payload
        """
        json_message = json.loads(payload)
        self._state = json_message['product-state']
        self._fan_power = self._get_field_value(self._state, 'fpwr')
        self._front_direction = self._get_field_value(self._state, 'fdir')
        self._auto_mode = self._get_field_value(self._state, 'auto')
        self._oscillation_status = self._get_field_value(self._state, 'oscs')
        self._oscillation = self._get_field_value(self._state, 'oson')
        self._night_mode = self._get_field_value(self._state, 'nmod')
        self._continuous_monitoring = self._get_field_value(self._state, 'rhtm')
        self._fan_state = self._get_field_value(self._state, 'fnst')
        self._night_mode_speed = self._get_field_value(self._state, 'nmdv')
        self._speed = self._get_field_value(self._state, 'fnsp')
        self._carbon_filter_state = self._get_field_value(self._state, 'cflr')
        self._hepa_filter_state = self._get_field_value(self._state, 'hflr')
        self._sleep_timer = self._get_field_value(self._state, 'sltm')
        self._oscillation_angle_low = self._get_field_value(self._state, 'osal')
        self._oscillation_angle_high = self._get_field_value(self._state, 'osau')

    @property
    def fan_power(self):
        """Fan on/off."""
        return self._fan_power

    @property
    def front_direction(self):
        """Airflow front/back direction."""
        return self._front_direction

    @property
    def auto_mode(self):
        """Auto mode."""
        return self._auto_mode

    @property
    def oscillation_status(self):
        """Oscillation. Can be IDLE if auto mode is on"""
        return self._oscillation_status

    @property
    def oscillation(self):
        """Oscillation mode."""
        return self._oscillation

    @property
    def night_mode(self):
        """Night mode."""
        return self._night_mode

    @property
    def continuous_monitoring(self):
        """Monitor when inactive (standby)."""
        return self._continuous_monitoring

    @property
    def fan_state(self):
        """Fan state."""
        return self._fan_state

    @property
    def night_mode_speed(self):
        """Night mode fan speed."""
        return self._night_mode_speed

    @property
    def speed(self):
        """Fan speed."""
        return self._speed

    @property
    def carbon_filter_state(self):
        """State of crabon filter in percentage."""
        return self._carbon_filter_state

    @property
    def hepa_filter_state(self):
        """State of crabon filter in percentage."""
        return self._hepa_filter_state

    @property
    def sleep_timer(self):
        """Sleep timer."""
        return self._sleep_timer

    @property
    def oscillation_angle_low(self):
        """Lower oscillation angle."""
        return self._oscillation_angle_low

    @property
    def oscillation_angle_high(self):
        """Higher oscillation angle."""
        return self._oscillation_angle_high

    def __repr__(self):
        """Return a String representation."""
        fields = [("fan_power", self.fan_power),
                  ("front_direction", self.front_direction),
                  ("auto_mode", self.auto_mode),
                  ("oscillation_status", self.oscillation_status),
                  ("oscillation", self.oscillation),
                  ("night_mode", self.night_mode),
                  ("continuous_monitoring", self.continuous_monitoring),
                  ("fan_state", self.fan_state),
                  ("night_mode_speed", self.night_mode_speed),
                  ("speed", self.speed),
                  ("carbon_filter_state", self.carbon_filter_state),
                  ("hepa_filter_state", self.hepa_filter_state),
                  ("sleep_timer", self.sleep_timer),
                  ("oscillation_angle_low", self.oscillation_angle_low),
                  ("oscillation_angle_high", self.oscillation_angle_high)]
        return 'DysonPureCoolV2State(' + ",".join(printable_fields(fields)) + ')'


class DysonEnvironmentalSensorV2State:
    """Environmental sensor state."""

    @staticmethod
    def is_environmental_state_message(payload):
        """Return true if this message is a state message."""
        json_message = json.loads(payload)
        return json_message['msg'] in ["ENVIRONMENTAL-CURRENT-SENSOR-DATA"]

    @staticmethod
    def __get_field_value(state, field):
        """Get field value."""
        return state[field][1] if isinstance(state[field], list) else state[
            field]

    def __init__(self, payload):
        """Create a new Environmental sensor state.

        :param payload: Message payload
        """
        json_message = json.loads(payload)
        data = json_message['data']

        temperature = self.__get_field_value(data, 'tact')
        self._temperature = 0 if temperature == 'OFF' else float(
            temperature) / 10

        humidity = self.__get_field_value(data, 'hact')
        self._humidity = 0 if humidity == 'OFF' else int(humidity)

        self._particulate_matter_25 = int(self.__get_field_value(data, 'pm25'))
        self._particulate_matter_10 = int(self.__get_field_value(data, 'pm10'))

        volatile_organic_compounds = self.__get_field_value(data, 'va10')
        self._volatile_organic_compounds = 0 \
            if volatile_organic_compounds == 'INIT' \
            else int(volatile_organic_compounds)

        self._nitrogen_dioxide = int(self.__get_field_value(data, 'noxl'))

        self._p25r = int(self.__get_field_value(data, 'p25r'))
        self._p10r = int(self.__get_field_value(data, 'p10r'))

        sltm = self.__get_field_value(data, 'sltm')
        self._sleep_timer = 0 if sltm == 'OFF' else int(sltm)

    @property
    def temperature(self):
        """Temperature in Kelvin."""
        return self._temperature

    @property
    def humidity(self):
        """Humidity in percent."""
        return self._humidity

    @property
    def particulate_matter_25(self):
        """particulate matter under 2.5micron."""
        return self._particulate_matter_25

    @property
    def particulate_matter_10(self):
        """particulate matter under 10micron """
        return self._particulate_matter_10

    @property
    def volatile_organic_compounds(self):
        """Volatile organic compounds level."""
        return self._volatile_organic_compounds

    @property
    def nitrogen_dioxide(self):
        """Nitrogen dioxide level."""
        return self._nitrogen_dioxide

    @property
    def p25r(self):
        """Unknown."""
        return self._p25r

    @property
    def p10r(self):
        """Unknown."""
        return self._p10r

    @property
    def sleep_timer(self):
        """Sleep timer."""
        return self._sleep_timer

    def __repr__(self):
        """Return a String representation."""
        fields = [("temperature", str(self.temperature)),
                  ("humidity", str(self.humidity)),
                  ("particulate_matter_25", str(self.particulate_matter_25)),
                  ("particulate_matter_10", str(self.particulate_matter_10)),
                  ("volatile_organic_compounds", str(self.volatile_organic_compounds)),
                  ("nitrogen_dioxide", str(self.nitrogen_dioxide)),
                  ("p25r", str(self.p25r)),
                  ("p10r", str(self.p10r)),
                  ("sleep_timer", str(self.sleep_timer))]
        return 'DysonEnvironmentalSensorV2State(' + ",".join(
            printable_fields(fields)) + ')'