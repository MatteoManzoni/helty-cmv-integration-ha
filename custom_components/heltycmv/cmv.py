import socket
import logging
from .const import (
    NAME_CMD,
    SENSORS_CMD,
    CONFIG_GET_CMD,
    CMV_NAME_PREFIX,
    PRESET_BOOST,
    PRESET_NIGHT,
    PRESET_COOLING,
    FAN_LOW,
    FAN_MEDIUM,
    FAN_HIGH,
    FAN_HIGHEST,
    MODE_CMDS,
    LED_OFF_CMD,
    LED_ON_CMD,
    RESET_FILTER,
)

_LOGGER = logging.getLogger(__name__)


class HeltyCMV:
    def __init__(self, host: str, port: int) -> None:
        self._host = host
        self._port = port
        self.name = host
        self._id = host.lower()
        self.online = True

    @property
    def cmv_id(self) -> str:
        return self._id

    async def test_connection(self) -> bool:
        """Test connectivity to the Dummy hub is OK."""
        cmv_name = await self.get_cmv_name()
        if not cmv_name:
            return False
        return True

    def _execute_cmv_cmd(self, cmd):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self._host, self._port))
        s.sendall(cmd)
        data = s.recv(1024)
        s.close()
        return data.decode('ASCII').strip()

    async def get_cmv_name(self):
        try:
            return self._execute_cmv_cmd(NAME_CMD).removeprefix(CMV_NAME_PREFIX).strip()
        except Exception as e:
            _LOGGER.warning(e)
            return None

    async def get_cmv_indoor_air_temperature(self):
        try:
            indoor_air_temp = None
            data = self._execute_cmv_cmd(SENSORS_CMD).strip().split(',')
            if data[0] == "VMGI":
                indoor_air_temp = float(int(data[1]) / 10)
            return indoor_air_temp
        except Exception as e:
            _LOGGER.warning(e)
            return None

    async def get_cmv_outdoor_air_temperature(self):
        try:
            outdoor_air_temp = None
            data = self._execute_cmv_cmd(SENSORS_CMD).strip().split(',')
            if data[0] == "VMGI":
                outdoor_air_temp = float(int(data[2]) / 10)
            return outdoor_air_temp
        except Exception as e:
            _LOGGER.warning(e)
            return None

    async def get_cmv_indoor_humidity(self):
        try:
            indoor_air_humidity = None
            data = self._execute_cmv_cmd(SENSORS_CMD).strip().split(',')
            if data[0] == "VMGI":
                indoor_air_humidity = float(int(data[3]) / 10)
            return indoor_air_humidity
        except Exception as e:
            _LOGGER.warning(e)
            return None

    async def get_cmv_op_status(self):
        try:
            op_state_int = None
            data = self._execute_cmv_cmd(CONFIG_GET_CMD).strip().split(',')
            if data[0] == "VMGO":
                op_state_int = int(data[1])
            if op_state_int == 1:
                return {"preset": None, "fan_mode": FAN_LOW}
            elif op_state_int == 2:
                return {"preset": None, "fan_mode": FAN_MEDIUM}
            elif op_state_int == 3:
                return {"preset": None, "fan_mode": FAN_HIGH}
            elif op_state_int == 4:
                return {"preset": None, "fan_mode": FAN_HIGHEST}
            elif op_state_int == 5:
                return {"preset": PRESET_BOOST, "fan_mode": None}
            elif op_state_int == 6:
                return {"preset": PRESET_NIGHT, "fan_mode": None}
            elif op_state_int == 7:
                return {"preset": PRESET_COOLING, "fan_mode": None}
            else:
                return None
        except Exception as e:
            _LOGGER.warning(e)
            return None

    async def set_cmv_mode(self, mode):
        exec_result = self._execute_cmv_cmd(MODE_CMDS.get(mode, NAME_CMD))
        if exec_result == "OK":
            return True

    async def are_cmv_leds_on(self):
        try:
            led_state_int = None
            data = self._execute_cmv_cmd(CONFIG_GET_CMD).strip().split(',')
            if data[0] == "VMGO":
                led_state_int = int(data[2])
            if led_state_int == 10:
                return True
            elif led_state_int == 0:
                return False
            else:
                return None
        except Exception as e:
            _LOGGER.warning(e)
            return None

    async def turn_cmv_leds_off(self):
        exec_result = self._execute_cmv_cmd(LED_OFF_CMD)
        if exec_result == "OK":
            return True

    async def turn_cmv_leds_on(self):
        exec_result = self._execute_cmv_cmd(LED_ON_CMD)
        if exec_result == "OK":
            return True

    async def reset_cmv_filters(self, mode):
        exec_result = self._execute_cmv_cmd(RESET_FILTER)
        if exec_result == "OK":
            return True