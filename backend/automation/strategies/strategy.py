"""
Base Strategy.

Every job site automation
must implement this interface.
"""

from abc import ABC
from abc import abstractmethod
from playwright.sync_api import Page


class Strategy(ABC):

    @abstractmethod
    def run(
        self,
        page: Page,
        application,
    ):
        pass