// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/app_bar/custom_app_bar.dart';
import 'package:ui/components/timeout_dialog.dart';
import 'package:ui/pages/main_page.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/state/notification_state.dart';
import 'package:ui/state/settings_state.dart';

void main() {
  late AppState appState;
  late NotificationState notificationState;

  setUp(() {
    appState = AppState();
    notificationState = NotificationState();
  });

  Widget createMainPage() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => appState),
        ChangeNotifierProvider(create: (context) => MessageState()),
        ChangeNotifierProvider(create: (context) => notificationState),
        ChangeNotifierProvider(create: (context) => SettingsState()),
      ],
      child: const MaterialApp(
        home: MainPage(),
      ),
    );
  }

  testWidgets('MainPage displays CustomAppBar', (WidgetTester tester) async {
    await tester.pumpWidget(createMainPage());
    expect(find.byType(CustomAppBar), findsOneWidget);
  });

  testWidgets('MainPage displays MenuDrawer button',
      (WidgetTester tester) async {
    await tester.pumpWidget(createMainPage());
    appState.setPageText();
    await tester.pump();
    expect(find.byIcon(Icons.menu), findsOneWidget);
  });

  testWidgets('MainPage does not display MenuDrawer on login page',
      (WidgetTester tester) async {
    await tester.pumpWidget(createMainPage());
    appState.setPageLogin();
    await tester.pump();
    expect(find.byIcon(Icons.menu), findsNothing);
  });

  testWidgets('MainPage displays error notification',
      (WidgetTester tester) async {
    await tester.pumpWidget(createMainPage());
    notificationState.setNotificationError('Test error');
    await tester.pump();
    expect(find.text('Test error'), findsOneWidget);
  });

  testWidgets('MainPage displays info notification',
      (WidgetTester tester) async {
    await tester.pumpWidget(createMainPage());
    notificationState.setNotificationInfo('Test info');
    await tester.pump();
    expect(find.text('Test info'), findsOneWidget);
  });

  testWidgets('MainPage displays warning notification',
      (WidgetTester tester) async {
    await tester.pumpWidget(createMainPage());
    notificationState.setNotificationWarning('Test warning');
    await tester.pump();
    expect(find.text('Test warning'), findsOneWidget);
  });

  testWidgets('MainPage displays TimeoutDialog when disconnected',
      (WidgetTester tester) async {
    await tester.pumpWidget(createMainPage());
    appState.setPageText();
    appState.setConnected(false);
    await tester.pump();
    expect(find.byType(TimeoutDialog), findsOneWidget);
  });
}
