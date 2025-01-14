// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/components/notifications.dart';

void main() {
  testWidgets('NotificationPopup displays message and icon',
      (WidgetTester tester) async {
    const message = 'Test message';
    const backgroundColor = Colors.red;
    const icon = Icons.info;

    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: NotificationPopup(
            message: message,
            backgroundColor: backgroundColor,
            icon: icon,
          ),
        ),
      ),
    );

    expect(find.text(message), findsOneWidget);
    expect(find.byIcon(icon), findsOneWidget);
  });

  testWidgets('NotificationError displays error message',
      (WidgetTester tester) async {
    const message = 'Error occurred';

    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: NotificationError(message: message),
        ),
      ),
    );

    expect(find.text(message), findsOneWidget);
    expect(find.byIcon(Icons.error), findsOneWidget);
  });

  testWidgets('NotificationWarning displays warning message',
      (WidgetTester tester) async {
    const message = 'Warning issued';

    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: NotificationWarning(message: message),
        ),
      ),
    );

    expect(find.text(message), findsOneWidget);
    expect(find.byIcon(Icons.warning), findsOneWidget);
  });

  testWidgets('NotificationInfo displays info message',
      (WidgetTester tester) async {
    const message = 'Information provided';

    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: NotificationInfo(message: message),
        ),
      ),
    );

    expect(find.text(message), findsOneWidget);
    expect(find.byIcon(Icons.info), findsOneWidget);
  });

  testWidgets(
      'NotificationPopup calls onClose callback when close icon is tapped',
      (WidgetTester tester) async {
    bool onCloseCalled = false;

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: NotificationPopup(
            message: 'Test message',
            backgroundColor: Colors.red,
            icon: Icons.info,
            onClose: () {
              onCloseCalled = true;
            },
          ),
        ),
      ),
    );

    await tester.tap(find.byIcon(Icons.close));
    await tester.pump();

    expect(onCloseCalled, isTrue);
  });
}
