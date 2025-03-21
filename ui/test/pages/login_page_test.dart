// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/pages/login_page.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/state/notification_state.dart';
import 'package:ui/state/settings_state.dart';
import 'login_page_test.mocks.dart';

@GenerateMocks([HttpHelper, http.Client])
void main() {
  late MockHttpHelper mockHttpHelper;

  setUp(() {
    mockHttpHelper = MockHttpHelper();
  });

  Widget createLoginPage() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AppState()),
        ChangeNotifierProvider(create: (_) => MessageState()),
        ChangeNotifierProvider(create: (_) => NotificationState()),
        ChangeNotifierProvider(create: (_) => SettingsState()),
      ],
      child: MaterialApp(
        home: Scaffold(
          body: LoginPage(httpHelper: mockHttpHelper),
        ),
      ),
    );
  }

  testWidgets('LoginPage displays IP, Port, and Auth Token fields',
      (WidgetTester tester) async {
    await tester.pumpWidget(createLoginPage());

    expect(find.byType(TextField), findsNWidgets(3));
    expect(find.widgetWithText(TextField, 'IP'), findsOneWidget);
    expect(find.widgetWithText(TextField, 'Port'), findsOneWidget);
    expect(
        find.widgetWithText(TextField, 'Authentication Token'), findsOneWidget);
  });

  testWidgets('LoginPage displays Connect button', (WidgetTester tester) async {
    await tester.pumpWidget(createLoginPage());

    expect(find.widgetWithText(ElevatedButton, 'Connect'), findsOneWidget);
  });

  testWidgets('Fields set IP, Port, and Auth Token in AppState',
      (WidgetTester tester) async {
    await tester.pumpWidget(createLoginPage());

    final ipField = find.widgetWithText(TextField, 'IP');
    final portField = find.widgetWithText(TextField, 'Port');
    final authTokenField =
        find.widgetWithText(TextField, 'Authentication Token');

    await tester.enterText(ipField, '192.168.1.1');
    await tester.enterText(portField, '8080');
    await tester.enterText(authTokenField, 'testToken');
    await tester.pumpAndSettle();

    final appState = Provider.of<AppState>(
        tester.element(find.byType(LoginPage)),
        listen: false);
    expect(appState.ip, '192.168.1.1');
    expect(appState.port, 8080);
    expect(appState.authToken, 'testToken');
  });

  testWidgets('Connect button triggers login process',
      (WidgetTester tester) async {
    when(mockHttpHelper.getLoginResponse(any, any)).thenAnswer((_) async => [
          {'text': 'Hello', 'is_user_message': false},
          {'text': 'Welcome', 'is_user_message': true}
        ]);
    when(mockHttpHelper.getConfig(any, any)).thenAnswer((_) async => {
          'model': 'model',
          'systemInstruction': 'instruction',
          'maxOutputTokens': 10,
          'temperature': 1.0,
        });

    await tester.pumpWidget(createLoginPage());

    final ipField = find.widgetWithText(TextField, 'IP');
    final portField = find.widgetWithText(TextField, 'Port');
    final authTokenField =
        find.widgetWithText(TextField, 'Authentication Token');
    final connectButton = find.widgetWithText(ElevatedButton, 'Connect');

    await tester.enterText(ipField, '192.168.1.1');
    await tester.enterText(portField, '8080');
    await tester.enterText(authTokenField, 'testToken');
    await tester.tap(connectButton);
    await tester.pumpAndSettle();

    final appState = Provider.of<AppState>(
        tester.element(find.byType(LoginPage)),
        listen: false);
    final messageState = Provider.of<MessageState>(
        tester.element(find.byType(LoginPage)),
        listen: false);
    expect(appState.connected, true);
    expect(messageState.messages.length, 2);
    expect(
        messageState.messages[0], {'text': 'Hello', 'is_user_message': false});
    expect(
        messageState.messages[1], {'text': 'Welcome', 'is_user_message': true});
  });

  testWidgets('Displays error message on failed connection',
      (WidgetTester tester) async {
    await tester.pumpWidget(createLoginPage());

    final ipField = find.widgetWithText(TextField, 'IP');
    final portField = find.widgetWithText(TextField, 'Port');
    final authTokenField =
        find.widgetWithText(TextField, 'Authentication Token');
    final connectButton = find.widgetWithText(ElevatedButton, 'Connect');

    await tester.enterText(ipField, 'invalid_ip');
    await tester.enterText(portField, '8080');
    await tester.enterText(authTokenField, 'testToken');
    await tester.tap(connectButton);
    await tester.pumpAndSettle();

    final notificationState = Provider.of<NotificationState>(
        tester.element(find.byType(LoginPage)),
        listen: false);
    expect(
        notificationState.notificationMessage, contains('Failed to connect'));
  });
}
