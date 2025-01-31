// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/messages/message_input.dart';
import 'package:ui/components/messages/message_list.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/types.dart';

class CommandPage extends StatefulWidget {
  const CommandPage({super.key});

  @override
  State<CommandPage> createState() => _CommandPageState();
}

class _CommandPageState extends State<CommandPage> {
  final ScrollController scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        Expanded(
          child: Consumer<MessageState>(
            builder: (context, messageState, child) {
              return MessageList(
                messages: [messageState.userMessage, messageState.botMessage],
                messageType: MessageType.command,
                scrollController: scrollController,
              );
            },
          ),
        ),
        const MessageInput(messageType: MessageType.command),
      ],
    );
  }
}
