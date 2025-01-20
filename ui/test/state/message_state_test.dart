// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/state/message_state.dart';

void main() {
  group('MessageState', () {
    late MessageState messageState;

    setUp(() {
      messageState = MessageState();
    });

    test('initial values are correct', () {
      expect(messageState.messages.length, 0);
    });

    test('addMessage adds a new message', () {
      final newMessage = {'text': 'Hello, world!', 'isUserMessage': true};
      messageState.addMessage(newMessage);
      expect(messageState.messages.length, 1);
      expect(messageState.messages[0], newMessage);
    });

    test('clearMessages clears all messages', () {
      final messages = [
        {'text': 'Message 1', 'isUserMessage': true},
        {'text': 'Message 2', 'isUserMessage': false},
      ];
      messageState.addMessage(messages[0]);
      messageState.addMessage(messages[1]);
      messageState.clearMessages();
      expect(messageState.messages.length, 0);
    });

    test('removeLastMessage removes the last message', () {
      final messages = [
        {'text': 'Message 1', 'isUserMessage': true},
        {'text': 'Message 2', 'isUserMessage': false},
      ];
      messageState.addMessage(messages[0]);
      messageState.addMessage(messages[1]);
      messageState.removeLastMessage();
      expect(messageState.messages.length, 1);
      expect(messageState.messages[0],
          {'text': 'Message 1', 'isUserMessage': true});
    });

    test('setUserMessage sets the user message', () {
      final userMessage = {'text': 'User message', 'isUserMessage': true};
      messageState.setUserMessage(userMessage);
      expect(messageState.userMessage, userMessage);
    });

    test('setBotMessage sets the bot message', () {
      final botMessage = {'text': 'Bot message', 'isUserMessage': false};
      messageState.setBotMessage(botMessage);
      expect(messageState.botMessage, botMessage);
    });
  });
}
