from unittest.mock import MagicMock

from google.genai.types import FunctionCall, GenerateContentConfig
from gtts import gTTSError

from rpi_ai.models.chatbot import Chatbot
from rpi_ai.types import AIConfigType, FunctionTool, FunctionToolList


class TestChatbot:
<<<<<<< HEAD
    def test_init(
        self,
        mock_chatbot: Chatbot,
        mock_config: AIConfigType,
        mock_api_key: MagicMock,
        mock_genai_configure: MagicMock,
        mock_generative_model: MagicMock,
    ) -> None:
        mock_genai_configure.assert_called_once_with(api_key=mock_api_key.return_value)
        mock_generative_model.assert_called_once_with(
            model_name=mock_config.model,
            system_instruction=mock_config.system_instruction,
            generation_config=mock_config.generation_config,
            tools=[*mock_chatbot._functions.functions, mock_chatbot._web_search_tool],
        )

    def test_first_message(self, mock_chatbot: Chatbot) -> None:
        assert mock_chatbot.first_message["role"] == "model"
        assert isinstance(mock_chatbot.first_message["parts"], str)
=======
    def test_init(self, mock_chatbot: Chatbot, mock_api_key: MagicMock, mock_genai_client: MagicMock) -> None:
        mock_genai_client.assert_called_once_with(api_key=mock_api_key.return_value)
>>>>>>> 34d5619378c3ca9a3260f5b72f49c0852cff3aa7

    def test_extract_command_without_args_from_part_with_valid_function(
        self,
        mock_chatbot: Chatbot,
        mock_functions_list: FunctionToolList,
        mock_response_command_without_args: MagicMock,
    ) -> None:
        part = mock_response_command_without_args.candidates[0].content.parts[0]
        command = mock_chatbot._extract_command_from_part(part)

        assert command is not None
        assert command.function.name == part.function_call.name
        assert command.callable_fn == mock_functions_list[part.function_call.name]

    def test_extract_command_with_args_from_part_with_valid_function(
        self, mock_chatbot: Chatbot, mock_functions_list: FunctionToolList, mock_response_command_with_args: MagicMock
    ) -> None:
        part = mock_response_command_with_args.candidates[0].content.parts[0]
        command = mock_chatbot._extract_command_from_part(part)

        assert command is not None
        assert command.function.name == part.function_call.name
        assert command.callable_fn == mock_functions_list[part.function_call.name]
        assert command.function.args == part.function_call.args

    def test_extract_command_from_part_with_invalid_function(self, mock_chatbot: Chatbot) -> None:
        mock_part = MagicMock(function_call=None)

        command = mock_chatbot._extract_command_from_part(mock_part)
        assert command is None

    def test_get_commands_without_args_from_response(
        self,
        mock_chatbot: Chatbot,
        mock_functions_list: FunctionToolList,
        mock_response_command_without_args: MagicMock,
    ) -> None:
        commands = list(mock_chatbot._get_commands_from_response(mock_response_command_without_args))
        assert len(commands) == 1

        function_name = mock_response_command_without_args.candidates[0].content.parts[0].function_call.name
        assert commands[0].name == function_name
        assert commands[0].callable_fn == mock_functions_list[function_name]

    def test_get_commands_with_args_from_response(
        self, mock_chatbot: Chatbot, mock_functions_list: FunctionToolList, mock_response_command_with_args: MagicMock
    ) -> None:
        commands = list(mock_chatbot._get_commands_from_response(mock_response_command_with_args))
        assert len(commands) == 1

        function_name = mock_response_command_with_args.candidates[0].content.parts[0].function_call.name
        assert commands[0].name == function_name
        assert commands[0].callable_fn == mock_functions_list[function_name]
        assert (
            commands[0].function.args
            == mock_response_command_with_args.candidates[0].content.parts[0].function_call.args
        )

    def test_get_response_parts_from_commands_with_valid_commands(
        self, mock_chatbot: Chatbot, mock_functions_list: FunctionToolList
    ) -> None:
        commands = [
            FunctionTool(
                fn=FunctionCall(name=mock_functions_list.functions[0].__name__, args={}),
                callable_fn=mock_functions_list.functions[0],
            ),
            FunctionTool(
                fn=FunctionCall(name=mock_functions_list.functions[1].__name__, args={"data": "test"}),
                callable_fn=mock_functions_list.functions[1],
            ),
        ]
        response_parts = mock_chatbot._get_response_parts_from_commands(commands)
        assert len(response_parts) == len(commands)
        for i, command in enumerate(commands):
            assert response_parts[i].function_response.name == command.name
            assert response_parts[i].function_response.response["result"] == command.response

    def test_get_response_parts_from_commands_with_invalid_commands(self, mock_chatbot: Chatbot) -> None:
        commands = [FunctionTool(fn=None, callable_fn=None)]
        response_parts = mock_chatbot._get_response_parts_from_commands(commands)
        assert response_parts == []

    def test_handle_commands_with_valid_commands(
        self, mock_chatbot: Chatbot, mock_response_command_without_args: MagicMock, mock_chat_instance: MagicMock
    ) -> None:
        mock_chatbot.start_chat()
        mock_chat_instance.send_message.return_value = MagicMock(parts=[MagicMock(text="Command executed")])
        response = mock_chatbot._handle_commands(mock_response_command_without_args)
        assert response.parts[0].text == "Command executed"

    def test_handle_commands_with_no_commands(
        self, mock_chatbot: Chatbot, mock_response_command_without_args: MagicMock
    ) -> None:
        mock_response_command_without_args.candidates[0].content.parts = []
        response = mock_chatbot._handle_commands(mock_response_command_without_args)
        assert response == mock_response_command_without_args

    def test_handle_commands_with_invalid_commands(
        self, mock_chatbot: Chatbot, mock_response_command_without_args: MagicMock
    ) -> None:
        mock_response_command_without_args.candidates[0].content.parts[0].function_call = None
        response = mock_chatbot._handle_commands(mock_response_command_without_args)
        assert response == mock_response_command_without_args

    def test_get_config(self, mock_chatbot: Chatbot, mock_config: AIConfigType) -> None:
        assert mock_chatbot.get_config() == mock_config

    def test_update_config(
        self,
        mock_chatbot: Chatbot,
        mock_config: AIConfigType,
    ) -> None:
        mock_config.model = "new-model"
        mock_chatbot.update_config(mock_config)
