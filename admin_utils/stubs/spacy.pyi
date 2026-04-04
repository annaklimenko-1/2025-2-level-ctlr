from typing import Protocol, runtime_checkable

from core_utils.pipeline import AbstractCoNLLUAnalyzer

@runtime_checkable
class Language(Protocol):
    def analyze_pipes(self) -> dict | None: ...
