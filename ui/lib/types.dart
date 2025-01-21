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

enum MessageType {
  chat,
  command,
}
