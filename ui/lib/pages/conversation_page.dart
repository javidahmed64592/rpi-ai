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

class ConversationPage extends StatefulWidget {
  final HttpHelper httpHelper;

  const ConversationPage({super.key, required this.httpHelper});

  @override
  State<ConversationPage> createState() => _ConversationPageState();
}

class _ConversationPageState extends State<ConversationPage> {
  final ScrollController scrollController = ScrollController();
  late HttpHelper httpHelper;

  @override
  void initState() {
    super.initState();
    httpHelper = widget.httpHelper;
  }

  @override
  void dispose() {
    scrollController.dispose();
    super.dispose();
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
                messageType: MessageType.chat,
                scrollController: scrollController,
              );
            },
          ),
        ),
        MessageInput(
          messageType: MessageType.chat,
          httpHelper: httpHelper,
          scrollController: scrollController,
        ),
      ],
    );
  }
}
