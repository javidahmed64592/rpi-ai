// Flutter imports:
import 'package:flutter/material.dart';

class MessageState extends ChangeNotifier {
  final List<Map<String, dynamic>> _messages = [];

  List<Map<String, dynamic>> get messages => _messages;

  void addMessage(Map<String, dynamic> message) {
    _messages.add(message);
    notifyListeners();
  }

  void addMessages(List<Map<String, dynamic>> messages) {
    _messages.addAll(messages);
    notifyListeners();
  }

  void clearMessages() {
    _messages.clear();
    notifyListeners();
  }

  void removeLastMessage() {
    if (_messages.isNotEmpty) {
      _messages.removeLast();
      notifyListeners();
    }
  }

  void initialiseChat(List<Map<String, dynamic>> messages) {
    clearMessages();
    addMessages(messages);
  }
}
