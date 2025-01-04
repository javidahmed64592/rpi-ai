import 'package:flutter/material.dart';

class AppState extends ChangeNotifier {
  String _ip = '127.0.0.1';
  int _port = 5000;

  final List<Map<String, dynamic>> _messages = [
    {'text': 'Hello there!', 'isUserMessage': true},
    {'text': 'Hi! How can I help you?', 'isUserMessage': false},
  ];

  String get ip => _ip;
  int get port => _port;

  List<Map<String, dynamic>> get messages => _messages;

  void setIp(String newIp) {
    _ip = newIp;
    notifyListeners();
  }

  void setPort(int newPort) {
    _port = newPort;
    notifyListeners();
  }

  void addMessage(Map<String, dynamic> message) {
    _messages.add(message);
    notifyListeners();
  }

  void setMessages(List<Map<String, dynamic>> newMessages) {
    _messages
      ..clear()
      ..addAll(newMessages);
    notifyListeners();
  }

  String getFullUrl() {
    return 'http://$_ip:$_port';
  }
}
