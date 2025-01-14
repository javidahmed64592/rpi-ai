import 'package:flutter_test/flutter_test.dart';
import 'package:ui/state/notification_state.dart';

void main() {
  group('NotificationState', () {
    test('initial state is null', () {
      final notificationState = NotificationState();
      expect(notificationState.notificationState, isNull);
      expect(notificationState.notificationMessage, isNull);
    });

    test('setNotificationError sets state to error', () {
      final notificationState = NotificationState();
      notificationState.setNotificationError('Error occurred');
      expect(notificationState.notificationState, 'error');
      expect(notificationState.notificationMessage, 'Error occurred');
    });

    test('setNotificationWarning sets state to warning', () {
      final notificationState = NotificationState();
      notificationState.setNotificationWarning('Warning issued');
      expect(notificationState.notificationState, 'warning');
      expect(notificationState.notificationMessage, 'Warning issued');
    });

    test('setNotificationInfo sets state to info', () {
      final notificationState = NotificationState();
      notificationState.setNotificationInfo('Information provided');
      expect(notificationState.notificationState, 'info');
      expect(notificationState.notificationMessage, 'Information provided');
    });

    test('clearNotification clears the state', () {
      final notificationState = NotificationState();
      notificationState.setNotificationError('Error occurred');
      notificationState.clearNotification();
      expect(notificationState.notificationState, isNull);
      expect(notificationState.notificationMessage, isNull);
    });
  });
}
