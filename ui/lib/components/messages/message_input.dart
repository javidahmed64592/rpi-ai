import 'package:flutter/material.dart';
import '../../helpers/http_helper.dart';

class MessageInput extends StatefulWidget {
  const MessageInput({Key? key}) : super(key: key);

  @override
  State<MessageInput> createState() => _MessageInputState();
}

class _MessageInputState extends State<MessageInput> {
  String message = '';

  void sendMessage(String message) async {
    await HttpHelper.sendMessage(context, message);
  }

  @override
  Widget build(BuildContext context) {
    return Row(
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
    );
  }
}
