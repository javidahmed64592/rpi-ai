// Flutter imports:
import 'package:flutter/material.dart';

// Project imports:
import 'package:ui/components/messages/message_container.dart';

class MessageList extends StatefulWidget {
  final List<Map<String, dynamic>> messages;
  final ScrollController scrollController;

  const MessageList({
    Key? key,
    required this.messages,
    required this.scrollController,
  }) : super(key: key);

  @override
  State<MessageList> createState() => _MessageListState();
}

class _MessageListState extends State<MessageList> {
  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      widget.scrollController
          .jumpTo(widget.scrollController.position.maxScrollExtent);
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      controller: widget.scrollController,
      itemCount: widget.messages.length,
      itemBuilder: (context, index) {
        final message = widget.messages[index];
        if (message.isNotEmpty) {
          return MessageContainer(
            message: message['text'],
            isUserMessage: message['isUserMessage'],
            timestamp: message['timestamp'],
          );
        }
        return const SizedBox.shrink();
      },
    );
  }
}
