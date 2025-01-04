import 'package:flutter/material.dart';

class AppState extends ChangeNotifier {
  String _ip = '127.0.0.1';
  int _port = 5000;

  final List<Map<String, dynamic>> _messages = [
    {'text': 'Hello!', 'isUserMessage': true},
    {'text': 'Hi there!', 'isUserMessage': false},
    {'text': 'How are you?', 'isUserMessage': true},
    {'text': 'I am good, thanks!', 'isUserMessage': false},
    {'text': 'What are you doing?', 'isUserMessage': true},
    {'text': 'Just working on a project.', 'isUserMessage': false},
    {'text': 'That sounds interesting!', 'isUserMessage': true},
    {'text': 'Yes, it is!', 'isUserMessage': false},
    {'text': 'Can you tell me more about it?', 'isUserMessage': true},
    {'text': 'Sure, it is about AI and Flutter.', 'isUserMessage': false},
    {'text': 'Wow, that is cool!', 'isUserMessage': true},
    {'text': 'Thank you!', 'isUserMessage': false},
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

  String getFullUrl() {
    return 'http://$_ip:$_port';
  }
}
