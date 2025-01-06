import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';
import 'package:flutter/material.dart';
import 'package:ui/app_state.dart';
import 'dart:convert';
import 'dart:io';

class HttpHelper {
  final http.Client client;

  HttpHelper({required this.client});

  Future<void> checkApiConnection(BuildContext context) async {
    final appState = Provider.of<AppState>(context, listen: false);
    final uri = '${appState.getFullUrl()}/';
    try {
      final response = await client.get(Uri.parse(uri));
      if (response.statusCode != 200) {
        appState.setActivePage('login');
      }
    } on SocketException catch (e) {
      print('Failed to connect to API: $e');
      appState.setActivePage('login');
    } catch (e) {
      print('Failed to connect to API: $e');
      appState.setActivePage('login');
    }
  }

  Future<List<Map<String, dynamic>>> getHistoryInternal(
      String uri, String authToken) async {
    final response = await client.get(
      Uri.parse(uri),
      headers: <String, String>{
        'Authorization': authToken,
      },
    );

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

  Future<void> getHistory(BuildContext context) async {
    final appState = Provider.of<AppState>(context, listen: false);
    try {
      final messages = await getHistoryInternal(
          '${appState.getFullUrl()}/history', appState.authToken);
      appState.setMessages(messages);
    } on SocketException catch (e) {
      print('Failed to get history: $e');
    } catch (e) {
      print('Failed to get history: $e');
    }
  }

  Future<List<Map<String, dynamic>>> sendMessageInternal(
      String uri, String message, String authToken) async {
    final response = await client.post(
      Uri.parse(uri),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': authToken,
      },
      body: jsonEncode(<String, String>{
        'message': message,
      }),
    );

    if (response.statusCode == 200) {
      print('Message sent successfully: ${response.body}');
      final Map<String, dynamic> body = jsonDecode(response.body);
      final List<dynamic> messagesList = body['messages'];
      return messagesList
          .map((message) => {
                'text': message['message'],
                'isUserMessage': message['is_user_message']
              })
          .toList();
    }

    throw Exception('Failed to send message: ${response.statusCode}');
  }

  Future<bool> sendMessage(BuildContext context, String message) async {
    final appState = Provider.of<AppState>(context, listen: false);
    try {
      final messages = await sendMessageInternal(
          '${appState.getFullUrl()}/chat', message, appState.authToken);
      appState.setMessages(messages);
      return true;
    } on SocketException catch (e) {
      print('Failed to send message: $e');
      return false;
    } catch (e) {
      print('Failed to send message: $e');
      return false;
    }
  }
}
