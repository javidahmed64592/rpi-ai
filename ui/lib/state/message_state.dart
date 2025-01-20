// Flutter imports:
import 'package:flutter/material.dart';

class MessageState extends ChangeNotifier {
  final List<Map<String, dynamic>> _messages = [];
  final Map<String, dynamic> _userMessage = {};
  final Map<String, dynamic> _botMessage = {};

  List<Map<String, dynamic>> get messages => _messages;
  Map<String, dynamic> get userMessage => _userMessage;
  Map<String, dynamic> get botMessage => _botMessage;

  void addMessage(Map<String, dynamic> message) {
    _messages.add(message);
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

  void setUserMessage(Map<String, dynamic> message) {
    _userMessage.clear();
    _userMessage.addAll(message);
    notifyListeners();
  }

  void setBotMessage(Map<String, dynamic> message) {
    _botMessage.clear();
    _botMessage.addAll(message);
    notifyListeners();
  }
}
