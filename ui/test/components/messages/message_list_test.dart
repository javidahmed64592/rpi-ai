import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ui/components/messages/message_list.dart';

void main() {
  testWidgets('MessageList displays messages correctly',
      (WidgetTester tester) async {
    final messages = [
      {'text': 'Hello, this is a user message', 'isUserMessage': true},
      {'text': 'Hello, this is a non-user message', 'isUserMessage': false},
    ];

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: MessageList(
            messages: messages,
            scrollController: ScrollController(),
          ),
        ),
      ),
    );

    final userMessageFinder = find.text('Hello, this is a user message');
    final nonUserMessageFinder = find.text('Hello, this is a non-user message');

    expect(userMessageFinder, findsOneWidget);
    expect(nonUserMessageFinder, findsOneWidget);
  });

  testWidgets('MessageList scrolls to the bottom', (WidgetTester tester) async {
    final messages = List.generate(20,
        (index) => {'text': 'Message $index', 'isUserMessage': index % 2 == 0});
    final scrollController = ScrollController();

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: MessageList(
            messages: messages,
            scrollController: scrollController,
          ),
        ),
      ),
    );

    expect(scrollController.offset, scrollController.position.maxScrollExtent);
  });
}
