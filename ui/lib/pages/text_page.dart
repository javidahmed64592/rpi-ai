// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:provider/provider.dart';

// Project imports:
import 'package:ui/components/conversation/text_input.dart';
import 'package:ui/components/messages/message_list.dart';
import 'package:ui/state/message_state.dart';

class TextPage extends StatefulWidget {
  const TextPage({super.key});

  @override
  State<TextPage> createState() => _TextPageState();
}

class _TextPageState extends State<TextPage> {
  final ScrollController scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
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
                scrollController: scrollController,
              );
            },
          ),
        ),
        TextInput(scrollController: scrollController),
      ],
    );
  }
}
