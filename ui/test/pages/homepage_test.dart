import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:ui/components/messages/message_input.dart';
import 'package:ui/components/messages/message_list.dart';
import 'package:ui/pages/homepage.dart';
import 'package:ui/app_state.dart';
import 'package:ui/components/settings_dialog.dart';
import 'package:ui/helpers/http_helper.dart';
import 'package:http/http.dart' as http;
import 'package:mockito/annotations.dart';

@GenerateMocks([HttpHelper, http.Client])
void main() {
  Widget createHomePage() {
    return ChangeNotifierProvider(
      create: (_) => AppState(),
      child: const MaterialApp(
        home: HomePage(title: 'Home Page'),
      ),
    );
  }

  testWidgets('HomePage displays title', (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    expect(find.text('Home Page'), findsOneWidget);
  });

  testWidgets('HomePage displays SettingsButton', (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    expect(find.byType(SettingsButton), findsOneWidget);
  });

  testWidgets('HomePage displays MessageInput', (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    expect(find.byType(MessageInput), findsOneWidget);
  });

  testWidgets('HomePage displays MessageList', (WidgetTester tester) async {
    await tester.pumpWidget(createHomePage());
    expect(find.byType(MessageList), findsOneWidget);
  });
}
