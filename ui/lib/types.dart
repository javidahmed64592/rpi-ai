// Project imports:
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/state/message_state.dart';

enum PageType {
  login,
  chat,
  command,
}

extension PageTypeExtension on PageType {
  String get title {
    switch (this) {
      case PageType.login:
        return 'Login';
      case PageType.chat:
        return 'Chat Mode';
      case PageType.command:
        return 'Command Mode';
    }
  }
}

enum NotificationType {
  error,
  warning,
  info,
}

enum MessageType {
  chat,
  command;

  Future<Map<String, dynamic>> sendMessage(HttpHelper httpHelper, String url,
      String token, String userMessage) async {
    switch (this) {
      case MessageType.chat:
        return await httpHelper.chat(url, token, userMessage);
      case MessageType.command:
        return await httpHelper.command(url, token, userMessage);
    }
  }

  void handleAddMessage(
      MessageState messageState, Map<String, dynamic> userMessageDict) {
    switch (this) {
      case MessageType.chat:
        messageState.addMessage(userMessageDict);
        break;
      case MessageType.command:
        messageState.clearUserMessage();
        messageState.clearBotMessage();
        messageState.setUserMessage(userMessageDict);
        break;
    }
  }

  void handleFailedMessage(MessageState messageState) {
    switch (this) {
      case MessageType.chat:
        messageState.removeLastMessage();
        break;
      case MessageType.command:
        messageState.clearUserMessage();
        messageState.clearBotMessage();
        break;
    }
  }
}
