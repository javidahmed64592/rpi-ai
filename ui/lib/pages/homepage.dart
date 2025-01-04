import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../components/settings_dialog.dart';
import '../components/messages/message_input.dart';
import '../components/messages/message_list.dart';
import '../app_state.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key, required this.title});
  final String title;

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
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
          padding: const EdgeInsets.all(10),
          child: Column(
            children: <Widget>[
              Expanded(
                child: Consumer<AppState>(
                  builder: (context, appState, child) {
                    return MessageList(messages: appState.messages);
                  },
                ),
              ),
              const MessageInput(),
            ],
          ),
        ),
      ),
    );
  }
}
