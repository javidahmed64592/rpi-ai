// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/components/messages/message_container.dart';
import 'package:ui/components/messages/message_list.dart';

void main() {
  Widget createMessageList(
      List<Map<String, dynamic>> messages, ScrollController? scrollController) {
    return MaterialApp(
      home: Scaffold(
        body: MessageList(
          messages: messages,
          scrollController: scrollController ?? ScrollController(),
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
        'timestamp': timestamp,
        'isUserMessage': true,
      },
      {
        'text': 'Hello, this is a non-user message',
        'timestamp': timestamp,
        'isUserMessage': false,
      },
    ];

    await tester.pumpWidget(createMessageList(messages, null));

    final userMessageFinder = find
        .descendant(
          of: find.byWidgetPredicate((widget) =>
              widget is MessageContainer &&
              widget.message == 'Hello, this is a user message'),
          matching: find.byType(RichText),
        )
        .first;
    final nonUserMessageFinder = find
        .descendant(
          of: find.byWidgetPredicate((widget) =>
              widget is MessageContainer &&
              widget.message == 'Hello, this is a non-user message'),
          matching: find.byType(RichText),
        )
        .first;
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
              'timestamp': DateTime.now(),
              'isUserMessage': index % 2 == 0,
            });
    final scrollController = ScrollController();

    await tester.pumpWidget(createMessageList(messages, scrollController));
    await tester.pumpAndSettle();

    expect(scrollController.offset, scrollController.position.maxScrollExtent);
  });
}
