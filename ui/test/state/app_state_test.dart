// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/state/app_state.dart';
import 'package:ui/types.dart';

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
      expect(appState.activePage, PageType.login);
      expect(appState.connected, false);
      expect(appState.isBusy, false);
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

    test('setConnected updates the connection status', () {
      appState.setConnected(true);
      expect(appState.connected, true);
    });

    test('setActivePage sets the active page', () {
      appState.setActivePage(PageType.text);
      expect(appState.activePage, PageType.text);
    });

    test('setActivePage does not update the active page if busy', () {
      appState.setIsBusy(true);
      appState.setActivePage(PageType.text);
      expect(appState.activePage, PageType.login);
    });

    test('setPageLogin sets the active page to login', () {
      appState.setPageLogin();
      expect(appState.activePage, PageType.login);
    });

    test('setPageText sets the active page to text', () {
      appState.setPageText();
      expect(appState.activePage, PageType.text);
    });

    test('setPageSpeech sets the active page to speech', () {
      appState.setPageSpeech();
      expect(appState.activePage, PageType.speech);
    });

    test('setPageSettings sets the active page to settings', () {
      appState.setPageSettings();
      expect(appState.activePage, PageType.settings);
    });

    test('getFullUrl returns the correct URL', () {
      expect(appState.fullUrl, 'http://127.0.0.1:5000');
      appState.setIp('192.168.1.1');
      appState.setPort(8080);
      expect(appState.fullUrl, 'http://192.168.1.1:8080');
    });

    test('setIsBusy', () {
      appState.setIsBusy(true);
      expect(appState.isBusy, true);
    });
  });
}
