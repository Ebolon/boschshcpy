from enum import Enum

from .device_service import SHCDeviceService


class TemperatureLevelService(SHCDeviceService):
    @property
    def temperature(self) -> float:
        return float(self.state["temperature"])

    def summary(self):
        super().summary()
        print(f"    Temperature              : {self.temperature}")


class HumidityLevelService(SHCDeviceService):
    @property
    def humidity(self) -> float:
        return float(self.state["humidity"])

    def summary(self):
        super().summary()
        print(f"    Humidity              : {self.humidity}")


class RoomClimateControlService(SHCDeviceService):
    class OperationMode(Enum):
        AUTOMATIC = "AUTOMATIC"
        MANUAL = "MANUAL"

    @property
    def operation_mode(self) -> OperationMode:
        return self.OperationMode(self.state["operationMode"])

    @operation_mode.setter
    def operation_mode(self, value: OperationMode):
        self.put_state_element("operationMode", value.value)

    @property
    def setpoint_temperature(self) -> float:
        return float(self.state["setpointTemperature"])

    @setpoint_temperature.setter
    def setpoint_temperature(self, value: float):
        self.put_state_element("setpointTemperature", value)

    @property
    def setpoint_temperature_eco(self) -> float:
        return float(self.state["setpointTemperatureForLevelEco"])

    @property
    def setpoint_temperature_comfort(self) -> float:
        return float(self.state["setpointTemperatureForLevelComfort"])

    @property
    def ventilation_mode(self) -> bool:
        return self.state["ventilationMode"]

    @property
    def low(self) -> bool:
        return self.state["low"]

    @low.setter
    def low(self, value: bool):
        self.put_state_element("low", value)

    @property
    def boost_mode(self) -> bool:
        return self.state["boostMode"]

    @boost_mode.setter
    def boost_mode(self, value: bool):
        self.put_state_element("boostMode", value)

    @property
    def summer_mode(self) -> bool:
        return self.state["summerMode"]

    @property
    def supports_boost_mode(self) -> bool:
        return self.state["supportsBoostMode"]

    @property
    def show_setpoint_temperature(self) -> bool:
        if "showSetpointTemperature" in self.state.keys():
            return self.state["showSetpointTemperature"]
        else:
            return False

    def summary(self):
        super().summary()
        print(f"    Operation Mode           : {self.operation_mode}")
        print(f"    Setpoint Temperature     : {self.setpoint_temperature}")
        print(f"    Setpoint Temperature ECO : {self.setpoint_temperature_eco}")
        print(f"    Setpoint Temperature CMF : {self.setpoint_temperature_comfort}")
        print(f"    Ventilation Mode         : {self.ventilation_mode}")
        print(f"    Low                      : {self.low}")
        print(f"    Boost Mode               : {self.boost_mode}")
        print(f"    Summer Mode              : {self.summer_mode}")
        print(f"    Supports Boost Mode      : {self.supports_boost_mode}")
        print(f"    Show Setpoint Temperature: {self.show_setpoint_temperature}")


class ShutterContactService(SHCDeviceService):
    class State(Enum):
        CLOSED = "CLOSED"
        OPEN = "OPEN"

    @property
    def value(self) -> State:
        return self.State(self.state["value"])

    def summary(self):
        super().summary()
        print(f"    Value                    : {self.value}")


class ValveTappetService(SHCDeviceService):
    @property
    def position(self) -> int:
        return int(self.state["position"])

    def summary(self):
        super().summary()
        print(f"    Position                 : {self.position}")


class PowerSwitchService(SHCDeviceService):
    class State(Enum):
        ON = "ON"
        OFF = "OFF"

    @property
    def value(self) -> State:
        return self.State(self.state["switchState"])

    @property
    def powerofftime(self) -> int:
        return int(self.state["automaticPowerOffTime"])

    def summary(self):
        super().summary()
        print(f"    switchState              : {self.value}")
        print(f"    automaticPowerOffTime    : {self.powerofftime}")


class PowerMeterService(SHCDeviceService):
    @property
    def powerconsumption(self) -> float:
        return float(self.state["powerConsumption"])

    @property
    def energyconsumption(self) -> float:
        return float(self.state["energyConsumption"])

    def summary(self):
        super().summary()
        print(f"    powerConsumption         : {self.powerconsumption}")
        print(f"    energyConsumption        : {self.energyconsumption}")


class RoutingService(SHCDeviceService):
    class State(Enum):
        ENABLED = "ENABLED"
        DISABLED = "DISABLED"

    @property
    def value(self) -> State:
        return self.State(self.state["value"])

    def summary(self):
        super().summary()
        print(f"    value                    : {self.value}")


class PowerSwitchProgramService(SHCDeviceService):
    class State(Enum):
        MANUAL = "MANUAL"
        AUTOMATIC = "AUTOMATIC"

    @property
    def value(self) -> State:
        return self.State(self.state["operationMode"])

    def summary(self):
        super().summary()
        print(f"    operationMode            : {self.value}")


