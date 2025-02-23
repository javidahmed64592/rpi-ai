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
        isUserMessage: false,
        timestamp: timestamp,
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

  testWidgets('MessageContainer displays bold text correctly',
      (WidgetTester tester) async {
    final timestamp = DateTime(2023, 10, 1, 14, 30);
    await tester.pumpWidget(
      createMessageContainer(
        message: 'This is **bold** text',
        isUserMessage: true,
        timestamp: timestamp,
      ),
    );

    final richTextFinder = find.descendant(
      of: find.byType(MessageBox),
      matching: find.byType(RichText),
    );
    expect(richTextFinder, findsOneWidget);

    final RichText richTextWidget = tester.widget<RichText>(richTextFinder);
    final TextSpan textSpan = richTextWidget.text as TextSpan;

    expect(textSpan.children, isNotNull);
    expect(textSpan.children!.length, 3);

    final TextSpan normalTextSpan1 = textSpan.children![0] as TextSpan;
    final TextSpan boldTextSpan = textSpan.children![1] as TextSpan;
    final TextSpan normalTextSpan2 = textSpan.children![2] as TextSpan;

    expect(normalTextSpan1.text, 'This is ');
    expect(normalTextSpan1.style?.fontWeight, null);
    expect(boldTextSpan.text, 'bold');
    expect(boldTextSpan.style?.fontWeight, FontWeight.bold);
    expect(normalTextSpan2.text, ' text');
    expect(normalTextSpan2.style?.fontWeight, null);
  });

  testWidgets('MessageContainer displays bullet points correctly',
      (WidgetTester tester) async {
    final timestamp = DateTime(2023, 10, 1, 14, 30);
    await tester.pumpWidget(
      createMessageContainer(
        message: '* Bullet point 1\n* Bullet point 2',
        isUserMessage: true,
        timestamp: timestamp,
      ),
    );

    final richTextFinder = find.descendant(
      of: find.byType(MessageBox),
      matching: find.byType(RichText),
    );
    expect(richTextFinder, findsOneWidget);

    final RichText richTextWidget = tester.widget<RichText>(richTextFinder);
    final TextSpan textSpan = richTextWidget.text as TextSpan;

    expect(textSpan.children, isNotNull);

    final TextSpan bulletPoint1 = textSpan.children![0] as TextSpan;
    final TextSpan bulletPoint2 = textSpan.children![2] as TextSpan;

    expect(bulletPoint1.text, '- Bullet point 1');
    expect(bulletPoint2.text, '- Bullet point 2');
  });
}
