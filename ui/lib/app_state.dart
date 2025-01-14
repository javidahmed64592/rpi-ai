// Flutter imports:
import 'package:flutter/material.dart';

class AppState extends ChangeNotifier {
  String _ip = '127.0.0.1';
  int _port = 5000;
  String _authToken = '';
  String _activePage = 'login';

  String? _notificationState;
  String? _notificationMessage;

  final List<Map<String, dynamic>> _messages = [];

  String get ip => _ip;
  int get port => _port;
  String get fullUrl => 'http://$_ip:$_port';
  String get authToken => _authToken;
  String get activePage => _activePage;
  String? get notificationState => _notificationState;
  String? get notificationMessage => _notificationMessage;

  List<Map<String, dynamic>> get messages => _messages;

  void setIp(String newIp) {
    _ip = newIp;
    notifyListeners();
  }

  void setPort(int newPort) {
    _port = newPort;
    notifyListeners();
  }

  void setAuthToken(String newAuthToken) {
    _authToken = newAuthToken;
    notifyListeners();
  }

  void setActivePage(String newPage) {
    _activePage = newPage;
    notifyListeners();
  }

  void setNotificationError(String? message) {
    _notificationState = 'error';
    _notificationMessage = message;
    notifyListeners();
  }

  void setNotificationWarning(String? message) {
    _notificationState = 'warning';
    _notificationMessage = message;
    notifyListeners();
  }

  void setNotificationInfo(String? message) {
    _notificationState = 'info';
    _notificationMessage = message;
    notifyListeners();
  }

  void clearNotification() {
    _notificationState = null;
    _notificationMessage = null;
    notifyListeners();
  }

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
}
