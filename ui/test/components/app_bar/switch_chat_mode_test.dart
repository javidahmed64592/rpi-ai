// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/app_bar/switch_chat_mode.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/types.dart';

void main() {
  testWidgets('SwitchChatMode toggles active page',
      (WidgetTester tester) async {
    // Create a mock AppState
    final appState = AppState();

    // Build the widget tree
    await tester.pumpWidget(
      ChangeNotifierProvider<AppState>.value(
        value: appState,
        child: const MaterialApp(
          home: Scaffold(
            body: SwitchChatMode(),
          ),
        ),
      ),
    );

    appState.setActivePage(PageType.chat);
    expect(appState.activePage, PageType.chat);

    await tester.tap(find.byType(IconButton));
    await tester.pump();

    expect(appState.activePage, PageType.command);

    await tester.tap(find.byType(IconButton));
    await tester.pump();

    expect(appState.activePage, PageType.chat);
  });
}
