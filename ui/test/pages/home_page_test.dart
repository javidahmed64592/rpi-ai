// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/app_bar/custom_app_bar.dart';
import 'package:ui/components/app_bar/logout_button.dart';
import 'package:ui/components/app_bar/switch_chat_mode.dart';
import 'package:ui/components/timeout_dialog.dart';
import 'package:ui/pages/home_page.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/state/notification_state.dart';
import 'package:ui/state/settings_state.dart';
import 'package:ui/types.dart';

void main() {
  late AppState appState;
  late NotificationState notificationState;

  setUp(() {
    appState = AppState();
    notificationState = NotificationState();
  });

  Widget createHomePage() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (context) => appState),
        ChangeNotifierProvider(create: (context) => MessageState()),
        ChangeNotifierProvider(create: (context) => notificationState),
        ChangeNotifierProvider(create: (context) => SettingsState()),
      ],
      child: const MaterialApp(
        home: HomePage(),
      ),
    );
  }

  testWidgets('HomePage displays CustomAppBar', (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    expect(find.byType(CustomAppBar), findsOneWidget);
  });

  testWidgets('HomePage displays SwitchChatMode', (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    appState.setActivePage(PageType.chat);
    await tester.pump();
    expect(find.byType(SwitchChatMode), findsOneWidget);
  });

  testWidgets('HomePage does not display SwitchChatMode on login page',
      (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    appState.setActivePage(PageType.login);
    await tester.pump();
    expect(find.byType(SwitchChatMode), findsNothing);
  });

  testWidgets('HomePage displays LogoutButton', (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    appState.setActivePage(PageType.chat);
    await tester.pump();
    expect(find.byType(LogoutButton), findsOneWidget);
  });

  testWidgets('HomePage does not display LogoutButton on login page',
      (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    appState.setActivePage(PageType.login);
    await tester.pump();
    expect(find.byType(LogoutButton), findsNothing);
  });

  testWidgets('HomePage displays error notification',
      (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    notificationState.setNotificationError('Test error');
    await tester.pump();
    expect(find.text('Test error'), findsOneWidget);
  });

  testWidgets('HomePage displays info notification',
      (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    notificationState.setNotificationInfo('Test info');
    await tester.pump();
    expect(find.text('Test info'), findsOneWidget);
  });

  testWidgets('HomePage displays warning notification',
      (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    notificationState.setNotificationWarning('Test warning');
    await tester.pump();
    expect(find.text('Test warning'), findsOneWidget);
  });

  testWidgets('HomePage displays TimeoutDialog when disconnected',
      (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    appState.setActivePage(PageType.chat);
    appState.setConnected(false);
    await tester.pump();
    expect(find.byType(TimeoutDialog), findsOneWidget);
  });
}
