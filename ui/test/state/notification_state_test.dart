// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/state/notification_state.dart';
import 'package:ui/types.dart';

void main() {
  group('NotificationState', () {
    late NotificationState notificationState;

    setUp(() {
      notificationState = NotificationState();
    });
    test('initial state is null', () {
      expect(notificationState.notificationState, isNull);
      expect(notificationState.notificationMessage, isNull);
    });

    test('setNotificationError sets state to error', () {
      notificationState.setNotificationError('Error occurred');
      expect(notificationState.notificationState, NotificationType.error);
      expect(notificationState.notificationMessage, 'Error occurred');
    });

    test('setNotificationWarning sets state to warning', () {
      notificationState.setNotificationWarning('Warning issued');
      expect(notificationState.notificationState, NotificationType.warning);
      expect(notificationState.notificationMessage, 'Warning issued');
    });

    test('setNotificationInfo sets state to info', () {
      notificationState.setNotificationInfo('Information provided');
      expect(notificationState.notificationState, NotificationType.info);
      expect(notificationState.notificationMessage, 'Information provided');
    });

    test('clearNotification clears the state', () {
      notificationState.setNotificationError('Error occurred');
      notificationState.clearNotification();
      expect(notificationState.notificationState, isNull);
      expect(notificationState.notificationMessage, isNull);
    });
  });
}
