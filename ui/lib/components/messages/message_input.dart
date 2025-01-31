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
  final ScrollController? scrollController;
  final HttpHelper? httpHelper;

  const MessageInput({
    Key? key,
    required this.messageType,
    this.httpHelper,
    this.scrollController,
  }) : super(key: key);

  @override
  State<MessageInput> createState() => _MessageInputState();
}

class _MessageInputState extends State<MessageInput> {
  late TextEditingController textController;
  late HttpHelper httpHelper;

  @override
  void initState() {
    super.initState();
    httpHelper = widget.httpHelper ?? HttpHelper();
    textController = TextEditingController();
  }

  void scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (widget.scrollController != null &&
          widget.scrollController!.hasClients) {
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

    widget.messageType.handleAddMessage(messageState, userMessageDict);
    textController.clear();

    Map<String, dynamic> message = await widget.messageType.sendMessage(
      httpHelper,
      appState.fullUrl,
      appState.authToken,
      userMessage,
    );

    if (message.isEmpty) {
      widget.messageType.handleFailedMessage(messageState);
      textController.text = userMessage;
      notificationState.setNotificationError('Failed to send message!');
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
