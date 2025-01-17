// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/state/app_state.dart';

void main() {
  group('AppState', () {
    late AppState appState;

    setUp(() {
      appState = AppState();
    });

    test('initial values are correct', () {
      expect(appState.ip, '127.0.0.1');
      expect(appState.port, 5000);
      expect(appState.authToken, '');
      expect(appState.activePage, 'login');
    });

    test('setIp updates the IP address', () {
      appState.setIp('192.168.1.1');
      expect(appState.ip, '192.168.1.1');
    });

    test('setPort updates the port', () {
      appState.setPort(8080);
      expect(appState.port, 8080);
    });

    test('setAuthToken updates the auth token', () {
      appState.setAuthToken('newToken');
      expect(appState.authToken, 'newToken');
    });

    test('setActivePage updates the active page', () {
      appState.setActivePage('message');
      expect(appState.activePage, 'message');
    });

    test('getFullUrl returns the correct URL', () {
      expect(appState.fullUrl, 'http://127.0.0.1:5000');
      appState.setIp('192.168.1.1');
      appState.setPort(8080);
      expect(appState.fullUrl, 'http://192.168.1.1:8080');
    });
  });
}
