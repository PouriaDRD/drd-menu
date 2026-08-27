from __future__ import annotations

import ipaddress
import logging

from dataclasses import asdict, dataclass
from typing import Any

from django.conf import settings
from geoip2.database import Reader
from geoip2.errors import AddressNotFoundError

from user_agents import parse
from rest_framework.request import Request

from accounts.repositories import UserRepository
from authentication.repositories import LoginHistoryRepository

logger = logging.getLogger("authentication.login_history")


# ==========================================================================
# DTO
# ==========================================================================


@dataclass(frozen=True, slots=True)
class LoginInfo:
    """
    Structured information extracted from an HTTP request.

    This DTO acts as the data-transfer object between request parsing
    and LoginHistoryRepository.
    """

    # ------------------------------------------------------------------
    # Network
    # ------------------------------------------------------------------

    ip_address: str | None

    # ------------------------------------------------------------------
    # User Agent
    # ------------------------------------------------------------------

    user_agent: str | None

    # ------------------------------------------------------------------
    # Device
    # ------------------------------------------------------------------

    device: str | None
    device_family: str | None

    # ------------------------------------------------------------------
    # Browser
    # ------------------------------------------------------------------

    browser: str | None
    browser_version: str | None

    # ------------------------------------------------------------------
    # Operating System
    # ------------------------------------------------------------------

    operating_system: str | None
    operating_system_version: str | None

    # ------------------------------------------------------------------
    # Geo
    # ------------------------------------------------------------------

    country: str | None = None
    country_code: str | None = None
    city: str | None = None
    region: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    # ------------------------------------------------------------------
    # Conversion
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the DTO into a dictionary suitable for repository calls.
        """

        return asdict(self)


# ==========================================================================
# Service
# ==========================================================================


class LoginHistoryService:
    """
    Service responsible for recording login attempts and extracting
    client information from HTTP requests.
    """

    user_repo = UserRepository
    login_history_repo = LoginHistoryRepository

    # ======================================================================
    # Successful Login
    # ======================================================================

    @classmethod
    def log_success(cls, user, request: Request):
        """
        Record a successful login attempt.
        """

        if not user:
            raise ValueError("User is required for successful login history.")

        if not request:
            raise ValueError("Request is required for login history.")

        login_info = cls.get_login_info(request)

        return cls.login_history_repo.create(
            user=user,
            **login_info.to_dict(),
            is_successful=True,
            failure_reason=None,
        )

    # ======================================================================
    # Failed Login
    # ======================================================================

    @classmethod
    def log_failed(cls, phone_number: str, request: Request, reason: str):
        """
        Record a failed login attempt.
        """

        if not phone_number or not phone_number.strip():
            logger.warning("Failed login history skipped: " "phone number is empty.")

            return None

        if not request:
            logger.warning("Failed login history skipped: " "request is missing.")

            return None

        user = cls.user_repo.get_by_phone_number(phone_number)

        if not user:
            logger.warning("Failed login attempt for unknown user.")

            return None

        login_info = cls.get_login_info(request)

        return cls.login_history_repo.create(
            user=user,
            **login_info.to_dict(),
            is_successful=False,
            failure_reason=reason,
        )

    # ======================================================================
    # Login Information
    # ======================================================================

    @classmethod
    def get_login_info(cls, request: Request) -> LoginInfo:
        """
        Extract structured client information from an HTTP request.

        The following information is collected:

        - IP address
        - User-Agent
        - Device
        - Device family
        - Browser
        - Browser version
        - Operating system
        - Operating system version
        - Country
        - Country code
        - City
        - Region
        - Latitude
        - Longitude
        """

        # --------------------------------------------------------------
        # User Agent
        # --------------------------------------------------------------

        user_agent_string = request.META.get(
            "HTTP_USER_AGENT",
            "",
        ).strip()

        user_agent = parse(user_agent_string)

        # --------------------------------------------------------------
        # IP
        # --------------------------------------------------------------

        ip_address = cls.get_client_ip(request)

        # --------------------------------------------------------------
        # Geo
        # --------------------------------------------------------------

        geo_info = cls.get_geo_info(ip_address)

        # --------------------------------------------------------------
        # DTO
        # --------------------------------------------------------------

        return LoginInfo(
            # Network
            ip_address=ip_address,
            # User Agent
            user_agent=cls.clean_value(user_agent_string),
            # Device
            device=cls.get_device_type(user_agent),
            device_family=cls.clean_value(user_agent.device.family),
            # Browser
            browser=cls.clean_value(user_agent.browser.family),
            browser_version=cls.clean_value(user_agent.browser.version_string),
            # Operating System
            operating_system=cls.clean_value(user_agent.os.family),
            operating_system_version=cls.clean_value(user_agent.os.version_string),
            # Geo
            country=geo_info.country,
            country_code=geo_info.country_code,
            city=geo_info.city,
            region=geo_info.region,
            latitude=geo_info.latitude,
            longitude=geo_info.longitude,
        )

    # ======================================================================
    # Geo DTO
    # ======================================================================

    @dataclass(frozen=True, slots=True)
    class GeoInfo:
        """
        Geographic information resolved from an IP address.
        """

        country: str | None = None
        country_code: str | None = None
        city: str | None = None
        region: str | None = None
        latitude: float | None = None
        longitude: float | None = None

    # ======================================================================
    # GeoIP
    # ======================================================================

    @classmethod
    def get_geo_info(cls, ip_address: str | None) -> GeoInfo:
        """
        Resolve geographic information from an IP address.

        Uses the local MaxMind GeoIP2/GeoLite2 database.

        Returns an empty GeoInfo when:

        - IP address is missing
        - IP address is invalid
        - IP address is private
        - IP address is loopback
        - IP address is not found in the database
        - GeoIP database is unavailable
        """

        if not ip_address:
            return cls.GeoInfo()

        try:
            ip = ipaddress.ip_address(ip_address)

        except ValueError:
            logger.warning(
                "Invalid IP address for GeoIP lookup: %s",
                ip_address,
            )

            return cls.GeoInfo()

        # --------------------------------------------------------------
        # Private / Local IP
        # --------------------------------------------------------------

        if ip.is_private or ip.is_loopback or ip.is_reserved or ip.is_unspecified:
            return cls.GeoInfo()

        # --------------------------------------------------------------
        # GeoIP Database
        # --------------------------------------------------------------

        database_path = settings.GEOIP_PATH / "GeoLite2-City.mmdb"

        try:
            with Reader(str(database_path)) as reader:

                response = reader.city(ip_address)

        except AddressNotFoundError:
            logger.info(
                "IP address was not found in GeoIP database: %s",
                ip_address,
            )

            return cls.GeoInfo()

        except FileNotFoundError:
            logger.error(
                "GeoIP database not found: %s",
                database_path,
            )

            return cls.GeoInfo()

        except Exception:
            logger.exception(
                "GeoIP lookup failed for IP: %s",
                ip_address,
            )

            return cls.GeoInfo()

        # --------------------------------------------------------------
        # Country
        # --------------------------------------------------------------

        country = cls.clean_value(response.country.name)

        country_code = cls.clean_value(response.country.iso_code)

        # --------------------------------------------------------------
        # City
        # --------------------------------------------------------------

        city = cls.clean_value(response.city.name)

        # --------------------------------------------------------------
        # Region
        # --------------------------------------------------------------

        region = None

        if response.subdivisions:
            region = cls.clean_value(response.subdivisions.most_specific.name)

        # --------------------------------------------------------------
        # Coordinates
        # --------------------------------------------------------------

        latitude = response.location.latitude
        longitude = response.location.longitude

        return cls.GeoInfo(
            country=country,
            country_code=country_code,
            city=city,
            region=region,
            latitude=latitude,
            longitude=longitude,
        )

    # ======================================================================
    # Device Type
    # ======================================================================

    @staticmethod
    def get_device_type(user_agent) -> str:
        """
        Determine the general device type.
        """

        if user_agent.is_mobile:
            return "Mobile"

        if user_agent.is_tablet:
            return "Tablet"

        if user_agent.is_pc:
            return "PC"

        if user_agent.is_bot:
            return "Bot"

        return "Unknown"

    # ======================================================================
    # Value Cleaning
    # ======================================================================

    @staticmethod
    def clean_value(value: Any) -> str | None:
        """
        Normalize parser values.

        Values such as 'Other' are converted to None.
        """

        if value is None:
            return None

        value = str(value).strip()

        if not value:
            return None

        if value.lower() == "other":
            return None

        return value

    # ======================================================================
    # Client IP
    # ======================================================================

    @staticmethod
    def get_client_ip(request: Request) -> str | None:
        """
        Get the client's IP address.

        X-Forwarded-For should only be trusted when the application
        is behind a trusted reverse proxy.
        """

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()

        return request.META.get("REMOTE_ADDR")
