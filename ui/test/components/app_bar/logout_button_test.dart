// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/app_bar/logout_button.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/types.dart';

void main() {
  late AppState appState;

  setUp(() {
    appState = AppState();
  });

  Widget createLogoutButton() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => appState),
      ],
      child: const MaterialApp(
        home: Scaffold(
          body: LogoutButton(),
        ),
      ),
    );
  }

  testWidgets('LogoutButton changes activePage to login',
      (WidgetTester tester) async {
    appState.setActivePage(PageType.text);
    await tester.pumpWidget(createLogoutButton());
    await tester.tap(find.byType(LogoutButton));
    await tester.pump();
    expect(appState.activePage, PageType.login);
  });

  testWidgets('LogoutButton does not change activePage when busy',
      (WidgetTester tester) async {
    appState.setActivePage(PageType.text);
    appState.setIsBusy(true);
    await tester.pumpWidget(createLogoutButton());
    await tester.tap(find.byType(LogoutButton));
    await tester.pump();
    expect(appState.activePage, PageType.text);
  });
}
