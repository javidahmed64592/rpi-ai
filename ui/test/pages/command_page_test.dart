// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/messages/message_input.dart';
import 'package:ui/components/messages/message_list.dart';
import 'package:ui/pages/command_page.dart';
import 'package:ui/state/message_state.dart';

void main() {
  Widget createConversationPage() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => MessageState()),
      ],
      child: const MaterialApp(
        home: Scaffold(
          body: CommandPage(),
        ),
      ),
    );
  }

  testWidgets('ConversationPage displays MessageInput',
      (WidgetTester tester) async {
    await tester.pumpWidget(createConversationPage());
    expect(find.byType(MessageInput), findsOneWidget);
  });

  testWidgets('ConversationPage displays MessageList',
      (WidgetTester tester) async {
    await tester.pumpWidget(createConversationPage());
    expect(find.byType(MessageList), findsOneWidget);
  });
}
