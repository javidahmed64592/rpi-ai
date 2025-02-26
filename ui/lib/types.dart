// Flutter imports:
import 'package:flutter/material.dart';

// Project imports:
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/message_state.dart';

enum PageType {
  login,
  text,
  speech,
  settings;

  void handlePageChange(AppState appState) {
    switch (this) {
      case PageType.login:
        appState.setPageLogin();
        break;
      case PageType.text:
        appState.setPageText();
        break;
      case PageType.speech:
        appState.setPageSpeech();
        break;
      case PageType.settings:
        appState.setPageSettings();
        break;
    }
  }
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
      case PageType.settings:
        return 'Settings';
      default:
        return 'Error';
    }
  }

  IconData get icon {
    switch (this) {
      case PageType.login:
        return Icons.login;
      case PageType.text:
        return Icons.text_fields;
      case PageType.speech:
        return Icons.mic;
      case PageType.settings:
        return Icons.settings;
      default:
        return Icons.error;
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
