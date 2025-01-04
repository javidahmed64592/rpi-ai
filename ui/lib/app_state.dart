import 'package:flutter/material.dart';

class AppState extends ChangeNotifier {
  String _ip = '127.0.0.1';
  int _port = 5000;

  String get ip => _ip;
  int get port => _port;

  void setIp(String newIp) {
    _ip = newIp;
    notifyListeners();
  }

  void setPort(int newPort) {
    _port = newPort;
    notifyListeners();
  }

  String getFullUrl() {
    return 'http://$_ip:$_port';
  }
}
