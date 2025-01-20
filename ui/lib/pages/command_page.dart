// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/messages/message_input.dart';
import 'package:ui/components/messages/message_list.dart';
import 'package:ui/helpers/http_helper.dart';
import 'package:ui/state/message_state.dart';
import 'package:ui/types.dart';

class CommandPage extends StatefulWidget {
  final HttpHelper httpHelper;

  const CommandPage({super.key, required this.httpHelper});

  @override
  State<CommandPage> createState() => _CommandPageState();
}

class _CommandPageState extends State<CommandPage> {
  final ScrollController scrollController = ScrollController();
  late HttpHelper httpHelper;

  @override
  void initState() {
    super.initState();
    httpHelper = widget.httpHelper;
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        Expanded(
          child: Consumer<MessageState>(
            builder: (context, messageState, child) {
              return MessageList(
                messages: messageState.messages,
                messageType: MessageType.command,
                scrollController: scrollController,
              );
            },
          ),
        ),
        MessageInput(messageType: MessageType.command, httpHelper: httpHelper),
      ],
    );
  }
}
