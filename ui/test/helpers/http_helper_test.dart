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
import 'package:ui/app_state.dart';
import 'package:ui/helpers/http_helper.dart';
import 'http_helper_test.mocks.dart';

// Generate a MockClient using the Mockito package.
// Create new instances of this class in each test.
@GenerateMocks([http.Client])
void main() {
  group('HttpHelper', () {
    test(
        'getHistoryInternal returns list of messages if the http call completes successfully',
        () async {
      final client = MockClient();
      final httpHelper = HttpHelper(client: client);
      const uri = 'http://example.com/history';
      const authToken = 'testToken';

      // Use Mockito to return a successful response when it calls the
      // provided http.Client.
      when(client.get(
        Uri.parse(uri),
        headers: {'Authorization': authToken},
      )).thenAnswer((_) async => http.Response(
          jsonEncode({
            'messages': [
              {'message': 'Hello', 'is_user_message': true},
              {'message': 'Hi', 'is_user_message': false}
            ]
          }),
          200));

      expect(await httpHelper.getHistoryInternal(uri, authToken), [
        {'text': 'Hello', 'isUserMessage': true},
        {'text': 'Hi', 'isUserMessage': false}
      ]);
    });

    test(
        'getHistoryInternal throws an exception if the http call completes with an error',
        () {
      final client = MockClient();
      final httpHelper = HttpHelper(client: client);
      const uri = 'http://example.com/history';
      const authToken = 'testToken';

      // Use Mockito to return an unsuccessful response when it calls the
      // provided http.Client.
      when(client.get(
        Uri.parse(uri),
        headers: {'Authorization': authToken},
      )).thenAnswer((_) async => http.Response('Not Found', 404));

      expect(httpHelper.getHistoryInternal(uri, authToken), throwsException);
    });

    test(
        'sendMessageInternal returns list of messages if the http call completes successfully',
        () async {
      final client = MockClient();
      final httpHelper = HttpHelper(client: client);
      const uri = 'http://example.com/chat';
      const message = 'Hello';
      const authToken = 'testToken';

      // Use Mockito to return a successful response when it calls the
      // provided http.Client.
      when(client.post(
        Uri.parse(uri),
        headers: {
          'Content-Type': 'application/json; charset=UTF-8',
          'Authorization': authToken,
        },
        body: jsonEncode({'message': message}),
      )).thenAnswer((_) async => http.Response(
          jsonEncode({
            'messages': [
              {'message': 'Hello', 'is_user_message': true},
              {'message': 'Hi', 'is_user_message': false}
            ]
          }),
          200));

      expect(await httpHelper.sendMessageInternal(uri, message, authToken), [
        {'text': 'Hello', 'isUserMessage': true},
        {'text': 'Hi', 'isUserMessage': false}
      ]);
    });

    test(
        'sendMessageInternal throws an exception if the http call completes with an error',
        () {
      final client = MockClient();
      final httpHelper = HttpHelper(client: client);
      const uri = 'http://example.com/chat';
      const message = 'Hello';
      const authToken = 'testToken';

      // Use Mockito to return an unsuccessful response when it calls the
      // provided http.Client.
      when(client.post(
        Uri.parse(uri),
        headers: {
          'Content-Type': 'application/json; charset=UTF-8',
          'Authorization': authToken,
        },
        body: jsonEncode({'message': message}),
      )).thenAnswer((_) async => http.Response('Not Found', 404));

      expect(httpHelper.sendMessageInternal(uri, message, authToken),
          throwsException);
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
              Future.microtask(() => httpHelper.checkApiConnection(context));
              return Container();
            },
          ),
        ),
      );

      await tester.pump(); // Rebuild the widget tree

      expect(appState.activePage, 'login');
    });
  });
}
