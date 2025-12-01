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
      'checkApiHealth sets activePage to login if the http call completes with an error',
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
            Future.microtask(() => httpHelper.checkApiHealth(uri));
            return Container();
          },
        ),
      ),
    );

    await tester.pump();

    expect(appState.activePage, PageType.login);
  });

  test(
      'checkApiHealth returns true if the http call completes successfully',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';

    when(client.get(Uri.parse('$uri/health'), headers: anyNamed('headers')))
        .thenAnswer((_) async => http.Response('OK', 200));

    expect(await httpHelper.checkApiHealth(uri), true);
  });

  test(
      'checkApiHealth returns false if the http call completes with an error',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';

    when(client.get(Uri.parse('$uri/'), headers: anyNamed('headers')))
        .thenAnswer((_) async => http.Response('Not Found', 404));

    expect(await httpHelper.checkApiHealth(uri), false);
  });

  test(
      'getChatHistory returns a list of messages if the http call completes successfully',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';

    when(client.get(
      Uri.parse('$uri/chat/history'),
      headers: {'X-API-Key': authToken},
    )).thenAnswer((_) async => http.Response(
        jsonEncode({
          'chat_history': {
            'messages': [
              {
                'message': 'Welcome',
                'timestamp': 1678886400,
                'is_user_message': true,
              },
              {
                'message': 'Hello',
                'timestamp': 1678886460,
                'is_user_message': false,
              }
            ]
          }
        }),
        200));

    final messages = await httpHelper.getChatHistory(uri, authToken);
    expect(messages.length, 2);
    expect(messages[0], {
      'text': 'Welcome',
      'timestamp': isA<DateTime>(),
      'isUserMessage': true,
    });
    expect(messages[1], {
      'text': 'Hello',
      'timestamp': isA<DateTime>(),
      'isUserMessage': false,
    });
  });

  test(
      'getChatHistory throws an exception if the http call completes with an error',
      () {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';

    when(client.get(
      Uri.parse('$uri/chat/history'),
      headers: {'X-API-Key': authToken},
    )).thenAnswer((_) async => http.Response('Not Found', 404));

    expect(httpHelper.getChatHistory(uri, authToken), throwsException);
  });

  test('getConfig returns config if the http call completes successfully',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';

    when(client.get(
      Uri.parse('$uri/config'),
      headers: {'X-API-Key': authToken},
    )).thenAnswer((_) async => http.Response(
        jsonEncode({
          'config': {
            'model': 'testModel',
            'system_instruction': 'testInstruction',
            'max_output_tokens': 100,
            'temperature': 0.7,
          }
        }),
        200));

    expect(await httpHelper.getConfig(uri, authToken), {
      'model': 'testModel',
      'systemInstruction': 'testInstruction',
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
      Uri.parse('$uri/config'),
      headers: {'X-API-Key': authToken},
    )).thenAnswer((_) async => http.Response('Not Found', 404));

    expect(httpHelper.getConfig(uri, authToken), throwsException);
  });

  test(
      'postConfig returns a list of messages if the http call completes successfully',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';
    final config = {
      'model': 'newModel',
      'system_instruction': 'newInstruction',
      'max_output_tokens': 200,
      'temperature': 0.9,
    };

    when(client.post(
      Uri.parse('$uri/config'),
      headers: {
        'X-API-Key': authToken,
        'Content-Type': 'application/json',
      },
      body: jsonEncode(config),
    )).thenAnswer((_) async => http.Response('', 200));

    when(client.get(
      Uri.parse('$uri/chat/history'),
      headers: {'X-API-Key': authToken},
    )).thenAnswer((_) async => http.Response(
        jsonEncode({
          'chat_history': {
            'messages': [
              {
                'message': 'Config updated successfully',
                'timestamp': 1678886400,
                'is_user_message': false
              },
            ]
          }
        }),
        200));

    final messages = await httpHelper.postConfig(uri, authToken, config);
    expect(messages[0], {
      'text': 'Config updated successfully',
      'timestamp': isA<DateTime>(),
      'isUserMessage': false,
    });
  });

  test(
      'postConfig throws an exception if the http call completes with an error',
      () {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';
    final config = {
      'model': 'newModel',
      'system_instruction': 'newInstruction',
      'max_output_tokens': 200,
      'temperature': 0.9,
    };

    when(client.post(
      Uri.parse('$uri/config'),
      headers: {
        'X-API-Key': authToken,
        'Content-Type': 'application/json',
      },
      body: jsonEncode(config),
    )).thenAnswer((_) async => http.Response('Not Found', 404));

    expect(httpHelper.postConfig(uri, authToken, config), throwsException);
  });

  test(
      'postRestartChat returns a list of one message if the http call completes successfully',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';

    when(client.post(
      Uri.parse('$uri/chat/restart'),
      headers: {'X-API-Key': authToken},
      body: '',
    )).thenAnswer((_) async => http.Response('', 200));

    when(client.get(
      Uri.parse('$uri/chat/history'),
      headers: {'X-API-Key': authToken},
    )).thenAnswer((_) async => http.Response(
        jsonEncode({
          'chat_history': {
            'messages': [
              {
                'message': 'Chat restarted',
                'timestamp': 1678886400,
                'is_user_message': false,
              },
            ]
          }
        }),
        200));

    final messages = await httpHelper.postRestartChat(uri, authToken);
    expect(messages.length, 1);
    expect(messages[0], {
      'text': 'Chat restarted',
      'timestamp': isA<DateTime>(),
      'isUserMessage': false,
    });
  });

  test(
      'postRestartChat throws an exception if the http call completes with an error',
      () {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const authToken = 'testToken';

    when(client.post(
      Uri.parse('$uri/chat/restart'),
      headers: {'X-API-Key': authToken},
      body: '',
    )).thenAnswer((_) async => http.Response('Not Found', 404));

    expect(httpHelper.postRestartChat(uri, authToken), throwsException);
  });

  test('postMessageText returns a message if the http call completes successfully',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const message = 'Hello';
    const authToken = 'testToken';

    when(client.post(
      Uri.parse('$uri/chat/message'),
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': authToken,
      },
      body: jsonEncode({'message': message}),
    )).thenAnswer((_) async => http.Response(
        jsonEncode({
          'reply': {
            'message': 'Hi',
            'timestamp': 1678886400,
            'is_user_message': false,
          }
        }),
        200));

    expect(await httpHelper.postMessageText(uri, authToken, message), {
      'text': 'Hi',
      'timestamp': isA<DateTime>(),
      'isUserMessage': false,
    });
  });

  test('postMessageText returns empty dict if the http call completes with an error',
      () async {
    final httpHelper = HttpHelper(client: client);
    const uri = 'http://example.com';
    const message = 'Hello';
    const authToken = 'testToken';

    when(client.post(
      Uri.parse('$uri/chat/message'),
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': authToken,
      },
      body: jsonEncode({'message': message}),
    )).thenAnswer((_) async => http.Response('Not Found', 404));

    expect(await httpHelper.postMessageText(uri, authToken, message), {});
  });

  test('postMessageAudio returns empty dict if the http call completes with an error',
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

    expect(await httpHelper.postMessageAudio(uri, authToken, audioData), {});
  });
}
