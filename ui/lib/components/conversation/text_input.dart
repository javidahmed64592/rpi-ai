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

class TextInput extends StatefulWidget {
  final ScrollController? scrollController;
  final HttpHelper? httpHelper;

  const TextInput({
    Key? key,
    this.httpHelper,
    this.scrollController,
  }) : super(key: key);

  @override
  State<TextInput> createState() => _TextInputState();
}

class _TextInputState extends State<TextInput> {
  late TextEditingController textController;
  late AppState appState;
  late MessageState messageState;
  late NotificationState notificationState;
  late HttpHelper httpHelper;

  @override
  void initState() {
    super.initState();
    httpHelper = widget.httpHelper ?? HttpHelper();
    textController = TextEditingController();
    appState = Provider.of<AppState>(context, listen: false);
    messageState = Provider.of<MessageState>(context, listen: false);
    notificationState = Provider.of<NotificationState>(context, listen: false);
  }

  MessageType getMessageType() {
    return MessageType.text;
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
    final String userMessage = textController.text.trim();
    if (userMessage.isEmpty) {
      return;
    }

    final MessageType messageType = getMessageType();

    final Map<String, dynamic> userMessageDict = {
      'text': userMessage,
      'isUserMessage': true,
      'timestamp': DateTime.now()
    };

    messageType.handleAddMessage(messageState, userMessageDict);
    textController.clear();
    scrollToBottom();

    Map<String, dynamic> message = await messageType.sendMessage(
      httpHelper,
      appState.fullUrl,
      appState.authToken,
      userMessage,
    );

    if (message.isEmpty) {
      messageType.handleFailedMessage(messageState);
      textController.text = userMessage;
      notificationState.setNotificationError('Failed to send message!');
      return;
    }

    if (messageType == MessageType.text) {
      messageState.addMessage(message);
      scrollToBottom();
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
