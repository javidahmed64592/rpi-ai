// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/app_bar/logout_button.dart';
import 'package:ui/components/app_bar/settings_dialog.dart';
import 'package:ui/pages/home_page.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/notification_state.dart';

void main() {
  Widget createHomePage(AppState appState) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: appState),
        ChangeNotifierProvider(create: (context) => NotificationState()),
      ],
      child: const MaterialApp(
        home: HomePage(),
      ),
    );
  }

  testWidgets('HomePage displays AppBar', (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage(AppState()));
    expect(find.byType(AppBar), findsOneWidget);
  });

  testWidgets('HomePage displays title', (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage(AppState()));
    expect(find.text('Gemini'), findsOneWidget);
  });

  testWidgets('HomePage displays SettingsButton', (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage('message');
    await tester.pumpWidget(createHomePage(appState));
    expect(find.byType(SettingsButton), findsOneWidget);
  });

  testWidgets('SettingsButton opens SettingsDialog',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage('message');
    await tester.pumpWidget(createHomePage(appState));

    await tester.tap(find.byType(SettingsButton));
    await tester.pumpAndSettle();
    expect(find.byType(SettingsDialog), findsOneWidget);
  });

  testWidgets('HomePage does not display SettingsButton on login page',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage('login');
    await tester.pumpWidget(createHomePage(appState));
    expect(find.byType(SettingsButton), findsNothing);
  });

  testWidgets('HomePage displays LogoutButton', (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage('message');
    await tester.pumpWidget(createHomePage(appState));
    expect(find.byType(LogoutButton), findsOneWidget);
  });

  testWidgets('HomePage does not display LogoutButton on login page',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage('login');
    await tester.pumpWidget(createHomePage(appState));
    expect(find.byType(LogoutButton), findsNothing);
  });
}
