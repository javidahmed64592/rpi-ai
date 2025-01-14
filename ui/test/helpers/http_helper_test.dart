// Dart imports:
import 'dart:convert';

// Flutter imports:
import 'package:flutter/widgets.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/state/app_state.dart';
import 'http_helper_test.mocks.dart';

// Generate a MockClient using the Mockito package.
// Create new instances of this class in each test.
@GenerateMocks([http.Client])
void main() {
  group('HttpHelper', () {
    test(
        'getLoginResponse returns a message if the http call completes successfully',
        () async {
      final client = MockClient();
      final httpHelper = HttpHelper(client: client);
      const uri = 'http://example.com';
      const authToken = 'testToken';

      // Use Mockito to return a successful response when it calls the
      // provided http.Client.
      when(client.get(
        Uri.parse('$uri/login'),
        headers: {'Authorization': authToken},
      )).thenAnswer((_) async => http.Response(
          jsonEncode({'message': 'Welcome', 'is_user_message': true}), 200));

      expect(await httpHelper.getLoginResponse(uri, authToken),
          {'text': 'Welcome', 'isUserMessage': true});
    });

    test(
        'getLoginResponse throws an exception if the http call completes with an error',
        () {
      final client = MockClient();
      final httpHelper = HttpHelper(client: client);
      const uri = 'http://example.com';
      const authToken = 'testToken';

      // Use Mockito to return an unsuccessful response when it calls the
      // provided http.Client.
      when(client.get(
        Uri.parse('$uri/login'),
        headers: {'Authorization': authToken},
      )).thenAnswer((_) async => http.Response('Not Found', 404));

      expect(httpHelper.getLoginResponse(uri, authToken), throwsException);
    });

    test('chat returns a message if the http call completes successfully',
        () async {
      final client = MockClient();
      final httpHelper = HttpHelper(client: client);
      const uri = 'http://example.com';
      const message = 'Hello';
      const authToken = 'testToken';

      // Use Mockito to return a successful response when it calls the
      // provided http.Client.
      when(client.post(
        Uri.parse('$uri/chat'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': authToken,
        },
        body: jsonEncode({'message': message}),
      )).thenAnswer((_) async => http.Response(
          jsonEncode({'message': 'Hi', 'is_user_message': false}), 200));

      expect(await httpHelper.chat(uri, authToken, message),
          {'text': 'Hi', 'isUserMessage': false});
    });

    test('chat returns empty dict if the http call completes with an error',
        () async {
      final client = MockClient();
      final httpHelper = HttpHelper(client: client);
      const uri = 'http://example.com';
      const message = 'Hello';
      const authToken = 'testToken';

      // Use Mockito to return an unsuccessful response when it calls the
      // provided http.Client.
      when(client.post(
        Uri.parse('$uri/chat'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': authToken,
        },
        body: jsonEncode({'message': message}),
      )).thenAnswer((_) async => http.Response('Not Found', 404));

      expect(await httpHelper.chat(uri, authToken, message), {});
    });

    testWidgets(
        'checkApiConnection sets activePage to login if the http call completes with an error',
        (WidgetTester tester) async {
      final client = MockClient();
      final httpHelper = HttpHelper(client: client);
      final appState = AppState();
      const uri = '/';

      when(client.get(Uri.parse(uri)))
          .thenAnswer((_) async => http.Response('Not Found', 404));

      await tester.pumpWidget(
        ChangeNotifierProvider<AppState>.value(
          value: appState,
          child: Builder(
            builder: (context) {
              Future.microtask(() => httpHelper.checkApiConnection(uri));
              return Container();
            },
          ),
        ),
      );

      await tester.pump(); // Rebuild the widget tree

      expect(appState.activePage, 'login');
    });

    test(
        'checkApiConnection returns true if the http call completes successfully',
        () async {
      final client = MockClient();
      final httpHelper = HttpHelper(client: client);
      const uri = 'http://example.com';

      // Use Mockito to return a successful response when it calls the
      // provided http.Client.
      when(client.get(Uri.parse('$uri/'), headers: anyNamed('headers')))
          .thenAnswer((_) async => http.Response('OK', 200));

      expect(await httpHelper.checkApiConnection(uri), true);
    });

    test(
        'checkApiConnection returns false if the http call completes with an error',
        () async {
      final client = MockClient();
      final httpHelper = HttpHelper(client: client);
      const uri = 'http://example.com';

      // Use Mockito to return an unsuccessful response when it calls the
      // provided http.Client.
      when(client.get(Uri.parse('$uri/'), headers: anyNamed('headers')))
          .thenAnswer((_) async => http.Response('Not Found', 404));

      expect(await httpHelper.checkApiConnection(uri), false);
    });
  });
}
