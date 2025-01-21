// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mockito/annotations.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/messages/message_input.dart';
import 'package:ui/components/messages/message_list.dart';
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/pages/command_page.dart';
import 'package:ui/state/message_state.dart';
import 'command_page_test.mocks.dart';

@GenerateMocks([HttpHelper, http.Client])
void main() {
  Widget createConversationPage() {
    return ChangeNotifierProvider(
      create: (_) => MessageState(),
      child: MaterialApp(
        home: Scaffold(
          body: CommandPage(httpHelper: MockHttpHelper()),
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
