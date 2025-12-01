// Dart imports:
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';

// Package imports:
import 'package:http/http.dart' as http;
import 'package:http/io_client.dart';
import 'package:http_parser/http_parser.dart';
import 'package:logging/logging.dart';

class HttpHelper {
  final http.Client client;
  final Logger _logger = Logger('HttpHelper');

  HttpHelper({http.Client? client}) : client = client ?? _createClient();

  static http.Client _createClient() {
    final ioClient = HttpClient()
      ..badCertificateCallback =
          (X509Certificate cert, String host, int port) => true;
    return IOClient(ioClient);
  }

  Future<http.Response> getResponseFromUri(
      String uri, Map<String, String>? headers) async {
    final response = await client.get(Uri.parse(uri), headers: headers);
    return response;
  }

  Future<http.Response> postResponseToUri(
      String uri, Map<String, String>? headers, String body) async {
    final response = await client.post(
      Uri.parse(uri),
      headers: headers,
      body: body,
    );
    return response;
  }

  Future<bool> checkApiConnection(String url) async {
    try {
      final response = await getResponseFromUri('$url/health', {});
      if (response.statusCode == 200) {
        return true;
      }
      throw Exception('(${response.statusCode}) ${response.body}');
    } catch (e) {
      _logger.severe('Failed to connect to API: $e');
      return false;
    }
  }

  Future<List<Map<String, dynamic>>> getLoginResponse(
      String url, String authToken) async {
    final headers = <String, String>{
      'X-API-Key': authToken,
    };
    final response = await getResponseFromUri('$url/chat/history', headers);

    if (response.statusCode == 200) {
      final Map<String, dynamic> body = jsonDecode(response.body);
      final Map<String, dynamic> chatHistory = body['chat_history'];
      final List<dynamic> messages = chatHistory['messages'];
      return messages.map((message) {
        return {
          'text': message['message'].toString().trim(),
          'timestamp': DateTime.fromMillisecondsSinceEpoch(
              (message['timestamp'] * 1000).toInt()),
          'isUserMessage': message['is_user_message'],
        };
      }).toList();
    }

    // Raise exception if response status code is not 200
    throw Exception('Login failed: (${response.statusCode}) ${response.body}');
  }

  Future<Map<String, dynamic>> getConfig(String url, String authToken) async {
    final headers = <String, String>{
      'X-API-Key': authToken,
    };
    final response = await getResponseFromUri('$url/config', headers);

    if (response.statusCode == 200) {
      final Map<String, dynamic> body = jsonDecode(response.body);
      final Map<String, dynamic> config = body['config'];
      return {
        'model': config['model'].toString().trim(),
        'systemInstruction': config['system_instruction'].toString().trim(),
        'maxOutputTokens': config['max_output_tokens'],
        'temperature': config['temperature'],
      };
    }

    // Raise exception if response status code is not 200
    throw Exception(
        'Getting config failed: (${response.statusCode}) ${response.body}');
  }

  Future<List<Map<String, dynamic>>> updateConfig(
      String url, String authToken, Map<String, dynamic> config) async {
    final headers = <String, String>{
      'X-API-Key': authToken,
      'Content-Type': 'application/json',
    };
    final body = jsonEncode(config);
    final response =
        await postResponseToUri('$url/config', headers, body);

    if (response.statusCode == 200) {
      // POST /config returns None, so fetch chat history to get updated messages
      return await getLoginResponse(url, authToken);
    }

    // Raise exception if response status code is not 200
    throw Exception(
        'Updating config failed: (${response.statusCode}) ${response.body}');
  }

  Future<List<Map<String, dynamic>>> postRestartChat(
      String url, String authToken) async {
    final headers = <String, String>{
      'X-API-Key': authToken,
    };
    final response = await postResponseToUri('$url/chat/restart', headers, '');

    if (response.statusCode == 200) {
      // POST /chat/restart returns None, so fetch chat history to get updated messages
      return await getLoginResponse(url, authToken);
    }

    // Raise exception if response status code is not 200
    throw Exception(
        'Restarting chat failed: (${response.statusCode}) ${response.body}');
  }

  Future<Map<String, dynamic>> chat(
      String url, String authToken, String message) async {
    final headers = <String, String>{
      'X-API-Key': authToken,
      'Content-Type': 'application/json',
    };
    final body = jsonEncode(<String, String>{
      'message': message,
    });

    try {
      final response = await client.post(
        Uri.parse('$url/chat/message'),
        headers: headers,
        body: body,
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> body = jsonDecode(response.body);
        final Map<String, dynamic> reply = body['reply'];
        return {
          'text': reply['message'].toString().trim(),
          'timestamp': DateTime.fromMillisecondsSinceEpoch(
              (reply['timestamp'] * 1000).toInt()),
          'isUserMessage': reply['is_user_message'],
        };
      }

      // Raise exception if response status code is not 200
      throw Exception(
          'Sending message failed: (${response.statusCode}) ${response.body}'); // Updated message
    } catch (e) {
      _logger.severe('Failed to send message: $e');
      return {};
    }
  }

  Future<Map<String, dynamic>> sendAudio(
      String url, String authToken, Uint8List audioBytes) async {
    final headers = <String, String>{
      'X-API-Key': authToken,
    };

    String mimeType = 'audio/ogg';

    try {
      var request = http.MultipartRequest('POST', Uri.parse('$url/chat/audio'));
      request.headers.addAll(headers);

      final contentType = MediaType.parse(mimeType);

      request.files.add(http.MultipartFile.fromBytes(
        'audio',
        audioBytes,
        contentType: contentType,
        filename: 'audio.ogg',
      ));

      var streamedResponse = await request.send();
      var response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 200) {
        final Map<String, dynamic> body = jsonDecode(response.body);
        final Map<String, dynamic> reply = body['reply'];
        return {
          'text': reply['message'].toString().trim(),
          'timestamp': DateTime.fromMillisecondsSinceEpoch(
              (reply['timestamp'] * 1000).toInt()),
          'bytes': reply['bytes'],
        };
      }

      // Raise exception if response status code is not 200
      throw Exception(
          'Sending audio failed: (${response.statusCode}) ${response.body}');
    } catch (e) {
      _logger.severe('Failed to send audio: $e');
      return {};
    }
  }
}
