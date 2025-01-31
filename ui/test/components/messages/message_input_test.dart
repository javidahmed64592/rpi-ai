// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/messages/message_input.dart';
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/state/notification_state.dart';
import 'package:ui/types.dart';
import 'message_input_test.mocks.dart';

@GenerateMocks([HttpHelper, AppState, MessageState, NotificationState])
void main() {
  late MockHttpHelper mockHttpHelper;
  late MockAppState mockAppState;
  late MockMessageState mockMessageState;
  late MockNotificationState mockNotificationState;

  setUp(() {
    mockHttpHelper = MockHttpHelper();
    mockAppState = MockAppState();
    mockMessageState = MockMessageState();
    mockNotificationState = MockNotificationState();
  });

  Widget createWidgetUnderTest(MessageType messageType,
      {ScrollController? scrollController}) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider<AppState>.value(value: mockAppState),
        ChangeNotifierProvider<MessageState>.value(value: mockMessageState),
        ChangeNotifierProvider<NotificationState>.value(
            value: mockNotificationState),
      ],
      child: MaterialApp(
        home: Scaffold(
          body: ListView(
            controller: scrollController,
            children: [
              MessageInput(
                messageType: messageType,
                httpHelper: mockHttpHelper,
                scrollController: scrollController,
              ),
            ],
          ),
        ),
      ),
    );
  }

  testWidgets('MessageInput sends a message when send button is pressed',
      (WidgetTester tester) async {
    when(mockAppState.fullUrl).thenReturn('http://example.com');
    when(mockAppState.authToken).thenReturn('token');
    when(mockHttpHelper.chat(any, any, any)).thenAnswer((_) async => {
          'text': 'response',
          'isUserMessage': false,
          'timestamp': DateTime.now()
        });

    await tester.pumpWidget(createWidgetUnderTest(MessageType.chat));

    await tester.enterText(find.byType(TextField), 'Hello');
    await tester.tap(find.byIcon(Icons.send));
    await tester.pump();

    verify(mockHttpHelper.chat('http://example.com', 'token', 'Hello'))
        .called(1);
  });

  testWidgets('MessageInput shows error notification on failure',
      (WidgetTester tester) async {
    when(mockAppState.fullUrl).thenReturn('http://example.com');
    when(mockAppState.authToken).thenReturn('token');
    when(mockHttpHelper.chat(any, any, any)).thenAnswer((_) async => {});

    await tester.pumpWidget(createWidgetUnderTest(MessageType.chat));

    await tester.enterText(find.byType(TextField), 'Hello');
    await tester.tap(find.byIcon(Icons.send));
    await tester.pump();

    verify(mockNotificationState
            .setNotificationError('Failed to send message!'))
        .called(1);
  });

  testWidgets('MessageInput scrolls to bottom when message is sent',
      (WidgetTester tester) async {
    final ScrollController scrollController = ScrollController();
    when(mockAppState.fullUrl).thenReturn('http://example.com');
    when(mockAppState.authToken).thenReturn('token');
    when(mockHttpHelper.chat(any, any, any)).thenAnswer((_) async => {
          'text': 'response',
          'isUserMessage': false,
          'timestamp': DateTime.now()
        });

    await tester.pumpWidget(createWidgetUnderTest(MessageType.chat,
        scrollController: scrollController));

    await tester.enterText(find.byType(TextField), 'Hello');
    await tester.tap(find.byIcon(Icons.send));
    await tester.pump();

    expect(scrollController.offset, scrollController.position.maxScrollExtent);
  });
}
