// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mockito/annotations.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/app_state.dart';
import 'package:ui/components/messages/message_input.dart';
import 'package:ui/components/messages/message_list.dart';
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/pages/message_page.dart';
import 'message_page_test.mocks.dart';

@GenerateMocks([HttpHelper, http.Client])
void main() {
  Widget createMessagePage() {
    return ChangeNotifierProvider(
      create: (_) => AppState(),
      child: MaterialApp(
        home: Scaffold(
          body: MessagePage(httpHelper: MockHttpHelper()),
        ),
      ),
    );
  }

  testWidgets('MessagePage displays MessageInput', (WidgetTester tester) async {
    await tester.pumpWidget(createMessagePage());
    expect(find.byType(MessageInput), findsOneWidget);
  });

  testWidgets('MessagePage displays MessageList', (WidgetTester tester) async {
    await tester.pumpWidget(createMessagePage());
    expect(find.byType(MessageList), findsOneWidget);
  });
}
