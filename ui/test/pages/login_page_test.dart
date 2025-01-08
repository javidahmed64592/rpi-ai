// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mockito/annotations.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/app_state.dart';
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/pages/login_page.dart';
import 'login_page_test.mocks.dart';

@GenerateMocks([HttpHelper, http.Client])
void main() {
  Widget createLoginPage(MockHttpHelper mockHttpHelper) {
    return ChangeNotifierProvider(
      create: (_) => AppState(),
      child: MaterialApp(
        home: const LoginPage(),
        builder: (context, child) {
          return Provider<HttpHelper>.value(
            value: mockHttpHelper,
            child: child!,
          );
        },
      ),
    );
  }

  testWidgets('LoginPage displays IP, Port, and Auth Token fields',
      (WidgetTester tester) async {
    final mockHttpHelper = MockHttpHelper();
    await tester.pumpWidget(createLoginPage(mockHttpHelper));

    expect(find.byType(TextField), findsNWidgets(3));
    expect(find.widgetWithText(TextField, 'IP'), findsOneWidget);
    expect(find.widgetWithText(TextField, 'Port'), findsOneWidget);
    expect(
        find.widgetWithText(TextField, 'Authentication Token'), findsOneWidget);
  });

  testWidgets('LoginPage displays Connect button', (WidgetTester tester) async {
    final mockHttpHelper = MockHttpHelper();
    await tester.pumpWidget(createLoginPage(mockHttpHelper));

    expect(find.widgetWithText(ElevatedButton, 'Connect'), findsOneWidget);
  });

  testWidgets('Fields sets IP, Port, and Auth Token in AppState',
      (WidgetTester tester) async {
    final mockHttpHelper = MockHttpHelper();
    await tester.pumpWidget(createLoginPage(mockHttpHelper));

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
}
