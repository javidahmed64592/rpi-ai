import 'package:flutter_test/flutter_test.dart';
import 'package:ui/app_state.dart';

void main() {
  group('AppState', () {
    late AppState appState;

    setUp(() {
      appState = AppState();
    });

    test('initial values are correct', () {
      expect(appState.ip, '127.0.0.1');
      expect(appState.port, 5000);
      expect(appState.messages.length, 1);
      expect(appState.messages[0]['text'],
          'Failed to retrieve messages! Please check IP and port.');
      expect(appState.messages[0]['isUserMessage'], false);
    });

    test('setIp updates the IP address', () {
      appState.setIp('192.168.1.1');
      expect(appState.ip, '192.168.1.1');
    });

    test('setPort updates the port', () {
      appState.setPort(8080);
      expect(appState.port, 8080);
    });

    test('addMessage adds a new message', () {
      final newMessage = {'text': 'Hello, world!', 'isUserMessage': true};
      appState.addMessage(newMessage);
      expect(appState.messages.length, 2);
      expect(appState.messages[1], newMessage);
    });

    test('setMessages updates the messages list', () {
      final newMessages = [
        {'text': 'New message 1', 'isUserMessage': true},
        {'text': 'New message 2', 'isUserMessage': false},
      ];
      appState.setMessages(newMessages);
      expect(appState.messages.length, 2);
      expect(appState.messages, newMessages);
    });

    test('setMessages with null does not update the messages list', () {
      final originalMessages =
          List<Map<String, dynamic>>.from(appState.messages);
      appState.setMessages(null);
      expect(appState.messages, originalMessages);
    });

    test('getFullUrl returns the correct URL', () {
      expect(appState.getFullUrl(), 'http://127.0.0.1:5000');
      appState.setIp('192.168.1.1');
      appState.setPort(8080);
      expect(appState.getFullUrl(), 'http://192.168.1.1:8080');
    });
  });
}
