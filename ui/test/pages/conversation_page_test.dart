// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/conversation/text_input.dart';
import 'package:ui/components/messages/message_list.dart';
import 'package:ui/pages/conversation_page.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/state/notification_state.dart';

void main() {
  Widget createConversationPage() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppState()),
        ChangeNotifierProvider(create: (_) => MessageState()),
        ChangeNotifierProvider(create: (_) => NotificationState()),
      ],
      child: const MaterialApp(
        home: Scaffold(
          body: ConversationPage(),
        ),
      ),
    );
  }

  testWidgets('ConversationPage displays TextInput',
      (WidgetTester tester) async {
    await tester.pumpWidget(createConversationPage());
    expect(find.byType(TextInput), findsOneWidget);
  });

  testWidgets('ConversationPage displays MessageList',
      (WidgetTester tester) async {
    await tester.pumpWidget(createConversationPage());
    expect(find.byType(MessageList), findsOneWidget);
  });
}
