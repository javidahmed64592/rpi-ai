// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/app_bar/custom_app_bar.dart';
import 'package:ui/components/app_bar/logout_button.dart';
import 'package:ui/components/app_bar/settings_dialog.dart';
import 'package:ui/components/app_bar/switch_chat_mode.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/types.dart';

void main() {
  Widget createCustomAppBar(AppState appState) {
    return ChangeNotifierProvider(
      create: (context) => appState,
      child: MaterialApp(
        home: Scaffold(
          appBar: CustomAppBar(appState: appState),
        ),
      ),
    );
  }

  testWidgets('CustomAppBar displays title for login page',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.login);
    await tester.pumpWidget(createCustomAppBar(appState));
    expect(find.text(PageType.login.title), findsOneWidget);
  });

  testWidgets('CustomAppBar displays title for chat page',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.chat);
    await tester.pumpWidget(createCustomAppBar(appState));
    expect(find.text(PageType.chat.title), findsOneWidget);
  });

  testWidgets('CustomAppBar displays title for command page',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.command);
    await tester.pumpWidget(createCustomAppBar(appState));
    expect(find.text(PageType.command.title), findsOneWidget);
  });

  testWidgets('CustomAppBar displays SettingsButton',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.chat);
    await tester.pumpWidget(createCustomAppBar(appState));
    expect(find.byType(SettingsButton), findsOneWidget);
  });

  testWidgets('CustomAppBar does not display SettingsButton on login page',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.login);
    await tester.pumpWidget(createCustomAppBar(appState));
    expect(find.byType(SettingsButton), findsNothing);
  });

  testWidgets('CustomAppBar displays SwitchChatMode',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.chat);
    await tester.pumpWidget(createCustomAppBar(appState));
    expect(find.byType(SwitchChatMode), findsOneWidget);
  });

  testWidgets('CustomAppBar does not display SwitchChatMode on login page',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.login);
    await tester.pumpWidget(createCustomAppBar(appState));
    expect(find.byType(SwitchChatMode), findsNothing);
  });

  testWidgets('CustomAppBar displays LogoutButton',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.chat);
    await tester.pumpWidget(createCustomAppBar(appState));
    expect(find.byType(LogoutButton), findsOneWidget);
  });

  testWidgets('CustomAppBar does not display LogoutButton on login page',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage(PageType.login);
    await tester.pumpWidget(createCustomAppBar(appState));
    expect(find.byType(LogoutButton), findsNothing);
  });
}
