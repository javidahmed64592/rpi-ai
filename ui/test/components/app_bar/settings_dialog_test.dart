// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/components/app_bar/settings_dialog.dart';

void main() {
  testWidgets('SettingsDialog displays Close button',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SettingsDialog(),
        ),
      ),
    );

    expect(find.text('Close'), findsOneWidget);
  });

  testWidgets('SettingsDialog closes when Close button is pressed',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SettingsDialog(),
        ),
      ),
    );

    expect(find.byType(AlertDialog), findsOneWidget);

    await tester.tap(find.text('Close'));
    await tester.pumpAndSettle();

    expect(find.byType(AlertDialog), findsNothing);
  });

  testWidgets('SettingsButton opens SettingsDialog',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SettingsButton(),
        ),
      ),
    );

    await tester.tap(find.byType(SettingsButton));
    await tester.pumpAndSettle();

    expect(find.byType(SettingsDialog), findsOneWidget);
  });
}
