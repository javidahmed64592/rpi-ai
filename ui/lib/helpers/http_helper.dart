// Dart imports:
import 'dart:convert';
import 'dart:typed_data';

// Package imports:
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'package:logging/logging.dart';

class HttpHelper {
  final http.Client client;
  final Logger _logger = Logger('HttpHelper');

  HttpHelper({http.Client? client}) : client = client ?? http.Client();

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
      final response = await getResponseFromUri('$url/', {});
      if (response.statusCode == 200) {
        return true;
      }
      throw Exception('(${response.statusCode}) ${response.body}');
    } catch (e) {
      _logger.severe('Failed to connect to API: $e');
      return false;
    }
  }

  Future<Map<String, dynamic>> getLoginResponse(
      String url, String authToken) async {
    final headers = <String, String>{
      'Authorization': authToken,
    };
    final response = await getResponseFromUri('$url/login', headers);

    if (response.statusCode == 200) {
      final Map<String, dynamic> body = jsonDecode(response.body);
      return {
        'text': body['message'].toString().trim(),
        'isUserMessage': body['is_user_message'],
        'timestamp': DateTime.now(),
      };
    }

    // Raise exception if response status code is not 200
    throw Exception('Login failed: (${response.statusCode}) ${response.body}');
  }

  Future<Map<String, dynamic>> getConfig(String url, String authToken) async {
    final headers = <String, String>{
      'Authorization': authToken,
    };
    final response = await getResponseFromUri('$url/get-config', headers);

    if (response.statusCode == 200) {
      final Map<String, dynamic> body = jsonDecode(response.body);
      return {
        'model': body['model'].toString().trim(),
        'systemInstruction': body['system_instruction'].toString().trim(),
        'candidateCount': body['candidate_count'],
        'maxOutputTokens': body['max_output_tokens'],
        'temperature': body['temperature'],
      };
    }

    // Raise exception if response status code is not 200
    throw Exception(
        'Getting config failed: (${response.statusCode}) ${response.body}');
  }

  Future<Map<String, dynamic>> updateConfig(
      String url, String authToken, Map<String, dynamic> config) async {
    final headers = <String, String>{
      'Authorization': authToken,
      'Content-Type': 'application/json',
    };
    final body = jsonEncode(config);
    final response =
        await postResponseToUri('$url/update-config', headers, body);

    if (response.statusCode == 200) {
      final Map<String, dynamic> body = jsonDecode(response.body);
      return {
        'text': body['message'].toString().trim(),
        'isUserMessage': body['is_user_message'],
        'timestamp': DateTime.now(),
      };
    }

    // Raise exception if response status code is not 200
    throw Exception(
        'Updating config failed: (${response.statusCode}) ${response.body}');
  }

  Future<Map<String, dynamic>> chat(
      String url, String authToken, String message) async {
    final headers = <String, String>{
      'Authorization': authToken,
      'Content-Type': 'application/json',
    };
    final body = jsonEncode(<String, String>{
      'message': message,
    });

    try {
      final response = await client.post(
        Uri.parse('$url/chat'),
        headers: headers,
        body: body,
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> body = jsonDecode(response.body);
        return {
          'text': body['message'].toString().trim(),
          'isUserMessage': body['is_user_message'],
          'timestamp': DateTime.now(),
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
      'Authorization': authToken,
    };

    String mimeType = 'audio/ogg';

    try {
      var request = http.MultipartRequest('POST', Uri.parse('$url/send-audio'));
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
        return {
          'text': body['message'].toString().trim(),
          'bytes': body['bytes'],
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
