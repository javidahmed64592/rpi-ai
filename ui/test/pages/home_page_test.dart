// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/app_bar/logout_button.dart';
import 'package:ui/components/app_bar/switch_chat_mode.dart';
import 'package:ui/components/timeout_dialog.dart';
import 'package:ui/pages/home_page.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/state/notification_state.dart';
import 'package:ui/types.dart';

void main() {
  Widget createHomePage(AppState appState) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => appState),
        ChangeNotifierProvider(create: (context) => MessageState()),
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
    expect(find.text('Login'), findsOneWidget);
  });

  testWidgets('HomePage displays SwitchChatMode', (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.chat);
    await tester.pumpWidget(createHomePage(appState));
    expect(find.byType(SwitchChatMode), findsOneWidget);
  });

  testWidgets('HomePage does not display SwitchChatMode on login page',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.login);
    await tester.pumpWidget(createHomePage(appState));
    expect(find.byType(SwitchChatMode), findsNothing);
  });

  testWidgets('SwitchChatMode changes page', (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.chat);
    await tester.pumpWidget(createHomePage(appState));
    await tester.tap(find.byType(SwitchChatMode));
    await tester.pump();
    expect(appState.activePage, PageType.command);
  });

  testWidgets('HomePage displays LogoutButton', (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.chat);
    await tester.pumpWidget(createHomePage(appState));
    expect(find.byType(LogoutButton), findsOneWidget);
  });

  testWidgets('HomePage does not display LogoutButton on login page',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.login);
    await tester.pumpWidget(createHomePage(appState));
    expect(find.byType(LogoutButton), findsNothing);
  });

  testWidgets('HomePage displays notification', (WidgetTester tester) async {
    final appState = AppState();
    final notificationState = NotificationState();
    notificationState.setNotificationError('Test error');
    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (context) => appState),
          ChangeNotifierProvider(create: (context) => MessageState()),
          ChangeNotifierProvider(create: (context) => notificationState),
        ],
        child: const MaterialApp(
          home: HomePage(),
        ),
      ),
    );
    await tester.pump();
    expect(find.text('Test error'), findsOneWidget);
  });

  testWidgets('HomePage displays TimeoutDialog when disconnected',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.chat);
    appState.setConnected(false);
    await tester.pumpWidget(createHomePage(appState));
    await tester.pump();
    expect(find.byType(TimeoutDialog), findsOneWidget);
  });
}
