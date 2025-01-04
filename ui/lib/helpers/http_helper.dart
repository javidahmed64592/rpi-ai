import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:provider/provider.dart';
import '../app_state.dart';
import 'package:flutter/material.dart';
import 'dart:io';

class HttpHelper {
  static Future<void> getHistory(BuildContext context) async {
    final appState = Provider.of<AppState>(context, listen: false);
    final Uri uri = Uri.parse('${appState.getFullUrl()}/history');
    try {
      final response = await http.get(uri);

      if (response.statusCode == 200) {
        final Map<String, dynamic> body = jsonDecode(response.body);
        final List<dynamic> messagesList = body['messages'];
        final List<Map<String, dynamic>> messages = messagesList
            .map((message) => {
                  'text': message['message'],
                  'isUserMessage': message['is_user_message']
                })
            .toList();
        appState.setMessages(messages);
      } else {
        print('Failed to get history: ${response.statusCode}');
      }
    } on SocketException catch (e) {
      print('Failed to get history: $e');
      print('URI: $uri');
    }
  }

  static Future<void> sendMessage(BuildContext context, String message) async {
    final appState = Provider.of<AppState>(context, listen: false);
    final Uri uri = Uri.parse('${appState.getFullUrl()}/chat');
    try {
      final response = await http.post(
        uri,
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: jsonEncode(<String, String>{
          'message': message,
        }),
      );

      if (response.statusCode == 200) {
        print('Message sent successfully: ${response.body}');
        await getHistory(context);
      } else {
        print('Failed to send message: ${response.statusCode}');
      }
    } on SocketException catch (e) {
      print('Failed to send message: $e');
      print('Message: $message');
      print('URI: $uri');
    }
  }
}
