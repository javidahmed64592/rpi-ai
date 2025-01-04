import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:provider/provider.dart';
import '../app_state.dart';
import 'package:flutter/material.dart';
import 'dart:io';

class HttpHelper {
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
