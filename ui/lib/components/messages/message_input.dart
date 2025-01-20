// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/state/app_state.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/state/notification_state.dart';
import 'package:ui/types.dart';

class MessageInput extends StatefulWidget {
  final MessageType messageType;
  final HttpHelper httpHelper;
  final ScrollController? scrollController;

  const MessageInput({
    Key? key,
    required this.messageType,
    required this.httpHelper,
    this.scrollController,
  }) : super(key: key);

  @override
  State<MessageInput> createState() => _MessageInputState();
}

class _MessageInputState extends State<MessageInput> {
  final TextEditingController textController = TextEditingController();

  void scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (widget.scrollController!.hasClients) {
        widget.scrollController
            ?.jumpTo(widget.scrollController!.position.maxScrollExtent);
      }
    });
  }

  void sendMessage() async {
    final appState = Provider.of<AppState>(context, listen: false);
    final messageState = Provider.of<MessageState>(context, listen: false);
    final notificationState =
        Provider.of<NotificationState>(context, listen: false);

    final String userMessage = textController.text.trim();
    if (userMessage.isEmpty) {
      return;
    }

    final Map<String, dynamic> userMessageDict = {
      'text': userMessage,
      'isUserMessage': true,
      'timestamp': DateTime.now()
    };

    if (widget.messageType == MessageType.chat) {
      messageState.addMessage(userMessageDict);
    } else if (widget.messageType == MessageType.command) {
      messageState.setUserMessage(userMessageDict);
    }

    textController.clear();

    Map<String, dynamic> message = {};
    if (widget.messageType == MessageType.chat) {
      message = await widget.httpHelper
          .chat(appState.fullUrl, appState.authToken, userMessage);
    } else if (widget.messageType == MessageType.command) {
      message = await widget.httpHelper
          .command(appState.fullUrl, appState.authToken, userMessage);
    }

    if (message.isEmpty) {
      messageState.removeLastMessage();
      textController.text = userMessage;
      notificationState.setNotificationError('Failed to send command!');
      return;
    }

    if (widget.messageType == MessageType.chat) {
      messageState.addMessage(message);
      scrollToBottom();
    } else if (widget.messageType == MessageType.command) {
      messageState.setBotMessage(message);
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
