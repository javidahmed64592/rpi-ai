import json
from unittest.mock import mock_open, patch

from rpi_ai.config import AIConfigType


class TestAIConfigType:
    def test_load(self, config_data: dict[str, str | float]) -> None:
        with patch("builtins.open", new_callable=mock_open, read_data=json.dumps(config_data)):
            config = AIConfigType.load("dummy_path")
            assert config.model == "test-model"
            assert config.candidate_count == 2
            assert config.max_output_tokens == 50
            assert config.temperature == 0.7

    def test_generation_config(self, config_data: dict[str, str | float]) -> None:
        config = AIConfigType(**config_data)
        gen_config = config.generation_config
        assert gen_config.candidate_count == 2
        assert gen_config.max_output_tokens == 50
        assert gen_config.temperature == 0.7
