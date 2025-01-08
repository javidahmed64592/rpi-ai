// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:http/http.dart' as http;
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/app_state.dart';
import 'package:ui/components/messages/message_input.dart';
import 'package:ui/components/messages/message_list.dart';
import 'package:ui/helpers/http_helper.dart';

class MessagePage extends StatefulWidget {
  const MessagePage({super.key});

  @override
  State<MessagePage> createState() => _MessagePageState();
}

class _MessagePageState extends State<MessagePage> {
  final ScrollController scrollController = ScrollController();
  late HttpHelper httpHelper;

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
    httpHelper = HttpHelper(client: http.Client());
    httpHelper.getHistory(context).then((_) => scrollToBottom());
  }

  @override
  Widget build(BuildContext context) {
    return Column(
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
        MessageInput(onSend: scrollToBottom, httpHelper: httpHelper),
      ],
    );
  }
}
