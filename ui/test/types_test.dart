// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

// Project imports:
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/types.dart';
import 'types_test.mocks.dart';

@GenerateMocks([HttpHelper, MessageState])
void main() {
  group('PageType', () {
    test('title returns correct values', () {
      expect(PageType.login.title, 'Login');
      expect(PageType.chat.title, 'Chat Mode');
      expect(PageType.command.title, 'Command Mode');
    });
  });

  group('NotificationType', () {
    test('values are correct', () {
      expect(NotificationType.values.length, 3);
      expect(NotificationType.error, NotificationType.values[0]);
      expect(NotificationType.warning, NotificationType.values[1]);
      expect(NotificationType.info, NotificationType.values[2]);
    });
  });

  group('MessageType', () {
    final mockHttpHelper = MockHttpHelper();
    final mockMessageState = MockMessageState();

    test('sendMessage calls correct methods', () async {
      when(mockHttpHelper.chat(any, any, any))
          .thenAnswer((_) async => {'response': 'chat'});
      when(mockHttpHelper.command(any, any, any))
          .thenAnswer((_) async => {'response': 'command'});

      var chatResponse = await MessageType.chat
          .sendMessage(mockHttpHelper, 'url', 'token', 'message');
      var commandResponse = await MessageType.command
          .sendMessage(mockHttpHelper, 'url', 'token', 'message');

      expect(chatResponse, {'response': 'chat'});
      expect(commandResponse, {'response': 'command'});
    });

    test('handleAddMessage calls correct methods', () {
      var userMessageDict = {'message': 'test'};

      MessageType.chat.handleAddMessage(mockMessageState, userMessageDict);
      verify(mockMessageState.addMessage(userMessageDict)).called(1);

      MessageType.command.handleAddMessage(mockMessageState, userMessageDict);
      verify(mockMessageState.clearUserMessage()).called(1);
      verify(mockMessageState.clearBotMessage()).called(1);
      verify(mockMessageState.setUserMessage(userMessageDict)).called(1);
    });

    test('handleFailedMessage calls correct methods', () {
      MessageType.chat.handleFailedMessage(mockMessageState);
      verify(mockMessageState.removeLastMessage()).called(1);

      MessageType.command.handleFailedMessage(mockMessageState);
      verify(mockMessageState.clearUserMessage()).called(1);
      verify(mockMessageState.clearBotMessage()).called(1);
    });
  });
}
