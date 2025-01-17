// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/app_bar/logout_button.dart';
import 'package:ui/state/app_state.dart';

void main() {
  Widget createTestWidget(AppState appState) {
    return ChangeNotifierProvider.value(
      value: appState,
      child: const MaterialApp(
        home: Scaffold(
          body: LogoutButton(),
        ),
      ),
    );
  }

  testWidgets('LogoutButton changes activePage to login',
      (WidgetTester tester) async {
    final appState = AppState();
    appState.setActivePage('message');
    await tester.pumpWidget(createTestWidget(appState));
    await tester.tap(find.byType(IconButton));
    await tester.pump();
    expect(appState.activePage, 'login');
  });
}
