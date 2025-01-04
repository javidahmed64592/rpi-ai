import 'package:flutter/material.dart';
import '../helpers/http_helper.dart';
import '../components/settings_dialog.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key, required this.title});
  final String title;

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String message = '';

  void sendMessage(String message) async {
    await HttpHelper.sendMessage(context, message);
  }

  Widget messageInterface() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.end,
      children: <Widget>[
        Row(
          children: [
            Expanded(
              child: TextField(
                maxLines: null,
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
            ),
            const SizedBox(width: 10),
            IconButton(
              icon: const Icon(Icons.send),
              onPressed: () {
                sendMessage(message);
              },
            ),
          ],
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
        leading: const SettingsButton(),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            children: <Widget>[
              Expanded(
                child: Container(),
              ),
              messageInterface(),
            ],
          ),
        ),
      ),
    );
  }
}
