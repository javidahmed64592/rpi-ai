// Flutter imports:
import 'package:flutter/material.dart';

// Package imports:
import 'package:flutter_test/flutter_test.dart';

// Project imports:
import 'package:ui/helpers/text_format_helper.dart';

void main() {
  test('createBoldText formats bold text correctly', () {
    const text = 'This is **bold** text';
    final spans = TextFormatHelper.createBoldText(text, const TextStyle());

    expect(spans.length, 3);
    expect(spans[0].text, 'This is ');
    expect(spans[1].text, 'bold');
    expect(spans[1].style?.fontWeight, FontWeight.bold);
    expect(spans[2].text, ' text');
  });

  test('createItalicText formats italic text correctly', () {
    const text = 'This is *italic* text';
    final spans = TextFormatHelper.createItalicText(text, const TextStyle());

    expect(spans.length, 3);
    expect(spans[0].text, 'This is ');
    expect(spans[1].text, 'italic');
    expect(spans[1].style?.fontStyle, FontStyle.italic);
    expect(spans[2].text, ' text');
  });

  test('createBoldItalicText formats bold and italic text correctly', () {
    const text = 'This is ***bold and italic*** text';
    final spans =
        TextFormatHelper.createBoldItalicText(text, const TextStyle());

    expect(spans.length, 3);
    expect(spans[0].text, 'This is ');
    expect(spans[1].text, 'bold and italic');
    expect(spans[1].style?.fontWeight, FontWeight.bold);
    expect(spans[1].style?.fontStyle, FontStyle.italic);
    expect(spans[2].text, ' text');
  });

  test('createBulletPoints formats bullet points correctly', () {
    const text = '* Bullet point 1\n* Bullet point 2';
    final spans = TextFormatHelper.createBulletPoints(text, const TextStyle());

    expect(spans.length, 3);
    expect(spans[0].text, '- Bullet point 1');
    expect(spans[1].text, '\n');
    expect(spans[2].text, '- Bullet point 2');
  });

  test('formatText applies all formatting correctly', () {
    const text =
        '*   **Item 1 - Bold item**\n*   *Item 2 - Italicized item*\n*   ***Item 3 - Bold and italicized item***';
    final spans = TextFormatHelper.formatText(text, const TextStyle());

    expect(spans.length, 8);
    expect(spans[0].text, '-   ');
    expect(spans[1].text, 'Item 1 - Bold item');
    expect(spans[1].style?.fontWeight, FontWeight.bold);
    expect(spans[2].text, '\n');
    expect(spans[3].text, '-   ');
    expect(spans[4].text, 'Item 2 - Italicized item');
    expect(spans[4].style?.fontStyle, FontStyle.italic);
    expect(spans[5].text, '\n');
    expect(spans[6].text, '-   ');
    expect(spans[7].text, 'Item 3 - Bold and italicized item');
    expect(spans[7].style?.fontWeight, FontWeight.bold);
    expect(spans[7].style?.fontStyle, FontStyle.italic);
  });
}
