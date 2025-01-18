import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ui/components/timeout_dialog.dart';

void main() {
  testWidgets('TimeoutDialog displays correct title and content',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: TimeoutDialog(
          retryConnection: () {},
        ),
      ),
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
      MaterialApp(
        home: TimeoutDialog(
          retryConnection: () {
            retryCalled = true;
          },
        ),
      ),
    );

    await tester.tap(find.text('Retry Connection'));
    await tester.pump();

    expect(retryCalled, isTrue);
  });
}
