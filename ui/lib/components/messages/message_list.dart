import 'package:flutter/material.dart';
import 'message_container.dart';

class MessageList extends StatefulWidget {
  final List<Map<String, dynamic>> messages;

  const MessageList({
    Key? key,
    required this.messages,
  }) : super(key: key);

  @override
  State<MessageList> createState() => _MessageListState();
}

class _MessageListState extends State<MessageList> {
  final ScrollController scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      scrollController.jumpTo(scrollController.position.maxScrollExtent);
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      controller: scrollController,
      itemCount: widget.messages.length,
      itemBuilder: (context, index) {
        final message = widget.messages[index];
        return MessageContainer(
          message: message['text'],
          isUserMessage: message['isUserMessage'],
        );
      },
    );
  }
}
