// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/app_bar/settings_dialog.dart';
import 'package:ui/state/settings_state.dart';

void main() {
  testWidgets('SettingsButton opens SettingsDialog',
      (WidgetTester tester) async {
    final settingsState = SettingsState();

    await tester.pumpWidget(
      ChangeNotifierProvider<SettingsState>.value(
        value: settingsState,
        child: const MaterialApp(
          home: Scaffold(
            body: SettingsButton(),
          ),
        ),
      ),
    );

    await tester.tap(find.byType(SettingsButton));
    await tester.pumpAndSettle();

    expect(find.byType(SettingsDialog), findsOneWidget);
  });

  testWidgets('SettingsDialog displays Update button',
      (WidgetTester tester) async {
    final settingsState = SettingsState();

    await tester.pumpWidget(
      ChangeNotifierProvider<SettingsState>.value(
        value: settingsState,
        child: const MaterialApp(
          home: Scaffold(
            body: SettingsDialog(),
          ),
        ),
      ),
    );

    expect(find.text('Update'), findsOneWidget);
  });

  testWidgets(
      'SettingsDialog updates SettingsState when Update button is pressed',
      (WidgetTester tester) async {
    final settingsState = SettingsState();

    await tester.pumpWidget(
      ChangeNotifierProvider<SettingsState>.value(
        value: settingsState,
        child: const MaterialApp(
          home: Scaffold(
            body: SettingsDialog(),
          ),
        ),
      ),
    );

    expect(find.byType(AlertDialog), findsOneWidget);

    await tester.enterText(find.byType(TextField).at(0), 'newModel');
    await tester.enterText(
        find.byType(TextField).at(1), 'newSystemInstruction');
    await tester.enterText(find.byType(TextField).at(2), '5');
    await tester.enterText(find.byType(TextField).at(3), '1500');
    await tester.enterText(find.byType(TextField).at(4), '1.5');

    await tester.tap(find.text('Update'));
    await tester.pumpAndSettle();

    expect(settingsState.model, 'newModel');
    expect(settingsState.systemInstruction, 'newSystemInstruction');
    expect(settingsState.candidateCount, 5);
    expect(settingsState.maxOutputTokens, 1500);
    expect(settingsState.temperature, 1.5);

    expect(find.byType(AlertDialog), findsNothing);
  });

  testWidgets('SettingsDialog displays Close button',
      (WidgetTester tester) async {
    final settingsState = SettingsState();

    await tester.pumpWidget(
      ChangeNotifierProvider<SettingsState>.value(
        value: settingsState,
        child: const MaterialApp(
          home: Scaffold(
            body: SettingsDialog(),
          ),
        ),
      ),
    );

    expect(find.text('Close'), findsOneWidget);
  });

  testWidgets('SettingsDialog closes when Close button is pressed',
      (WidgetTester tester) async {
    final settingsState = SettingsState();

    await tester.pumpWidget(
      ChangeNotifierProvider<SettingsState>.value(
        value: settingsState,
        child: const MaterialApp(
          home: Scaffold(
            body: SettingsDialog(),
          ),
        ),
      ),
    );

    expect(find.byType(AlertDialog), findsOneWidget);

    await tester.tap(find.text('Close'));
    await tester.pumpAndSettle();

    expect(find.byType(AlertDialog), findsNothing);
  });
}
