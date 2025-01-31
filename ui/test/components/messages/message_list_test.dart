// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/components/messages/message_list.dart';
import 'package:ui/types.dart';

void main() {
  Widget createMessageList(
      List<Map<String, dynamic>> messages, ScrollController? scrollController) {
    return MaterialApp(
      home: Scaffold(
        body: MessageList(
          messages: messages,
          scrollController: scrollController ?? ScrollController(),
          messageType: MessageType.chat,
        ),
      ),
    );
  }

  testWidgets('MessageList displays messages correctly',
      (WidgetTester tester) async {
    final timestamp = DateTime(2023, 10, 1, 14, 30);
    final messages = [
      {
        'text': 'Hello, this is a user message',
        'isUserMessage': true,
        'timestamp': timestamp,
      },
      {
        'text': 'Hello, this is a non-user message',
        'isUserMessage': false,
        'timestamp': timestamp,
      },
    ];

    await tester.pumpWidget(createMessageList(messages, null));

    final userMessageFinder = find.text('Hello, this is a user message');
    final nonUserMessageFinder = find.text('Hello, this is a non-user message');
    final timestampFinder = find.text('01/10/23 | 14:30');

    expect(userMessageFinder, findsOneWidget);
    expect(nonUserMessageFinder, findsOneWidget);
    expect(timestampFinder, findsNWidgets(2));
  });

  testWidgets('MessageList scrolls to the bottom', (WidgetTester tester) async {
    final messages = List.generate(
        20,
        (index) => {
              'text': 'Message $index',
              'isUserMessage': index % 2 == 0,
              'timestamp': DateTime.now(),
            });
    final scrollController = ScrollController();

    await tester.pumpWidget(createMessageList(messages, scrollController));
    await tester.pumpAndSettle();

    expect(scrollController.offset, scrollController.position.maxScrollExtent);
  });
}
