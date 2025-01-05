import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'dart:convert';
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

      // Use Mockito to return a successful response when it calls the
      // provided http.Client.
      when(client.get(Uri.parse(uri))).thenAnswer((_) async => http.Response(
          jsonEncode({
            'messages': [
              {'message': 'Hello', 'is_user_message': true},
              {'message': 'Hi', 'is_user_message': false}
            ]
          }),
          200));

      expect(await httpHelper.getHistoryInternal(uri), [
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

      // Use Mockito to return an unsuccessful response when it calls the
      // provided http.Client.
      when(client.get(Uri.parse(uri)))
          .thenAnswer((_) async => http.Response('Not Found', 404));

      expect(httpHelper.getHistoryInternal(uri), throwsException);
    });

    test(
        'sendMessageInternal returns list of messages if the http call completes successfully',
        () async {
      final client = MockClient();
      final httpHelper = HttpHelper(client: client);
      const uri = 'http://example.com/chat';
      const message = 'Hello';

      // Use Mockito to return a successful response when it calls the
      // provided http.Client.
      when(client.post(
        Uri.parse(uri),
        headers: anyNamed('headers'),
        body: anyNamed('body'),
      )).thenAnswer((_) async => http.Response(
          jsonEncode({
            'messages': [
              {'message': 'Hello', 'is_user_message': true},
              {'message': 'Hi', 'is_user_message': false}
            ]
          }),
          200));

      expect(await httpHelper.sendMessageInternal(uri, message), [
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

      // Use Mockito to return an unsuccessful response when it calls the
      // provided http.Client.
      when(client.post(
        Uri.parse(uri),
        headers: anyNamed('headers'),
        body: anyNamed('body'),
      )).thenAnswer((_) async => http.Response('Not Found', 404));

      expect(httpHelper.sendMessageInternal(uri, message), throwsException);
    });
  });
}
