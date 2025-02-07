// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/app_bar/custom_app_bar.dart';
import 'package:ui/components/app_bar/logout_button.dart';
import 'package:ui/components/app_bar/settings_dialog.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/types.dart';

void main() {
  Widget createCustomAppBar() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppState()),
      ],
      child: const MaterialApp(
        home: Scaffold(
          body: CustomAppBar(),
        ),
      ),
    );
  }

  testWidgets('CustomAppBar displays title for login page',
      (WidgetTester tester) async {
    await tester.pumpWidget(createCustomAppBar());
    final appState = Provider.of<AppState>(
        tester.element(find.byType(CustomAppBar)),
        listen: false);
    appState.setActivePage(PageType.login);
    await tester.pump();
    expect(find.text(PageType.login.title), findsOneWidget);
  });

  testWidgets('CustomAppBar displays title for chat page',
      (WidgetTester tester) async {
    await tester.pumpWidget(createCustomAppBar());
    final appState = Provider.of<AppState>(
        tester.element(find.byType(CustomAppBar)),
        listen: false);
    appState.setActivePage(PageType.text);
    await tester.pump();
    expect(find.text(PageType.text.title), findsOneWidget);
  });

  testWidgets('CustomAppBar displays SettingsButton',
      (WidgetTester tester) async {
    await tester.pumpWidget(createCustomAppBar());
    final appState = Provider.of<AppState>(
        tester.element(find.byType(CustomAppBar)),
        listen: false);
    appState.setActivePage(PageType.text);
    await tester.pump();
    expect(find.byType(SettingsButton), findsOneWidget);
  });

  testWidgets('CustomAppBar does not display SettingsButton on login page',
      (WidgetTester tester) async {
    await tester.pumpWidget(createCustomAppBar());
    final appState = Provider.of<AppState>(
        tester.element(find.byType(CustomAppBar)),
        listen: false);
    appState.setActivePage(PageType.login);
    await tester.pump();
    expect(find.byType(SettingsButton), findsNothing);
  });

  testWidgets('CustomAppBar displays LogoutButton',
      (WidgetTester tester) async {
    await tester.pumpWidget(createCustomAppBar());
    final appState = Provider.of<AppState>(
        tester.element(find.byType(CustomAppBar)),
        listen: false);
    appState.setActivePage(PageType.text);
    await tester.pump();
    expect(find.byType(LogoutButton), findsOneWidget);
  });

  testWidgets('CustomAppBar does not display LogoutButton on login page',
      (WidgetTester tester) async {
    await tester.pumpWidget(createCustomAppBar());
    final appState = Provider.of<AppState>(
        tester.element(find.byType(CustomAppBar)),
        listen: false);
    appState.setActivePage(PageType.login);
    await tester.pump();
    expect(find.byType(LogoutButton), findsNothing);
  });
}
