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
          timestamp: timestamp,
          isUserMessage: isUserMessage,
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
        timestamp: timestamp,
        isUserMessage: true,
      ),
    );

    final richTextFinder = find.descendant(
      of: find.byType(MessageBox),
      matching: find.byType(RichText),
    );
    expect(richTextFinder, findsOneWidget);

    final RichText richTextWidget = tester.widget<RichText>(richTextFinder);
    final TextSpan textSpan = richTextWidget.text as TextSpan;

    expect(textSpan.toPlainText(), contains('Hello, this is a user message'));

    final timestampFinder = find.text('01/10/23 | 14:30');
    expect(timestampFinder, findsOneWidget);

    await tester.longPress(richTextFinder);
    await tester.pumpAndSettle();
    expect(find.text('Copied to clipboard'), findsOneWidget);
  });

  testWidgets('MessageContainer displays non-user message correctly',
      (WidgetTester tester) async {
    final timestamp = DateTime(2023, 10, 1, 14, 30);
    await tester.pumpWidget(
      createMessageContainer(
        message: 'Hello, this is a non-user message',
        timestamp: timestamp,
        isUserMessage: false,
      ),
    );

    final richTextFinder = find.descendant(
      of: find.byType(MessageBox),
      matching: find.byType(RichText),
    );
    expect(richTextFinder, findsOneWidget);

    final RichText richTextWidget = tester.widget<RichText>(richTextFinder);
    final TextSpan textSpan = richTextWidget.text as TextSpan;

    expect(
        textSpan.toPlainText(), contains('Hello, this is a non-user message'));

    final timestampFinder = find.text('01/10/23 | 14:30');
    expect(timestampFinder, findsOneWidget);

    await tester.longPress(richTextFinder);
    await tester.pumpAndSettle();
    expect(find.text('Copied to clipboard'), findsOneWidget);
  });

  testWidgets('MessageContainer displays formatted text correctly',
      (WidgetTester tester) async {
    final timestamp = DateTime(2023, 10, 1, 14, 30);
    await tester.pumpWidget(
      createMessageContainer(
        message:
            'This is **bold** text\n* Bullet point 1\n* Bullet point 2\nThis is ***bold and italic*** text',
        timestamp: timestamp,
        isUserMessage: true,
      ),
    );

    final richTextFinder = find.descendant(
      of: find.byType(MessageBox),
      matching: find.byType(RichText),
    );
    expect(richTextFinder, findsOneWidget);

    final RichText richTextWidget = tester.widget<RichText>(richTextFinder);
    final TextSpan textSpan = richTextWidget.text as TextSpan;

    expect(textSpan.toPlainText(),
        'This is bold text\n- Bullet point 1\n- Bullet point 2\nThis is bold and italic text');
  });
}
