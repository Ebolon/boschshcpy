from enum import Enum

from .device import SHCDevice
from .services_impl import (
    BatteryLevelService,
    CameraLightService,
    HumidityLevelService,
    IntrusionDetectionControlService,
    ShutterContactService,
    ShutterControlService,
    TemperatureLevelService,
    ValveTappetService,
)


class SHCBatteryDevice(SHCDevice):
    from .services_impl import BatteryLevelService

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)
        self._batterylevel_service = self.device_service("BatteryLevel")

    @property
    def batterylevel(self) -> BatteryLevelService.State:
        return self._batterylevel_service.warningLevel

    def update(self):
        self._batterylevel_service.short_poll()


class SHCSmokeDetector(SHCBatteryDevice):
    from .services_impl import AlarmService, SmokeDetectorCheckService

    class AlarmState(Enum):
        INTRUSION_ALARM_ON_REQUESTED = "INTRUSION_ALARM_ON_REQUESTED"
        INTRUSION_ALARM_OFF_REQUESTED = "INTRUSION_ALARM_OFF_REQUESTED"
        MUTE_SECONDARY_ALARM_REQUESTED = "MUTE_SECONDARY_ALARM_REQUESTED"

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)

        self._alarm_service: AlarmService = self.device_service("Alarm")
        self._smokedetectorcheck_service: SmokeDetectorCheckService = self.device_service(
            "SmokeDetectorCheck"
        )

    @property
    def alarmstate(self) -> AlarmService.State:
        return self._alarm_service.value

    @alarmstate.setter
    def alarmstate(self, state: AlarmState):
        self._alarm_service.put_state_element("state", state.name)

    @property
    def smokedetectorcheck_state(self) -> SmokeDetectorCheckService.State:
        return self._smokedetectorcheck_service.value

    def smoketest_requested(self):
        self._smokedetectorcheck_service.put_state_element(
            "value", "SMOKE_TEST_REQUESTED"
        )

    def update(self):
        self._alarm_service.short_poll()
        self._smokedetectorcheck_service.short_poll()
        super().update()

    def summary(self):
        print(f"SD SmokeDetector:")
        super().summary()


class SHCSmartPlug(SHCDevice):
    from .services_impl import (
        PowerSwitchService,
        PowerMeterService,
        PowerSwitchProgramService,
    )

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)

        self._powerswitch_service = self.device_service("PowerSwitch")
        self._powerswitchprogram_service = self.device_service("PowerSwitchProgram")
        self._powermeter_service = self.device_service("PowerMeter")

    @property
    def state(self) -> PowerSwitchService.State:
        return self._powerswitch_service.value

    @state.setter
    def state(self, state: bool):
        self._powerswitch_service.put_state_element(
            "switchState", "ON" if state else "OFF"
        )

    @property
    def energyconsumption(self) -> float:
        return self._powermeter_service.energyconsumption

    @property
    def powerconsumption(self) -> float:
        return self._powermeter_service.powerconsumption

    def update(self):
        self._powerswitch_service.short_poll()
        self._powerswitchprogram_service.short_poll()
        self._powermeter_service.short_poll()

    def summary(self):
        print(f"PSM SmartPlug:")
        super().summary()


class SHCShutterControl(SHCDevice):
    from .services_impl import ShutterControlService

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device=raw_device)
        self._service: ShutterControlService = self.device_service("ShutterControl")

    @property
    def level(self) -> float:
        return self._service.level

    @level.setter
    def level(self, level):
        self._service.put_state_element("level", level)

    def stop(self):
        self._service.put_state_element(
            "operationState", ShutterControlService.State.STOPPED.name
        )

    @property
    def operation_state(self) -> ShutterControlService.State:
        return self._service.value

    def update(self):
        self._service.short_poll()

    def summary(self):
        print(f"BBL ShutterControl:")
        super().summary()


class SHCShutterContact(SHCBatteryDevice):
    from .services_impl import ShutterContactService

    class DeviceClass(Enum):
        GENERIC = "GENERIC"
        ENTRANCE_DOOR = "ENTRANCE_DOOR"
        REGULAR_WINDOW = "REGULAR_WINDOW"
        FRENCH_WINDOW = "FRENCH_WINDOW"

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)
        self._service = self.device_service("ShutterContact")

    @property
    def device_class(self) -> DeviceClass:
        return self.DeviceClass(self.profile)

    @property
    def state(self) -> ShutterContactService.State:
        return self._service.value

    def update(self):
        self._service.short_poll()
        super().update()

    def summary(self):
        print(f"SWD ShutterContact:")
        super().summary()


