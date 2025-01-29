from __future__ import annotations

import json

import google.generativeai as genai
from pydantic.dataclasses import dataclass


@dataclass
class AIConfigType:
    model: str
    system_instruction: str
    candidate_count: int = 1
    max_output_tokens: int = 20
    temperature: float = 1.0

    @classmethod
    def load(cls, path: str) -> AIConfigType:
        with open(path) as file:
            return cls(**json.load(file))

    @property
    def generation_config(self) -> genai.types.GenerationConfig:
        return genai.types.GenerationConfig(
            candidate_count=self.candidate_count,
            max_output_tokens=self.max_output_tokens,
            temperature=self.temperature,
        )
