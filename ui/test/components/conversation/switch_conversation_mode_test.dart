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
  Widget createSwitchChatMode() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppState()),
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
    await tester.pumpWidget(createSwitchChatMode());
    final appState = Provider.of<AppState>(
        tester.element(find.byType(SwitchConversationMode)),
        listen: false);

    appState.setActivePage(PageType.text);
    expect(appState.activePage, PageType.text);

    await tester.tap(find.byType(IconButton));
    await tester.pump();

    expect(appState.activePage, PageType.speech);

    await tester.tap(find.byType(IconButton));
    await tester.pump();

    expect(appState.activePage, PageType.text);
  });
}
