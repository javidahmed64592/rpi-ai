import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:ui/helpers/http_helper.dart';
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
  final ScrollController scrollController = ScrollController();

  void scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (scrollController.hasClients) {
        scrollController.jumpTo(scrollController.position.maxScrollExtent);
      }
    });
  }

  @override
  void initState() {
    super.initState();
    HttpHelper.getHistory(context).then((_) => scrollToBottom());
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
          padding: const EdgeInsets.all(10),
          child: Column(
            children: <Widget>[
              Expanded(
                child: Consumer<AppState>(
                  builder: (context, appState, child) {
                    return MessageList(
                      messages: appState.messages,
                      scrollController: scrollController,
                    );
                  },
                ),
              ),
              MessageInput(onSend: scrollToBottom),
            ],
          ),
        ),
      ),
    );
  }
}
