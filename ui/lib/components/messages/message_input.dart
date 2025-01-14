// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/notification_state.dart';

class MessageInput extends StatefulWidget {
  final VoidCallback onSend;
  final HttpHelper httpHelper;

  const MessageInput({Key? key, required this.onSend, required this.httpHelper})
      : super(key: key);

  @override
  State<MessageInput> createState() => _MessageInputState();
}

class _MessageInputState extends State<MessageInput> {
  final TextEditingController textController = TextEditingController();

  void sendMessage() async {
    final appState = Provider.of<AppState>(context, listen: false);
    final notificationState =
        Provider.of<NotificationState>(context, listen: false);

    final String userMessage = textController.text.trim();
    if (userMessage.isEmpty) {
      return;
    }
    appState.addMessage({'text': userMessage, 'isUserMessage': true});
    textController.clear();

    Map<String, dynamic> message = await widget.httpHelper
        .chat(appState.fullUrl, appState.authToken, userMessage);
    if (message.isNotEmpty) {
      appState.addMessage(message);
      widget.onSend();
    } else {
      appState.removeLastMessage();
      textController.text = userMessage;
      notificationState.setNotificationError('Failed to send message!');
    }
  }

  @override
  void dispose() {
    textController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: TextField(
            controller: textController,
            maxLines: null,
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
              hintText: 'Type a message...',
            ),
          ),
        ),
        const SizedBox(width: 10),
        IconButton(
          icon: const Icon(Icons.send),
          onPressed: () {
            sendMessage();
          },
        ),
      ],
    );
  }
}
