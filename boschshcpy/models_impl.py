from enum import Enum

from .device import SHCDevice
from .services_impl import CameraLightService


class SHCSmokeDetector(SHCDevice):
    class AlarmState(Enum):
        INTRUSION_ALARM_ON_REQUESTED = "INTRUSION_ALARM_ON_REQUESTED"
        INTRUSION_ALARM_OFF_REQUESTED = "INTRUSION_ALARM_OFF_REQUESTED"
        MUTE_SECONDARY_ALARM_REQUESTED = "MUTE_SECONDARY_ALARM_REQUESTED"

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)

        self._service = self.device_service('Alarm')

    def set_alarmstate(self, state: AlarmState):
        self._service.put_state_element('state', state.name)

    def summary(self):
        print(f"SD SmokeDetector:")
        super().summary()


class SHCSmartPlug(SHCDevice):
    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)

        self._service = self.device_service('PowerSwitch')

    def set_state(self, state: bool):
        self._service.put_state_element('state', state)

    def summary(self):
        print(f"PSM SmartPlug:")
        super().summary()


class SHCShutterControl(SHCDevice):
    def __init__(self, api, raw_device):
        super().__init__(api, raw_device=raw_device)

        self._service = self.device_service('ShutterControl')

    def set_level(self, level):
        self._service.put_state_element('level', level)

    @property
    def level(self) -> float:
        self._service.short_poll()
        return self._service.level

    def set_stopped(self):
        self._service.put_state_element('operationState', 'STOPPED')

    def summary(self):
        print(f"BBL ShutterControl:")
        super().summary()


class SHCShutterContact(SHCDevice):
    class DeviceClass(Enum):
        GENERIC = "GENERIC"
        ENTRANCE_DOOR = "ENTRANCE_DOOR"
        REGULAR_WINDOW = "REGULAR_WINDOW"
        FRENCH_WINDOW = "FRENCH_WINDOW"

    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)

    @property
    def device_class(self) -> DeviceClass:
        return self.DeviceClass(self.profile)

    def summary(self):
        print(f"SWD ShutterContact:")
        super().summary()


class SHCCameraEyes(SHCDevice):
    def __init__(self, api, raw_device):
        super().__init__(api, raw_device)

        self._privacymode_service = self.device_service('PrivacyMode')
        self._cameranotification_service = self.device_service(
            'CameraNotification')
        self._cameralight_service = self.device_service('CameraLight')

    def set_privacymode(self, state: bool):
        self._privacymode_service.put_state_element(
            'value', "ENABLED" if state else "DISABLED")

    def set_cameranotification(self, state: bool):
        self._cameranotification_service.put_state_element(
            'value', "ENABLED" if state else "DISABLED")

    def set_cameralight(self, state: bool):
        self._cameralight_service.put_state_element(
            'value', "ON" if state else "OFF")

    @property
    def get_light_state(self) -> CameraLightService.State:
        self._cameralight_service.short_poll()
        return self._cameralight_service.value

    def summary(self):
        print(f"CAMERA_EYES CameraEyes:")
        super().summary()


MODEL_MAPPING = {
    "SWD": "ShutterContact",
    "BBL": "ShutterControl",
    "PSM": "SmartPlug",
    "SD": "SmokeDetector",
    "CAMERA_EYES": "CameraEyes",
}
# "WRC2": "UniversalSwitchFlex",
# "BSM": "LightControl",
# "MD": "MotionDetector"

SUPPORTED_MODELS = MODEL_MAPPING.keys()