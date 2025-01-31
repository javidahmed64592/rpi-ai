// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/components/messages/message_container.dart';

void main() {
  Widget createMessageContainer({
    required String message,
    required bool isUserMessage,
    required DateTime timestamp,
  }) {
    return MaterialApp(
      home: Scaffold(
        body: MessageContainer(
          message: message,
          isUserMessage: isUserMessage,
          timestamp: timestamp,
        ),
      ),
    );
  }

  testWidgets('MessageContainer displays user message correctly',
      (WidgetTester tester) async {
    final timestamp = DateTime(2023, 10, 1, 14, 30);
    await tester.pumpWidget(
      createMessageContainer(
        message: 'Hello, this is a user message',
        isUserMessage: true,
        timestamp: timestamp,
      ),
    );

    final messageFinder = find.text('Hello, this is a user message');
    final timestampFinder = find.text('01/10/23 | 14:30');
    expect(messageFinder, findsOneWidget);
    expect(timestampFinder, findsOneWidget);

    await tester.longPress(find.text('Hello, this is a user message'));
    await tester.pumpAndSettle();
    expect(find.text('Copied to clipboard'), findsOneWidget);
  });

  testWidgets('MessageContainer displays non-user message correctly',
      (WidgetTester tester) async {
    final timestamp = DateTime(2023, 10, 1, 14, 30);
    await tester.pumpWidget(
      createMessageContainer(
        message: 'Hello, this is a non-user message',
        isUserMessage: false,
        timestamp: timestamp,
      ),
    );

    final messageFinder = find.text('Hello, this is a non-user message');
    final timestampFinder = find.text('01/10/23 | 14:30');
    expect(messageFinder, findsOneWidget);
    expect(timestampFinder, findsOneWidget);

    await tester.longPress(find.text('Hello, this is a non-user message'));
    await tester.pumpAndSettle();
    expect(find.text('Copied to clipboard'), findsOneWidget);
  });

  testWidgets('MessageBox displays message with correct colors',
      (WidgetTester tester) async {
    const message = 'Test message';
    const boxColour = Colors.blue;
    const textColour = Colors.white;

    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: MessageBox(
            message: message,
            boxColour: boxColour,
            textColour: textColour,
          ),
        ),
      ),
    );

    final messageFinder = find.text(message);
    expect(messageFinder, findsOneWidget);

    final container = tester.widget<Container>(find.byType(Container));
    final decoration = container.decoration as BoxDecoration;
    expect(decoration.color, boxColour);

    final text = tester.widget<Text>(find.text(message));
    expect(text.style?.color, textColour);
  });
}
