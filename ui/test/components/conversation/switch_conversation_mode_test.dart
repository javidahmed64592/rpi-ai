// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/conversation/switch_conversation_mode.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/types.dart';

void main() {
  late AppState appState;

  setUp(() {
    appState = AppState();
  });

  Widget createSwitchChatMode() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => appState),
      ],
      child: const MaterialApp(
        home: Scaffold(
          body: SwitchConversationMode(),
        ),
      ),
    );
  }

  testWidgets('SwitchChatMode toggles active page',
      (WidgetTester tester) async {
    appState.setActivePage(PageType.text);
    expect(appState.activePage, PageType.text);

    await tester.pumpWidget(createSwitchChatMode());

    await tester.tap(find.byType(SwitchConversationMode));
    await tester.pump();

    expect(appState.activePage, PageType.speech);

    await tester.tap(find.byType(SwitchConversationMode));
    await tester.pump();

    expect(appState.activePage, PageType.text);
  });

  testWidgets('SwitchChatMode does not toggle active page when busy',
      (WidgetTester tester) async {
    appState.setActivePage(PageType.text);
    appState.setIsBusy(true);

    await tester.pumpWidget(createSwitchChatMode());

    await tester.tap(find.byType(SwitchConversationMode));
    await tester.pump();

    expect(appState.activePage, PageType.text);
  });
}
