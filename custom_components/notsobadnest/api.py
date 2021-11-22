import logging

from requests_futures.sessions import FuturesSession
import simplejson

from homeassistant.util import dt

API_URL = "https://home.nest.com"
TOKEN_URL = "https://oauth2.googleapis.com/token"
CLIENT_ID = "733249279899-1gpkq9duqmdp55a7e5lft1pr2smumdla.apps.googleusercontent.com"
CLIENT_ID_FT = (
    "384529615266-57v6vaptkmhm64n9hn5dcmkr4at14p8j.apps.googleusercontent.com"
)
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/75.0.3770.100 Safari/537.36"
)
URL_JWT = "https://nestauthproxyservice-pa.googleapis.com/v1/issue_jwt"
NEST_API_KEY = "AIzaSyAdkSIMNc51XGNEAYWasX9UOWkS5P6sZE4"
KNOWN_BUCKET_TYPES = ["topaz"]

REQUEST_TIMEOUT = 30

_LOGGER = logging.getLogger(__name__)


class NestAPI:
    def __init__(self, hass, refresh_token, field_test=False):
        self._hass = hass
        self.rooms = {}
        self.protects = {}
        self.available = True
        self._field_test = field_test

        self._session = FuturesSession()
        self._session.headers.update(
            {
                "Referer": "https://home.nest.com/",
                "User-Agent": USER_AGENT,
            }
        )
        self._refresh_token = refresh_token

    async def setup(self):
        if await self.login():
            return await self.update()
        else:
            return False

    async def _call_nest_api(
        self,
        method,
        url,
        headers,
        json=None,
        params=None,
        data=None,
        is_retry=False,
        is_json=True,
    ):
        try:
            if method == "get":
                r = self._session.get(
                    url=url,
                    headers=headers,
                    params=params,
                    json=json,
                    data=data,
                    timeout=REQUEST_TIMEOUT,
                ).result()
            elif method == "post":
                r = self._session.post(
                    url=url,
                    headers=headers,
                    params=params,
                    json=json,
                    data=data,
                    timeout=REQUEST_TIMEOUT,
                ).result()
            else:
                _LOGGER.error("Unsupported Method: {}".format(method))
        except KeyError:
            if is_retry:
                _LOGGER.error(
                    "KeyError Retry Failed Calling: {}\nMethod: {}".format(url, method)
                )
            else:
                _LOGGER.error(
                    "KeyError Failed Calling: {}\nMethod: {}".format(url, method)
                )
                if self.login():
                    if "Authorization" in headers:
                        headers["Authorization"] = f"Basic {self._access_token}"
                    return await self._call_nest_api(
                        method,
                        url,
                        headers,
                        json=json,
                        params=params,
                        data=data,
                        is_retry=True,
                        is_json=is_json,
                    )
        else:
            # Parse Json
            if r.status_code == 200:
                try:
                    if is_json:
                        api_response = r.json()
                    else:
                        api_response = r.content

                    self.available = True
                except simplejson.errors.JSONDecodeError as e:
                    _LOGGER.error(
                        "API Response: JsonDecodeError: return code {} and returned text {}  for url {}".format(
                            r.text, r.status_code, url
                        )
                    )
                else:
                    return api_response
            elif r.status_code != 200 and r.status_code not in (502, 401):
                _LOGGER.error(
                    "Bad API Response: Information for further debugging: return code {} and returned text {} for url {}".format(
                        r.status_code, r.text, url
                    )
                )
                self.available = False
            elif r.status_code == 401:
                if is_retry:
                    _LOGGER.error(
                        "401 Retry Failed Calling: {}\nMethod: {}".format(url, method)
                    )
                    self.available = False
                else:
                    if await self.login():
                        if "Authorization" in headers:
                            headers["Authorization"] = f"Basic {self._access_token}"
                        return await self._call_nest_api(
                            method,
                            url,
                            headers,
                            json=json,
                            params=params,
                            data=data,
                            is_retry=True,
                            is_json=is_json,
                        )
            else:
                _LOGGER.error("502 API Response for url {}".format(url))
        return False

    async def login(self):
        status = await self._login_google(self._refresh_token)
        if not status:
            _LOGGER.error("Login To Google Failes")
        return status

    async def _login_google(self, refresh_token):
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": USER_AGENT,
        }
        data = {
            "refresh_token": refresh_token,
            "client_id": CLIENT_ID if not self._field_test else CLIENT_ID_FT,
            "grant_type": "refresh_token",
        }
        r = await self._call_nest_api(
            method="post", url=TOKEN_URL, headers=headers, data=data
        )
        if not r:
            _LOGGER.error("Failed Getting Access Token")
            return False
        else:
            access_token = r["access_token"]

            headers = {
                "User-Agent": USER_AGENT,
                "Authorization": "Bearer " + access_token,
                "x-goog-api-key": NEST_API_KEY,
                "Referer": "https://home.nest.com",
            }
            params = {
                "embed_google_oauth_access_token": True,
                "expire_after": "3600s",
                "google_oauth_access_token": access_token,
                "policy_id": "authproxy-oauth-policy",
            }
            r = await self._call_nest_api(
                method="post", url=URL_JWT, headers=headers, params=params
            )
            if not r:
                _LOGGER.error("Failed Getting JWT")
                return False
            else:
                self._user_id = r["claims"]["subject"]["nestId"]["id"]
                self._access_token = r["jwt"]
        return True

    async def update(self):
        try:
            APP_LAUNCH_URL = f"{API_URL}/api/0.1/user/{self._user_id}/app_launch"
            APP_LAUNCH_HEADERS = {"Authorization": f"Basic {self._access_token}"}
            APP_LAUNCH_JSON = {
                "known_bucket_types": ["where"],
                "known_bucket_versions": [],
            }

            r = await self._call_nest_api(
                method="post",
                url=APP_LAUNCH_URL,
                json=APP_LAUNCH_JSON,
                headers=APP_LAUNCH_HEADERS,
            )

            if not r:
                _LOGGER.error("Failed Calling App Launch")
                return False

            buckets = r["updated_buckets"]

            for bucket in buckets:
                sensor_data = bucket["value"]
                sn = bucket["object_key"].split(".")[1]
                if bucket["object_key"].startswith(f"where.{sn}"):
                    for where in sensor_data["wheres"]:
                        self.rooms[where["where_id"]] = Room(where)

            APP_LAUNCH_JSON = {
                "known_bucket_types": KNOWN_BUCKET_TYPES,
                "known_bucket_versions": [],
            }

            r = await self._call_nest_api(
                method="post",
                url=APP_LAUNCH_URL,
                json=APP_LAUNCH_JSON,
                headers=APP_LAUNCH_HEADERS,
            )

            if not r:
                _LOGGER.error("Failed Calling App Launch")
                return False

            buckets = r["updated_buckets"]

            for bucket in buckets:
                sensor_data = bucket["value"]
                sn = bucket["object_key"].split(".")[1]

                if bucket["object_key"].startswith(f"topaz.{sn}"):
                    if not self.protects.get(sn):
                        self.protects[sn] = NestProtect(self, sn, sensor_data)
                    else:
                        self.protects[sn].update(sn, sensor_data)

            return True
        except Exception:
            return False


