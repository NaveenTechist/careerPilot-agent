from abc import ABC
from abc import abstractmethod

from .strategy_result import StrategyResult


class BaseExtractionStrategy(ABC):
    @abstractmethod
    def extract(
        self,
        url: str,
    ) -> StrategyResult: ...
