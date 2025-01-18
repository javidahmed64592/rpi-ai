// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/components/messages/message_container.dart';

void main() {
  testWidgets('MessageContainer displays user message correctly',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: MessageContainer(
            message: 'Hello, this is a user message',
            isUserMessage: true,
          ),
        ),
      ),
    );

    final messageFinder = find.text('Hello, this is a user message');
    expect(messageFinder, findsOneWidget);

    await tester.longPress(find.text('Hello, this is a user message'));
    await tester.pumpAndSettle();
    expect(find.text('Copied to clipboard'), findsOneWidget);
  });

  testWidgets('MessageContainer displays non-user message correctly',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: MessageContainer(
            message: 'Hello, this is a non-user message',
            isUserMessage: false,
          ),
        ),
      ),
    );

    final messageFinder = find.text('Hello, this is a non-user message');
    expect(messageFinder, findsOneWidget);

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
