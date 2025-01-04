import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String url = 'http://127.0.0.1';
  int port = 5000;
  String message = '';

  void setUrl(String newUrl) {
    setState(() {
      url = newUrl;
    });
  }

  void setPort(int newPort) {
    setState(() {
      port = newPort;
    });
  }

  String getFullUrl() {
    final String fullUrl = '$url:$port';
    return fullUrl;
  }

  Widget urlText() {
    return TextField(
      decoration: const InputDecoration(
        border: OutlineInputBorder(),
        labelText: 'URL',
      ),
      onChanged: setUrl,
    );
  }

  Widget portText() {
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
          setPort(int.parse(value));
        }
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
            'Enter URL and Port',
            style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
          ),
        ),
        const SizedBox(height: 20),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Expanded(
              flex: 3,
              child: urlText(),
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

  // Add a method to send a POST request to full URL
  void sendMessage(String message) async {
    final Uri uri = Uri.parse('${getFullUrl()}/chat');
    print('Sending message to $uri');
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
