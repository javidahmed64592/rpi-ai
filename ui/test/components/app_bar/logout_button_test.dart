import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:ui/app_state.dart';
import 'package:ui/components/app_bar/logout_button.dart';

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
