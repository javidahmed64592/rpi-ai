// Flutter imports:
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class MessageContainer extends StatelessWidget {
  final String message;
  final bool isUserMessage;
  final DateTime timestamp;

  const MessageContainer({
    Key? key,
    required this.message,
    required this.isUserMessage,
    required this.timestamp,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final boxColour = isUserMessage
        ? Theme.of(context).colorScheme.primary
        : Theme.of(context).colorScheme.secondary;
    final textColour = isUserMessage
        ? Theme.of(context).colorScheme.onPrimary
        : Theme.of(context).colorScheme.onSecondary;

    void copyToClipboard() {
      Clipboard.setData(ClipboardData(text: message));
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Copied to clipboard')),
      );
    }

    return GestureDetector(
      onLongPress: copyToClipboard,
      child: Align(
        alignment: isUserMessage ? Alignment.centerRight : Alignment.centerLeft,
        child: Column(
          crossAxisAlignment:
              isUserMessage ? CrossAxisAlignment.end : CrossAxisAlignment.start,
          children: [
            MessageBox(
              message: message,
              boxColour: boxColour,
              textColour: textColour,
            ),
            MessageTimestamp(timestamp: timestamp),
          ],
        ),
      ),
    );
  }
}

class MessageBox extends StatelessWidget {
  final String message;
  final Color boxColour;
  final Color textColour;

  const MessageBox({
    Key? key,
    required this.message,
    required this.boxColour,
    required this.textColour,
  }) : super(key: key);

  List<TextSpan> _getFormattedText(String text, Color textColour) {
    final RegExp boldExp = RegExp(r'\*\*(.*?)\*\*');
    final RegExp bulletExp = RegExp(r'^\* (.*)', multiLine: true);
    final List<TextSpan> spans = [];
    int start = 0;

    for (final Match match in bulletExp.allMatches(text)) {
      if (match.start > start) {
        spans.add(TextSpan(
          text: text.substring(start, match.start),
          style: TextStyle(color: textColour),
        ));
      }
      spans.add(TextSpan(
        text: '- ${match.group(1)}',
        style: TextStyle(color: textColour),
      ));
      start = match.end;
    }

    if (start < text.length) {
      spans.add(TextSpan(
        text: text.substring(start),
        style: TextStyle(color: textColour),
      ));
    }

    final List<TextSpan> finalSpans = [];
    for (final span in spans) {
      final text = span.text!;
      int boldStart = 0;
      for (final Match match in boldExp.allMatches(text)) {
        if (match.start > boldStart) {
          finalSpans.add(TextSpan(
            text: text.substring(boldStart, match.start),
            style: span.style,
          ));
        }
        finalSpans.add(TextSpan(
          text: match.group(1),
          style: span.style?.copyWith(
            fontWeight: FontWeight.bold,
            fontSize: 16,
          ),
        ));
        boldStart = match.end;
      }
      if (boldStart < text.length) {
        finalSpans.add(TextSpan(
          text: text.substring(boldStart),
          style: span.style?.copyWith(fontSize: 16),
        ));
      }
    }

    return finalSpans;
  }

  @override
  Widget build(BuildContext context) {
    final maxWidth = MediaQuery.of(context).size.width * 0.75;
    return Container(
      constraints: BoxConstraints(maxWidth: maxWidth),
      margin: const EdgeInsets.symmetric(vertical: 5),
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: boxColour,
        borderRadius: BorderRadius.circular(10),
      ),
      child: RichText(
        text: TextSpan(
          children: _getFormattedText(message, textColour),
          style: const TextStyle(fontSize: 16),
        ),
      ),
    );
  }
}

class MessageTimestamp extends StatelessWidget {
  final DateTime timestamp;

  const MessageTimestamp({
    Key? key,
    required this.timestamp,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final String dateText =
        '${timestamp.day.toString().padLeft(2, '0')}/${timestamp.month.toString().padLeft(2, '0')}/${timestamp.year.toString().substring(2)}';
    final String timeText =
        '${timestamp.hour.toString().padLeft(2, '0')}:${timestamp.minute.toString().padLeft(2, '0')}';
    final String text = '$dateText | $timeText';
    final Color textColour = Theme.of(context).colorScheme.onBackground;
    final TextStyle textStyle =
        TextStyle(color: textColour.withOpacity(0.6), fontSize: 12);
    return Text(text, style: textStyle);
  }
}
