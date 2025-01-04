import 'package:http/http.dart' as http;
import 'package:http/http.dart';
import 'dart:convert';
import 'package:provider/provider.dart';
import '../app_state.dart';
import 'package:flutter/material.dart';
import 'dart:io';

class HttpHelper {
  static Future<List<Map<String, dynamic>>> _getHistory(String uri) async {
    final response = await http.get(Uri.parse(uri));

    if (response.statusCode == 200) {
      final Map<String, dynamic> body = jsonDecode(response.body);
      final List<dynamic> messagesList = body['messages'];
      return messagesList
          .map((message) => {
                'text': message['message'],
                'isUserMessage': message['is_user_message']
              })
          .toList();
    }

    // Raise exception if response status code is not 200
    throw Exception('Failed to get history: ${response.statusCode}');
  }

  static Future<void> getHistory(BuildContext context) async {
    final appState = Provider.of<AppState>(context, listen: false);
    try {
      final messages = await _getHistory('${appState.getFullUrl()}/history');
      appState.setMessages(messages);
    } on SocketException catch (e) {
      print('Failed to get history: $e');
    } catch (e) {
      print('Failed to get history: $e');
    }
  }

  static Future<Response> _sendMessage(String uri, String message) async {
    return await http.post(
      Uri.parse(uri),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, String>{
        'message': message,
      }),
    );
  }

  static Future<bool> sendMessage(BuildContext context, String message) async {
    final appState = Provider.of<AppState>(context, listen: false);
    try {
      final response =
          await _sendMessage('${appState.getFullUrl()}/chat', message);

      if (response.statusCode == 200) {
        print('Message sent successfully: ${response.body}');
        await getHistory(context);
        return true;
      } else {
        print('Failed to send message: ${response.statusCode}');
        return false;
      }
    } on SocketException catch (e) {
      print('Failed to send message: $e');
      return false;
    }
  }
}
