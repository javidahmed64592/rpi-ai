// Flutter imports:
import 'package:flutter/material.dart';

class NotificationState extends ChangeNotifier {
  String? _notificationState;
  String? _notificationMessage;

  String? get notificationState => _notificationState;
  String? get notificationMessage => _notificationMessage;

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
}
