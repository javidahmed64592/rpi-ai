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
  Widget createLogoutButton() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppState()),
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
    await tester.pumpWidget(createLogoutButton());
    final appState = Provider.of<AppState>(
        tester.element(find.byType(LogoutButton)),
        listen: false);
    appState.setActivePage(PageType.login);
    await tester.tap(find.byType(IconButton));
    await tester.pump();
    expect(appState.activePage, PageType.login);
  });
}
