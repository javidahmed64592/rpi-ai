// Flutter imports:
import 'package:flutter/material.dart';

class TextFormatHelper {
  static List<TextSpan> createBulletPoints(String text, TextStyle? style) {
    final RegExp bulletExp = RegExp(r'^\* (.*)', multiLine: true);
    final List<TextSpan> spans = [];
    int start = 0;

    for (final Match match in bulletExp.allMatches(text)) {
      if (match.start > start) {
        spans.add(TextSpan(
          text: text.substring(start, match.start),
          style: style,
        ));
      }
      spans.add(TextSpan(
        text: '- ${match.group(1)}',
        style: style,
      ));
      start = match.end;
    }

    if (start < text.length) {
      spans.add(TextSpan(
        text: text.substring(start),
        style: style,
      ));
    }

    return spans;
  }

  static List<TextSpan> createBoldItalicText(String text, TextStyle? style) {
    final RegExp boldItalicExp = RegExp(r'\*\*\*(.*?)\*\*\*');
    final List<TextSpan> spans = [];
    int start = 0;

    for (final Match match in boldItalicExp.allMatches(text)) {
      if (match.start > start) {
        spans.add(TextSpan(
          text: text.substring(start, match.start),
          style: style,
        ));
      }
      spans.add(TextSpan(
        text: match.group(1),
        style: style?.copyWith(
          fontWeight: FontWeight.bold,
          fontStyle: FontStyle.italic,
          fontSize: 16,
        ),
      ));
      start = match.end;
    }

    if (start < text.length) {
      spans.add(TextSpan(
        text: text.substring(start),
        style: style?.copyWith(fontSize: 16),
      ));
    }

    return spans;
  }

  static List<TextSpan> createBoldText(String text, TextStyle? style) {
    final RegExp boldExp = RegExp(r'\*\*(.*?)\*\*');
    final List<TextSpan> spans = [];
    int start = 0;

    for (final Match match in boldExp.allMatches(text)) {
      if (match.start > start) {
        spans.add(TextSpan(
          text: text.substring(start, match.start),
          style: style,
        ));
      }
      spans.add(TextSpan(
        text: match.group(1),
        style: style?.copyWith(
          fontWeight: FontWeight.bold,
          fontSize: 16,
        ),
      ));
      start = match.end;
    }

    if (start < text.length) {
      spans.add(TextSpan(
        text: text.substring(start),
        style: style?.copyWith(fontSize: 16),
      ));
    }

    return spans;
  }

  static List<TextSpan> createItalicText(String text, TextStyle? style) {
    final RegExp italicExp = RegExp(r'\*(.*?)\*');
    final List<TextSpan> spans = [];
    int start = 0;

    for (final Match match in italicExp.allMatches(text)) {
      if (match.start > start) {
        spans.add(TextSpan(
          text: text.substring(start, match.start),
          style: style,
        ));
      }
      spans.add(TextSpan(
        text: match.group(1),
        style: style?.copyWith(
          fontStyle: FontStyle.italic,
          fontSize: 16,
        ),
      ));
      start = match.end;
    }

    if (start < text.length) {
      spans.add(TextSpan(
        text: text.substring(start),
        style: style?.copyWith(fontSize: 16),
      ));
    }

    return spans;
  }

  static List<TextSpan> formatText(String text, TextStyle? style) {
    final List<TextSpan> bulletSpans = createBulletPoints(text, style);
    final List<TextSpan> finalSpans = [];

    for (final span in bulletSpans) {
      finalSpans.addAll(createBoldItalicText(span.text!, span.style));
    }

    final List<TextSpan> boldSpans = [];
    for (final span in finalSpans) {
      boldSpans.addAll(createBoldText(span.text!, span.style));
    }

    final List<TextSpan> italicSpans = [];
    for (final span in boldSpans) {
      italicSpans.addAll(createItalicText(span.text!, span.style));
    }

    return italicSpans;
  }
}
