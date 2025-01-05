import 'package:flutter/material.dart';
import '../../helpers/http_helper.dart';

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
    final String message = textController.text.trim();
    if (message.isEmpty) {
      return;
    }
    bool success = await widget.httpHelper.sendMessage(context, message);
    if (success) {
      textController.clear();
      widget.onSend();
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
