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
  late MockHttpHelper mockHttpHelper;

  setUp(() {
    mockHttpHelper = MockHttpHelper();
  });

  group('PageType', () {
    test('title returns correct values', () {
      expect(PageType.login.title, 'Login');
      expect(PageType.text.title, 'Chat');
      expect(PageType.speech.title, 'Speech');
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
    final mockMessageState = MockMessageState();

    test('sendMessage calls correct methods', () async {
      when(mockHttpHelper.chat(any, any, any))
          .thenAnswer((_) async => {'response': 'chat'});

      var chatResponse = await MessageType.text
          .sendMessage(mockHttpHelper, 'url', 'token', 'message');

      expect(chatResponse, {'response': 'chat'});
    });

    test('handleAddMessage calls correct methods', () {
      var userMessageDict = {'message': 'test'};

      MessageType.text.handleAddMessage(mockMessageState, userMessageDict);
      verify(mockMessageState.addMessage(userMessageDict)).called(1);
    });

    test('handleFailedMessage calls correct methods', () {
      MessageType.text.handleFailedMessage(mockMessageState);
      verify(mockMessageState.removeLastMessage()).called(1);
    });
  });
}
