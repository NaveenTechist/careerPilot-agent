"""
Site Detector.

Chooses the correct
automation strategy
based on URL.
"""

from urllib.parse import urlparse

from automation.strategies.linkedin_strategy import LinkedInStrategy

from automation.strategies.greenhouse_strategy import GreenhouseStrategy

from automation.strategies.workday_strategy import WorkdayStrategy

from automation.strategies.lever_strategy import LeverStrategy

from automation.strategies.naukri_strategy import NaukriStrategy

from automation.strategies.generic_strategy import GenericStrategy


class SiteDetector:

    @staticmethod
    def detect(

        url: str,

    ):

        host = urlparse(

            url

        ).netloc.lower()

        if "linkedin.com" in host:
            return LinkedInStrategy()
        if "greenhouse.io" in host:
            return GreenhouseStrategy()
        if "myworkdayjobs.com" in host:
            return WorkdayStrategy()
        if "lever.co" in host:
            return LeverStrategy()
        if "naukri.com" in host:
            return NaukriStrategy()
        return GenericStrategy()