class SHCCameraEyes(SHCDevice):
    from .services_impl import (
        CameraLightService,
        CameraNotificationService,
        PrivacyModeService,
    )

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)

        self._privacymode_service = self.device_service("PrivacyMode")
        self._cameranotification_service = self.device_service("CameraNotification")
        self._cameralight_service = self.device_service("CameraLight")

    @property
    def privacymode(self) -> PrivacyModeService.State:
        return self._privacymode_service.value

    @privacymode.setter
    def privacymode(self, state: bool):
        self._privacymode_service.put_state_element(
            "value", "ENABLED" if state else "DISABLED"
        )

    @property
    def cameranotification(self) -> CameraNotificationService.State:
        return self._cameranotification_service.value

    @cameranotification.setter
    def cameranotification(self, state: bool):
        self._cameranotification_service.put_state_element(
            "value", "ENABLED" if state else "DISABLED"
        )

    @property
    def cameralight(self) -> CameraLightService.State:
        return self._cameralight_service.value

    @cameralight.setter
    def cameralight(self, state: bool):
        self._cameralight_service.put_state_element("value", "ON" if state else "OFF")

    def update(self):
        self._cameralight_service.short_poll()
        self._cameranotification_service.short_poll()
        self._privacymode_service.short_poll()

    def summary(self):
        print(f"CAMERA_EYES CameraEyes:")
        super().summary()


class SHCIntrusionDetectionSystem(SHCDevice):
    from .services_impl import IntrusionDetectionControlService

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)
        self._service = self.device_service("IntrusionDetectionControl")

    def disarm(self):
        self.alarmstate = IntrusionDetectionControlService.State.SYSTEM_DISARMED

    def arm(self):
        self.alarmstate = IntrusionDetectionControlService.State.SYSTEM_ARMED

    def mute_alarm(self):
        self.alarmstate = IntrusionDetectionControlService.State.MUTE_ALARM

    def arm_activation_delay(self, seconds):
        if self.alarmstate == IntrusionDetectionControlService.State.SYSTEM_ARMING:
            return

        self._service.put_state_element("armActivationDelayTime", seconds)

    def arm_instant(self):
        if self.alarmstate == IntrusionDetectionControlService.State.SYSTEM_ARMING:
            return

        delay_time = self._service.armActivationDelayTime
        self.arm_activation_delay(1)
        self.arm()
        self.arm_activation_delay(delay_time)

    def trigger(self):
        # not implemented yet
        pass

    @property
    def alarmstate(self) -> IntrusionDetectionControlService.State:
        return self._service.value

    @alarmstate.setter
    def alarmstate(self, state: IntrusionDetectionControlService.State):
        self._service.put_state_element("value", state.name)

    @property
    def armActivationDelayTime(self):
        return self._service.value

    def update(self):
        self._service.short_poll()

    def summary(self):
        print(f"-IntrusionDetectionSystem-:")
        super().summary()


class SHCThermostat(SHCBatteryDevice):
    from .services_impl import TemperatureLevelService, ValveTappetService

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)
        self._temperaturelevel_service = self.device_service("TemperatureLevel")
        self._valvetappet_service = self.device_service("ValveTappet")

    @property
    def position(self) -> int:
        return self._valvetappet_service.position

    @property
    def temperature(self) -> float:
        return self._temperaturelevel_service.temperature

    def update(self):
        self._temperaturelevel_service.short_poll()
        self._valvetappet_service.short_poll()
        super().update()

    def summary(self):
        print(f"TRV Thermostat:")
        super().summary()


class SHCClimateControl(SHCDevice):
    from .services_impl import RoomClimateControlService, TemperatureLevelService

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)
        self._temperaturelevel_service = self.device_service("TemperatureLevel")
        self._roomclimatecontrol_service = self.device_service("RoomClimateControl")

    @property
    def setpoint_temperature(self) -> float:
        return self._roomclimatecontrol_service.setpoint_temperature

    @setpoint_temperature.setter
    def setpoint_temperature(self, temperature: float):
        self._roomclimatecontrol_service.setpoint_temperature = temperature

    @property
    def temperature(self) -> float:
        return self._temperaturelevel_service.temperature

    def update(self):
        self._temperaturelevel_service.short_poll()
        self._roomclimatecontrol_service.short_poll()
        super().update()

    def summary(self):
        print(f"ROOM_CLIMATE_CONTROL:")
        super().summary()