class BinarySwitchService(SHCDeviceService):
    @property
    def value(self) -> bool:
        return self.state["on"]

    def summary(self):
        super().summary()
        print(f"    switchState              : {self.value}")


class SmokeDetectorCheckService(SHCDeviceService):
    class State(Enum):
        NONE = "NONE"
        SMOKE_TEST_OK = "SMOKE_TEST_OK"
        SMOKE_TEST_REQUESTED = "SMOKE_TEST_REQUESTED"

    @property
    def value(self) -> State:
        return self.State(self.state["value"])

    def summary(self):
        super().summary()
        print(f"    smokeDetectorCheckState  : {self.value}")


class AlarmService(SHCDeviceService):
    class State(Enum):
        IDLE_OFF = "IDLE_OFF"
        INTRUSION_ALARM = "INTRUSION_ALARM"
        SECONDARY_ALARM = "SECONDARY_ALARM"
        PRIMARY_ALARM = "PRIMARY_ALARM"

    @property
    def value(self) -> State:
        return self.State(self.state["value"])

    def summary(self):
        super().summary()
        print(f"    alarmState               : {self.value}")


class ShutterControlService(SHCDeviceService):
    class State(Enum):
        STOPPED = "STOPPED"
        MOVING = "MOVING"
        CALIBRATING = "CALIBRATING"
        OPENING = "OPENING"
        CLOSING = "CLOSING"

    def __init__(self, api, raw_device_service):
        super().__init__(api=api, raw_device_service=raw_device_service)
        self._current_level = self.state["level"]
        self._last_level = self.state["level"]

    @property
    def value(self) -> State:
        if self._current_level != self.level:
            self._last_level = self._current_level
            self._current_level = self.level
        if self.state["operationState"] == "MOVING" and self.level < self._last_level:
            return self.State("CLOSING")
        elif self.state["operationState"] == "MOVING" and self.level > self._last_level:
            return self.State("OPENING")
        else:
            return self.State(self.state["operationState"])

    @property
    def calibrated(self) -> bool:
        return self.state["calibrated"]

    @property
    def level(self) -> float:
        return self.state["level"]

    def summary(self):
        super().summary()
        print(f"    operationState           : {self.value}")
        print(f"    Level                    : {self.level}")
        print(f"    Calibrated               : {self.calibrated}")


class CameraLightService(SHCDeviceService):
    class State(Enum):
        ON = "ON"
        OFF = "OFF"
        NONE = "NONE"

    @property
    def value(self) -> State:
        return self.State(self.state["value"] if "value" in self.state else "NONE")

    def summary(self):
        super().summary()
        print(f"    value                    : {self.value}")


class PrivacyModeService(SHCDeviceService):
    class State(Enum):
        ENABLED = "ENABLED"
        DISABLED = "DISABLED"

    @property
    def value(self) -> State:
        return self.State(self.state["value"])

    def summary(self):
        super().summary()
        print(f"    value                    : {self.value}")


class CameraNotificationService(SHCDeviceService):
    class State(Enum):
        ENABLED = "ENABLED"
        DISABLED = "DISABLED"

    @property
    def value(self) -> State:
        return self.State(self.state["value"])

    def summary(self):
        super().summary()
        print(f"    value                    : {self.value}")


class IntrusionDetectionControlService(SHCDeviceService):
    class State(Enum):
        SYSTEM_DISARMED = "SYSTEM_DISARMED"
        SYSTEM_ARMING = "SYSTEM_ARMING"
        SYSTEM_ARMED = "SYSTEM_ARMED"
        MUTE_ALARM = "MUTE_ALARM"

    @property
    def value(self) -> State:
        return self.State(self.state["value"])

    @property
    def armActivationDelayTime(self) -> int:
        return self.state["armActivationDelayTime"]

    @property
    def alarmActivationDelayTime(self) -> int:
        return self.state["alarmActivationDelayTime"]

    def summary(self):
        super().summary()
        print(f"    value                    : {self.value}")
        print(f"    armActivationDelayTime   : {self.armActivationDelayTime}")
        print(f"    alarmActivationDelayTime : {self.alarmActivationDelayTime}")


class KeypadService(SHCDeviceService):
    class KeyState(Enum):
        LOWER_BUTTON = "LOWER_BUTTON"
        UPPER_BUTTON = "UPPER_BUTTON"

    class KeyEvent(Enum):
        PRESS_SHORT = "PRESS_SHORT"
        PRESS_LONG = "PRESS_LONG"

    @property
    def keyCode(self) -> int:
        return self.state["keyCode"]

    @property
    def keyName(self) -> KeyState:
        return self.KeyState(self.state["keyName"])

    @property
    def eventType(self) -> KeyEvent:
        return self.KeyEvent(self.state["eventType"])

    @property
    def eventTimestamp(self) -> int:
        return self.state["eventTimestamp"]

    def summary(self):
        super().summary()
        print(f"    keyCode                  : {self.keyCode}")
        print(f"    keyName                  : {self.keyName}")
        print(f"    eventType                : {self.eventType}")
        print(f"    eventTimestamp           : {self.eventTimestamp}")


