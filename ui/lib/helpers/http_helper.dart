// Dart imports:
import 'dart:convert';

// Package imports:
import 'package:http/http.dart' as http;

class HttpHelper {
  final http.Client client;

  HttpHelper({required this.client});

  Future<http.Response> getResponseFromUri(
      String uri, Map<String, String>? headers) async {
    try {
      final response = await client.get(Uri.parse(uri), headers: headers);
      return response;
    } catch (e) {
      print('Request failed: $e');
      rethrow;
    }
  }

  Future<bool> checkApiConnection(String url) async {
    try {
      final response = await getResponseFromUri('$url/', {});
      if (response.statusCode == 200) {
        return true;
      }
      throw Exception('(${response.statusCode}) ${response.body}');
    } catch (e) {
      print('Failed to connect to API: $e');
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
        'isUserMessage': body['is_user_message']
      };
    }

    // Raise exception if response status code is not 200
    throw Exception('Login failed: (${response.statusCode}) ${response.body}');
  }

  Future<Map<String, dynamic>> chat(
      String url, String authToken, String message) async {
    final headers = <String, String>{
      'Authorization': authToken,
      'Content-Type': 'application/json', // Add this line
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
          'isUserMessage': body['is_user_message']
        };
      }

      // Raise exception if response status code is not 200
      throw Exception(
          'Login failed: (${response.statusCode}) ${response.body}');
    } catch (e) {
      print('Failed to send message: $e');
      return {};
    }
  }
}
