import json
from unittest.mock import mock_open, patch

from rpi_ai.config import AIConfigType


class TestAIConfigType:
    def test_load(self, config_data: dict[str, str | float]) -> None:
        with patch("builtins.open", new_callable=mock_open, read_data=json.dumps(config_data)):
            config = AIConfigType.load("dummy_path")
            assert config.model == "test-model"
            assert config.candidate_count == config_data["candidate_count"]
            assert config.max_output_tokens == config_data["max_output_tokens"]
            assert config.temperature == config_data["temperature"]

    def test_generation_config(self, config_data: dict[str, str | float]) -> None:
        config = AIConfigType(**config_data)
        gen_config = config.generation_config
        assert gen_config.candidate_count == config_data["candidate_count"]
        assert gen_config.max_output_tokens == config_data["max_output_tokens"]
        assert gen_config.temperature == config_data["temperature"]
