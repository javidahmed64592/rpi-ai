// Dart imports:
import 'dart:convert';
import 'dart:typed_data';

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
import 'package:ui/types.dart';
import 'http_helper_test.mocks.dart';

@GenerateMocks([http.Client])
void main() {
  late MockClient client;

  setUp(() {
    client = MockClient();
  });

  testWidgets(
      'checkApiConnection sets activePage to login if the http call completes with an error',
      (WidgetTester tester) async {
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

    await tester.pump();

    expect(appState.activePage, PageType.login);
  });

  test(
      'checkApiConnection returns true if the http call completes successfully',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';

    when(client.get(Uri.parse('$uri/'), headers: anyNamed('headers')))
        .thenAnswer((_) async => http.Response('OK', 200));

    expect(await httpHelper.checkApiConnection(uri), true);
  });

  test(
      'checkApiConnection returns false if the http call completes with an error',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';

    when(client.get(Uri.parse('$uri/'), headers: anyNamed('headers')))
        .thenAnswer((_) async => http.Response('Not Found', 404));

    expect(await httpHelper.checkApiConnection(uri), false);
  });

  test(
      'getLoginResponse returns a list of messages if the http call completes successfully',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';

    when(client.get(
      Uri.parse('$uri/login'),
      headers: {'Authorization': authToken},
    )).thenAnswer((_) async => http.Response(
        jsonEncode({
          'messages': [
            {'message': 'Welcome', 'is_user_message': true},
            {'message': 'Hello', 'is_user_message': false}
          ]
        }),
        200));

    final messages = await httpHelper.getLoginResponse(uri, authToken);
    expect(messages.length, 2);
    expect(messages[0], {
      'text': 'Welcome',
      'isUserMessage': true,
      'timestamp': isA<DateTime>(),
    });
    expect(messages[1], {
      'text': 'Hello',
      'isUserMessage': false,
      'timestamp': isA<DateTime>(),
    });
  });

  test(
      'getLoginResponse throws an exception if the http call completes with an error',
      () {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';

    when(client.get(
      Uri.parse('$uri/login'),
      headers: {'Authorization': authToken},
    )).thenAnswer((_) async => http.Response('Not Found', 404));

    expect(httpHelper.getLoginResponse(uri, authToken), throwsException);
  });

  test('getConfig returns config if the http call completes successfully',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';

    when(client.get(
      Uri.parse('$uri/get-config'),
      headers: {'Authorization': authToken},
    )).thenAnswer((_) async => http.Response(
        jsonEncode({
          'model': 'testModel',
          'system_instruction': 'testInstruction',
          'candidate_count': 5,
          'max_output_tokens': 100,
          'temperature': 0.7,
        }),
        200));

    expect(await httpHelper.getConfig(uri, authToken), {
      'model': 'testModel',
      'systemInstruction': 'testInstruction',
      'candidateCount': 5,
      'maxOutputTokens': 100,
      'temperature': 0.7,
    });
  });

  test('getConfig throws an exception if the http call completes with an error',
      () {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';

    when(client.get(
      Uri.parse('$uri/get-config'),
      headers: {'Authorization': authToken},
    )).thenAnswer((_) async => http.Response('Not Found', 404));

    expect(httpHelper.getConfig(uri, authToken), throwsException);
  });

  test(
      'updateConfig returns a list of messages if the http call completes successfully',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';
    final config = {
      'model': 'newModel',
      'system_instruction': 'newInstruction',
      'candidate_count': 10,
      'max_output_tokens': 200,
      'temperature': 0.9,
    };

    when(client.post(
      Uri.parse('$uri/update-config'),
      headers: {
        'Authorization': authToken,
        'Content-Type': 'application/json',
      },
      body: jsonEncode(config),
    )).thenAnswer((_) async => http.Response(
        jsonEncode({
          'messages': [
            {
              'message': 'Config updated successfully',
              'is_user_message': false
            },
          ]
        }),
        200));

    final messages = await httpHelper.updateConfig(uri, authToken, config);
    expect(messages[0], {
      'text': 'Config updated successfully',
      'isUserMessage': false,
      'timestamp': isA<DateTime>(),
    });
  });

  test(
      'updateConfig throws an exception if the http call completes with an error',
      () {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';
    final config = {
      'model': 'newModel',
      'system_instruction': 'newInstruction',
      'candidate_count': 10,
      'max_output_tokens': 200,
      'temperature': 0.9,
    };

    when(client.post(
      Uri.parse('$uri/update-config'),
      headers: {
        'Authorization': authToken,
        'Content-Type': 'application/json',
      },
      body: jsonEncode(config),
    )).thenAnswer((_) async => http.Response('Not Found', 404));

    expect(httpHelper.updateConfig(uri, authToken, config), throwsException);
  });

  test(
      'postRestartChat returns a list of one message if the http call completes successfully',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';

    when(client.get(
      Uri.parse('$uri/restart-chat'),
      headers: {'Authorization': authToken},
    )).thenAnswer((_) async => http.Response(
        jsonEncode({
          'messages': [
            {'message': 'Chat restarted', 'is_user_message': false},
          ]
        }),
        200));

    final messages = await httpHelper.postRestartChat(uri, authToken);
    expect(messages.length, 1);
    expect(messages[0], {
      'text': 'Chat restarted',
      'isUserMessage': false,
      'timestamp': isA<DateTime>(),
    });
  });

  test(
      'postRestartChat throws an exception if the http call completes with an error',
      () {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';

    when(client.get(
      Uri.parse('$uri/restart-chat'),
      headers: {'Authorization': authToken},
    )).thenAnswer((_) async => http.Response('Not Found', 404));

    expect(httpHelper.postRestartChat(uri, authToken), throwsException);
  });

  test('chat returns a message if the http call completes successfully',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const message = 'Hello';
    const authToken = 'testToken';

    when(client.post(
      Uri.parse('$uri/chat'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': authToken,
      },
      body: jsonEncode({'message': message}),
    )).thenAnswer((_) async => http.Response(
        jsonEncode({'message': 'Hi', 'is_user_message': false}), 200));

    expect(await httpHelper.chat(uri, authToken, message), {
      'text': 'Hi',
      'isUserMessage': false,
      'timestamp': isA<DateTime>(),
    });
  });

  test('chat returns empty dict if the http call completes with an error',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const message = 'Hello';
    const authToken = 'testToken';

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

  test('sendAudio returns empty dict if the http call completes with an error',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';
    final Uint8List audioData = Uint8List.fromList([1, 2, 3, 4]);

    when(client.send(any)).thenAnswer((_) async {
      final response =
          http.Response(jsonEncode({'message': 'Error', 'bytes': ''}), 404);
      return http.StreamedResponse(
          Stream.fromIterable([response.bodyBytes]), response.statusCode);
    });

    expect(await httpHelper.sendAudio(uri, authToken, audioData), {});
  });
}