class SHCWallThermostat(SHCBatteryDevice):
    from .services_impl import TemperatureLevelService, HumidityLevelService

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)
        self._temperaturelevel_service = self.device_service("TemperatureLevel")
        self._humiditylevel_service = self.device_service("HumidityLevel")

    @property
    def temperature(self) -> float:
        return self._temperaturelevel_service.temperature

    @property
    def humidity(self) -> float:
        return self._humiditylevel_service.humidity

    def update(self):
        self._temperaturelevel_service.short_poll()
        self._humiditylevel_service.short_poll()
        super().update()

    def summary(self):
        print(f"THB Wall Thermostat:")
        super().summary()


class SHCUniversalSwitch(SHCBatteryDevice):
    from .services_impl import KeypadService

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)
        self._keypad_service = self.device_service("Keypad")

    @property
    def keycode(self) -> int:
        return self._keypad_service.keyCode

    @property
    def keyname(self) -> KeypadService.KeyState:
        return self._keypad_service.keyName

    @property
    def eventtype(self) -> KeypadService.KeyEvent:
        return self._keypad_service.eventType

    @property
    def eventtimestamp(self) -> int:
        return self._keypad_service.eventTimestamp

    def update(self):
        self._keypad_service.short_poll()
        super().update()

    def summary(self):
        print(f"WRC2 Universal Switch:")
        super().summary()


class SHCMotionDetector(SHCBatteryDevice):
    from .services_impl import LatestMotionService

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)
        self._service = self.device_service("LatestMotion")

    @property
    def latestmotion(self) -> str:
        return self._service.latestMotion

    def update(self):
        self._service.short_poll()
        super().update()

    def summary(self):
        print(f"MD Motion Detector:")
        super().summary()


class SHCTwinguard(SHCBatteryDevice):
    from .services_impl import AirQualityLevelService, SmokeDetectorCheckService

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)
        self._airqualitylevel_service: AirQualityLevelService = self.device_service(
            "AirQualityLevel"
        )
        self._smokedetectorcheck_service: SmokeDetectorCheckService = self.device_service(
            "SmokeDetectorCheck"
        )

    @property
    def combinedrating(self) -> AirQualityLevelService.RatingState:
        return self._airqualitylevel_service.combinedRating

    @property
    def description(self) -> str:
        return self._airqualitylevel_service.description

    @property
    def temperature(self) -> int:
        return self._airqualitylevel_service.temperature

    @property
    def temperatureRating(self) -> AirQualityLevelService.RatingState:
        return self._airqualitylevel_service.temperatureRating

    @property
    def humidity(self) -> int:
        return self._airqualitylevel_service.humidity

    @property
    def humidityrating(self) -> AirQualityLevelService.RatingState:
        return self._airqualitylevel_service.humidityRating

    @property
    def purity(self) -> int:
        return self._airqualitylevel_service.purity

    @property
    def purityrating(self) -> str:
        return self._airqualitylevel_service.purityRating

    @property
    def smokedetectorcheck_state(self) -> SmokeDetectorCheckService.State:
        return self._smokedetectorcheck_service.value

    def smoketest_requested(self):
        self._smokedetectorcheck_service.put_state_element(
            "value", "SMOKE_TEST_REQUESTED"
        )

    def update(self):
        self._airqualitylevel_service.short_poll()
        self._smokedetectorcheck_service.short_poll()
        super().update()

    def summary(self):
        print(f"TWINGUARD:")
        super().summary()


MODEL_MAPPING = {
    "SWD": SHCShutterContact,
    "BBL": SHCShutterControl,
    "PSM": SHCSmartPlug,
    "BSM": SHCSmartPlug,  # uses same impl as PSM
    "SD": SHCSmokeDetector,
    "CAMERA_EYES": SHCCameraEyes,
    "INTRUSION_DETECTION_SYSTEM": SHCIntrusionDetectionSystem,
    "ROOM_CLIMATE_CONTROL": SHCClimateControl,
    "TRV": SHCThermostat,
    "THB": SHCWallThermostat,
    "WRC2": SHCUniversalSwitch,
    "MD": SHCMotionDetector,
    "TWINGUARD": SHCTwinguard,
}
# "PRESENCE_SIMULATION_SERVICE": "Presence Simulation"
# "CAMERA_360": "Security Camera 360"

SUPPORTED_MODELS = MODEL_MAPPING.keys()


def build(api, raw_device):
    device_model = raw_device["deviceModel"]
    assert device_model in SUPPORTED_MODELS, "Device model is supported"
    return MODEL_MAPPING[device_model](api=api, raw_device=raw_device)