class LatestMotionService(SHCDeviceService):
    @property
    def latestMotionDetected(self) -> str:
        return self.state["latestMotionDetected"]

    def summary(self):
        super().summary()
        print(f"    latestMotionDetected     : {self.latestMotionDetected}")


class AirQualityLevelService(SHCDeviceService):
    class RatingState(Enum):
        GOOD = "GOOD"
        MEDIUM = "MEDIUM"
        BAD = "BAD"

    @property
    def combinedRating(self) -> RatingState:
        return self.RatingState(self.state["combinedRating"])

    @property
    def description(self) -> str:
        return self.state["description"]

    @property
    def temperature(self) -> int:
        return self.state["temperature"]

    @property
    def temperatureRating(self) -> RatingState:
        return self.RatingState(self.state["temperatureRating"])

    @property
    def humidity(self) -> int:
        return self.state["humidity"]

    @property
    def humidityRating(self) -> RatingState:
        return self.RatingState(self.state["humidityRating"])

    @property
    def purity(self) -> int:
        return self.state["purity"]

    @property
    def purityRating(self) -> str:
        return self.state["purityRating"]

    def summary(self):
        super().summary()
        print(f"    combinedRating           : {self.combinedRating}")
        print(f"    description              : {self.description}")
        print(f"    temperature              : {self.temperature}")
        print(f"    temperatureRating        : {self.temperatureRating}")
        print(f"    humidity                 : {self.humidity}")
        print(f"    humidityRating           : {self.humidityRating}")
        print(f"    purity                   : {self.purity}")
        print(f"    purityRating             : {self.purityRating}")


class SurveillanceAlarmService(SHCDeviceService):
    class SurveillanceAlarmState(Enum):
        ALARM_OFF = "ALARM_OFF"

    @property
    def value(self) -> SurveillanceAlarmState:
        return self.SurveillanceAlarmState(self.state["value"])

    def summary(self):
        super().summary()
        print(f"    value                    : {self.value}")


class SmokeDetectionControlService(SHCDeviceService):
    def summary(self):
        super().summary()
        print(f"    not yet implemented!")


class BatteryLevelService(SHCDeviceService):
    class State(Enum):
        LOW_BATTERY = "LOW_BATTERY"
        CRITICAL_LOW = "CRITICAL_LOW"
        OK = "OK"

    @property
    def warningLevel(self) -> State:
        faults = (
            self._raw_device_service["faults"]
            if "faults" in self._raw_device_service
            else None
        )
        if not faults:
            return self.State("OK")
        assert len(faults["entries"]) == 1
        assert "type" in faults["entries"][0]
        return self.State(faults["entries"][0]["type"])

    def summary(self):
        super().summary()
        print(f"    warningLevel             : {self.warningLevel}")


class ThermostatService(SHCDeviceService):
    class State(Enum):
        ON = "ON"
        OFF = "OFF"

    @property
    def value(self) -> State:
        return self.State(self.state["childLock"])

    def summary(self):
        super().summary()
        print(f"    childLock                : {self.value}")


SERVICE_MAPPING = {
    "TemperatureLevel": TemperatureLevelService,
    "HumidityLevel": HumidityLevelService,
    "RoomClimateControl": RoomClimateControlService,
    "ShutterContact": ShutterContactService,
    "ValveTappet": ValveTappetService,
    "PowerSwitch": PowerSwitchService,
    "PowerMeter": PowerMeterService,
    "Routing": RoutingService,
    "PowerSwitchProgram": PowerSwitchProgramService,
    "BinarySwitch": BinarySwitchService,
    "SmokeDetectorCheck": SmokeDetectorCheckService,
    "Alarm": AlarmService,
    "ShutterControl": ShutterControlService,
    "CameraLight": CameraLightService,
    "PrivacyMode": PrivacyModeService,
    "CameraNotification": CameraNotificationService,
    "IntrusionDetectionControl": IntrusionDetectionControlService,
    "Keypad": KeypadService,
    "LatestMotion": LatestMotionService,
    "AirQualityLevel": AirQualityLevelService,
    "SurveillanceAlarm": SurveillanceAlarmService,
    "BatteryLevel": BatteryLevelService,
    "Thermostat": ThermostatService,
}

#    "SmokeDetectionControl": SmokeDetectionControlService,

SUPPORTED_DEVICE_SERVICE_IDS = SERVICE_MAPPING.keys()


def build(api, raw_device_service):
    device_service_id = raw_device_service["id"]
    assert (
        device_service_id in SUPPORTED_DEVICE_SERVICE_IDS
    ), "Device service is supported"
    return SERVICE_MAPPING[device_service_id](
        api=api, raw_device_service=raw_device_service
    )
