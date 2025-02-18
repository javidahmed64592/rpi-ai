// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/components/timeout_dialog.dart';

void main() {
  Widget createTimeoutDialog(VoidCallback retryConnection) {
    return MaterialApp(
      home: TimeoutDialog(
        retryConnection: retryConnection,
      ),
    );
  }

  testWidgets('TimeoutDialog displays correct title and content',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      createTimeoutDialog(() {}),
    );

    expect(find.text('Connection Lost'), findsOneWidget);
    expect(find.text('The connection has been lost. Please try again.'),
        findsOneWidget);
    expect(find.text('Retry Connection'), findsOneWidget);
  });

  testWidgets('Retry button triggers retryConnection callback',
      (WidgetTester tester) async {
    bool retryCalled = false;

    await tester.pumpWidget(
      createTimeoutDialog(() {
        retryCalled = true;
      }),
    );

    await tester.tap(find.text('Retry Connection'));
    await tester.pump();

    expect(retryCalled, isTrue);
  });
}