<<<<<<< HEAD
        mock_generative_model.assert_called_with(
            model_name="new-model",
            system_instruction=mock_config.system_instruction,
            generation_config=mock_config.generation_config,
            tools=[*mock_chatbot._functions.functions, mock_chatbot._web_search_tool],
        )
=======
        assert mock_chatbot.get_config() == mock_config
>>>>>>> 34d5619378c3ca9a3260f5b72f49c0852cff3aa7

    def test_start_chat(self, mock_chatbot: Chatbot, mock_start_chat_method: MagicMock) -> None:
        response = mock_chatbot.start_chat()
        mock_start_chat_method.assert_called_once_with(
            model=mock_chatbot._config.model,
            config=GenerateContentConfig(
                system_instruction=mock_chatbot._config.system_instruction,
                candidate_count=mock_chatbot._config.candidate_count,
                max_output_tokens=mock_chatbot._config.max_output_tokens,
                temperature=mock_chatbot._config.temperature,
                tools=mock_chatbot._functions.functions,
            ),
        )
        assert response.message == "What's on your mind today?"

    def test_send_message_with_valid_response(self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock) -> None:
        mock_msg = "Hi model!"
        mock_response = MagicMock(text="Hi user!")
        mock_chat_instance.send_message.return_value = mock_response

        mock_chatbot.start_chat()
        response = mock_chatbot.send_message(mock_msg)
        mock_chat_instance.send_message.assert_called_once_with(mock_msg)
        assert response.message == "Hi user!"

    def test_send_message_with_commands(
        self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock, mock_response_command_without_args: MagicMock
    ) -> None:
        mock_msg = "Hi model!"
        mock_responses = [
            mock_response_command_without_args,
            MagicMock(text="Command executed"),
        ]
        mock_chat_instance.send_message.side_effect = mock_responses

        mock_chatbot.start_chat()
        response = mock_chatbot.send_message(mock_msg)
        assert mock_chat_instance.send_message.call_count == len(mock_responses)
        assert response.message == "Command executed"

    def test_send_message_with_error(self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock) -> None:
        mock_msg = "Hi model!"
        mock_chat_instance.send_message.return_value = MagicMock(text=None)

        mock_chatbot.start_chat()
        response = mock_chatbot.send_message(mock_msg)
        mock_chat_instance.send_message.assert_called_once_with(mock_msg)
        assert response.message == "An error occurred! Please try again."

    def test_send_audio_with_valid_response(
        self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock, mock_get_audio_bytes_from_text: MagicMock
    ) -> None:
        mock_response = MagicMock()
        mock_response = MagicMock(text="Hi user!")
        mock_chat_instance.send_message.return_value = mock_response

        mock_audio = "test_audio_response"
        mock_get_audio_bytes_from_text.return_value = mock_audio
        mock_chatbot.start_chat()
        response = mock_chatbot.send_audio(b"test_audio_data")
        mock_chat_instance.send_message.assert_called_once()
        assert response.message == "Hi user!"
        assert response.bytes == mock_audio

    def test_send_audio_with_error(
        self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock, mock_get_audio_bytes_from_text: MagicMock
    ) -> None:
        mock_response = MagicMock()
        mock_response.parts = [MagicMock(text=None)]
        mock_chat_instance.send_message.return_value = mock_response

        mock_audio = "Failed to send messages to chatbot!"
        mock_get_audio_bytes_from_text.return_value = mock_audio

        mock_chatbot.start_chat()
        response = mock_chatbot.send_audio(b"test_audio_data")
        mock_chat_instance.send_message.assert_called_once()
        assert response.message == "Failed to send message to chatbot!"
        assert response.bytes == mock_audio

    def test_send_audio_with_gtts_error(
        self, mock_chatbot: Chatbot, mock_chat_instance: MagicMock, mock_get_audio_bytes_from_text: MagicMock
    ) -> None:
        mock_chat_instance.send_message.return_value = MagicMock(parts=[MagicMock(text="Hi user!")])
        mock_get_audio_bytes_from_text.side_effect = gTTSError("gTTS error")

        mock_chatbot.start_chat()
        response = mock_chatbot.send_audio(b"test_audio_data")
        mock_chat_instance.send_message.assert_called_once()
        assert response.message == "gTTS error"
        assert response.bytes == ""
