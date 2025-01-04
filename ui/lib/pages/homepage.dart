import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:provider/provider.dart';
import '../app_state.dart';

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String message = '';

  void sendMessage(String message) async {
    final appState = Provider.of<AppState>(context, listen: false);
    final Uri uri = Uri.parse('${appState.getFullUrl()}/chat');
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
  }

  Widget ipText() {
    return Consumer<AppState>(
      builder: (context, appState, child) {
        return TextField(
          decoration: const InputDecoration(
            border: OutlineInputBorder(),
            labelText: 'IP',
          ),
          onChanged: appState.setIp,
        );
      },
    );
  }

  Widget portText() {
    return Consumer<AppState>(
      builder: (context, appState, child) {
        return TextField(
          decoration: const InputDecoration(
            border: OutlineInputBorder(),
            labelText: 'Port',
          ),
          keyboardType: TextInputType.number,
          inputFormatters: <TextInputFormatter>[
            FilteringTextInputFormatter.digitsOnly
          ],
          onChanged: (String value) {
            if (value.isNotEmpty) {
              appState.setPort(int.parse(value));
            }
          },
        );
      },
    );
  }

  Widget urlBuilder() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        const Align(
          alignment: Alignment.centerLeft,
          child: Text(
            'Enter IP and Port',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
        ),
        const SizedBox(height: 20),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Expanded(
              flex: 3,
              child: ipText(),
            ),
            const SizedBox(width: 10),
            Expanded(
              flex: 1,
              child: portText(),
            ),
          ],
        ),
      ],
    );
  }

  Widget messageInterface() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        const Align(
          alignment: Alignment.centerLeft,
          child: Text(
            'Enter Message',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
        ),
        const SizedBox(height: 20),
        TextField(
          decoration: const InputDecoration(
            border: OutlineInputBorder(),
            labelText: 'Message',
          ),
          onChanged: (String value) {
            setState(() {
              message = value;
            });
          },
        ),
        const SizedBox(height: 20),
        ElevatedButton(
          onPressed: () {
            sendMessage(message);
          },
          child: const Text('Send Message'),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              urlBuilder(),
              messageInterface(),
            ],
          ),
        ),
      ),
    );
  }
}
