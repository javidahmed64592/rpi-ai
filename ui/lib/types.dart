// Project imports:
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/state/message_state.dart';

enum PageType {
  login,
  text,
  speech,
}

extension PageTypeExtension on PageType {
  String get title {
    switch (this) {
      case PageType.login:
        return 'Login';
      case PageType.text:
        return 'Chat';
      case PageType.speech:
        return 'Speech';
    }
  }
}

enum NotificationType {
  error,
  warning,
  info,
}

enum MessageType {
  text;

  Future<Map<String, dynamic>> sendMessage(HttpHelper httpHelper, String url,
      String token, String userMessage) async {
    switch (this) {
      case MessageType.text:
        return await httpHelper.chat(url, token, userMessage);
    }
  }

  void handleAddMessage(
      MessageState messageState, Map<String, dynamic> userMessageDict) {
    switch (this) {
      case MessageType.text:
        messageState.addMessage(userMessageDict);
        break;
    }
  }

  void handleFailedMessage(MessageState messageState) {
    switch (this) {
      case MessageType.text:
        messageState.removeLastMessage();
        break;
    }
  }
}
