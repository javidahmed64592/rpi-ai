// Flutter imports:
import 'package:flutter/material.dart';

// Project imports:
import 'package:ui/types.dart';

class NotificationState extends ChangeNotifier {
  NotificationType? _notificationState;
  String? _notificationMessage;

  NotificationType? get notificationState => _notificationState;
  String? get notificationMessage => _notificationMessage;

  void setNotificationError(String? message) {
    _notificationState = NotificationType.error;
    _notificationMessage = message;
    notifyListeners();
  }

  void setNotificationWarning(String? message) {
    _notificationState = NotificationType.warning;
    _notificationMessage = message;
    notifyListeners();
  }

  void setNotificationInfo(String? message) {
    _notificationState = NotificationType.info;
    _notificationMessage = message;
    notifyListeners();
  }

  void clearNotification() {
    _notificationState = null;
    _notificationMessage = null;
    notifyListeners();
  }
}
