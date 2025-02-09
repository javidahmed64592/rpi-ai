// Flutter imports:
import 'package:flutter/material.dart';

// Project imports:
import 'package:ui/types.dart';

class AppState extends ChangeNotifier {
  String _ip = '127.0.0.1';
  int _port = 5000;
  String _authToken = '';
  PageType _activePage = PageType.login;
  bool _connected = false;

  String get ip => _ip;
  int get port => _port;
  String get fullUrl => 'http://$_ip:$_port';
  String get authToken => _authToken;
  PageType get activePage => _activePage;
  bool get connected => _connected;

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

  void setActivePage(PageType newPage) {
    _activePage = newPage;
    notifyListeners();
  }

  void toggleActivePage() {
    if (_activePage == PageType.text) {
      setActivePage(PageType.speech);
    } else if (_activePage == PageType.speech) {
      setActivePage(PageType.text);
    }
    notifyListeners();
  }

  void setConnected(bool newConnected) {
    _connected = newConnected;
    notifyListeners();
  }
}
