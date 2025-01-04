import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import '../app_state.dart';
import '../helpers/http_helper.dart';

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String message = '';

  void sendMessage(String message) async {
    await HttpHelper.sendMessage(context, message);
  }

  void _showSettingsDialog() {
    final appState = Provider.of<AppState>(context, listen: false);
    final TextEditingController ipController =
        TextEditingController(text: appState.ip);
    final TextEditingController portController =
        TextEditingController(text: appState.port.toString());

    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Settings'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              TextField(
                controller: ipController,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'IP',
                ),
                onChanged: appState.setIp,
              ),
              const SizedBox(height: 10),
              TextField(
                controller: portController,
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
              ),
            ],
          ),
          actions: <Widget>[
            TextButton(
              child: const Text('Close'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        );
      },
    );
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
        leading: IconButton(
          icon: const Icon(Icons.settings),
          onPressed: _showSettingsDialog,
        ),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              messageInterface(),
            ],
          ),
        ),
      ),
    );
  }
}