class Room:
    def __init__(self, data: dict) -> None:
        self.where_id = data["where_id"]
        self.name = data["name"]


class NestProtect:
    def __init__(self, api, serial, data: dict):
        self.serial = serial
        self.room = api.rooms[data["where_id"]]
        self.name = self.room.name + " Protect"
        self.ip = data["wifi_ip_address"]
        self.ac_power = data["wired_or_battery"] == 0
        self.software_version = data["software_version"]
        self.model = data["model"]
        self.replace_by = dt.utc_from_timestamp(data["replace_by_date_utc_secs"])
        self.update(serial, data)

    def update(self, serial, data: dict):
        self.smoke_detected = data["smoke_status"] == 3
        self.smoke_warning = data["smoke_status"] == 1 or data["smoke_status"] == 2
        self.co_detected = data["co_status"] == 3
        self.co_warning = data["co_status"] == 1 or data["co_status"] == 2
        self.heat_detected = data["heat_status"] == 3
        self.heat_warning = data["heat_status"] == 1 or data["heat_status"] == 2
        self.motion_enabled = data["night_light_enable"]
        self.motion_detected = data["auto_away"] == 0
        self.manual_test_active = (
            dt.as_timestamp(dt.utcnow()) - data["latest_manual_test_start_utc_secs"]
            < 60
            # and not dt.as_timestamp(dt.utcnow())
            # - data["latest_manual_test_end_utc_secs"]
            # < 20
        )
        self.battery_state = data["battery_health_state"]
        self.battery_level = round(data["battery_level"] / 100, 1)
        self.steam_detection = data["steam_detection_enable"]
        self.hushed = data["hushed_state"]
        self.attributes = data
