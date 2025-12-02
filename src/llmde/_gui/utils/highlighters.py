"""Syntax highlighters for Markdown and JSON content."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from PyQt6.QtGui import QColor, QFont, QSyntaxHighlighter, QTextCharFormat

if TYPE_CHECKING:
    from PyQt6.QtGui import QTextDocument


class MarkdownHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for Markdown content.

    Parameters
    ----------
    document : QTextDocument
        The document to highlight.
    """

    def __init__(self, document: QTextDocument) -> None:
        super().__init__(document)
        self._highlighting_rules: list[tuple[re.Pattern, QTextCharFormat]] = []
        self._setup_formats()
        self._setup_rules()

    def _setup_formats(self) -> None:
        """Set up text formats for different markdown elements."""
        # Headers (H1-H6)
        self._header_format = QTextCharFormat()
        self._header_format.setForeground(QColor("#0066cc"))
        self._header_format.setFontWeight(QFont.Weight.Bold)

        # Bold text
        self._bold_format = QTextCharFormat()
        self._bold_format.setFontWeight(QFont.Weight.Bold)
        self._bold_format.setForeground(QColor("#333333"))

        # Italic text
        self._italic_format = QTextCharFormat()
        self._italic_format.setFontItalic(True)
        self._italic_format.setForeground(QColor("#555555"))

        # Code (inline and blocks)
        self._code_format = QTextCharFormat()
        self._code_format.setForeground(QColor("#d14"))
        self._code_format.setBackground(QColor("#f5f5f5"))
        self._code_format.setFontFamily("Consolas")

        # Links
        self._link_format = QTextCharFormat()
        self._link_format.setForeground(QColor("#0066cc"))
        self._link_format.setFontUnderline(True)

        # List items
        self._list_format = QTextCharFormat()
        self._list_format.setForeground(QColor("#666666"))

        # Blockquote
        self._blockquote_format = QTextCharFormat()
        self._blockquote_format.setForeground(QColor("#888888"))
        self._blockquote_format.setFontItalic(True)

        # Horizontal rule
        self._hr_format = QTextCharFormat()
        self._hr_format.setForeground(QColor("#cccccc"))

    def _setup_rules(self) -> None:
        """Set up highlighting rules."""
        # Headers: # Header, ## Header, etc.
        self._highlighting_rules.append(
            (re.compile(r"^#{1,6}\s+.+$", re.MULTILINE), self._header_format)
        )

        # Bold: **text** or __text__
        self._highlighting_rules.append(
            (re.compile(r"\*\*[^*]+\*\*"), self._bold_format)
        )
        self._highlighting_rules.append((re.compile(r"__[^_]+__"), self._bold_format))

        # Italic: *text* or _text_
        self._highlighting_rules.append(
            (re.compile(r"(?<!\*)\*(?!\*)[^*]+\*(?!\*)"), self._italic_format)
        )
        self._highlighting_rules.append(
            (re.compile(r"(?<!_)_(?!_)[^_]+_(?!_)"), self._italic_format)
        )

        # Inline code: `code`
        self._highlighting_rules.append((re.compile(r"`[^`]+`"), self._code_format))

        # Links: [text](url)
        self._highlighting_rules.append(
            (re.compile(r"\[[^\]]+\]\([^)]+\)"), self._link_format)
        )

        # Unordered list items: - item, * item, + item
        self._highlighting_rules.append(
            (re.compile(r"^\s*[-*+]\s+", re.MULTILINE), self._list_format)
        )

        # Ordered list items: 1. item
        self._highlighting_rules.append(
            (re.compile(r"^\s*\d+\.\s+", re.MULTILINE), self._list_format)
        )

        # Blockquote: > text
        self._highlighting_rules.append(
            (re.compile(r"^>\s+.+$", re.MULTILINE), self._blockquote_format)
        )

        # Horizontal rule: ---, ***, ___
        self._highlighting_rules.append(
            (re.compile(r"^[-*_]{3,}$", re.MULTILINE), self._hr_format)
        )

    def highlightBlock(self, text: str) -> None:
        """Highlight a block of text.

        Parameters
        ----------
        text : str
            The text to highlight.
        """
        for pattern, fmt in self._highlighting_rules:
            for match in pattern.finditer(text):
                start = match.start()
                length = match.end() - start
                self.setFormat(start, length, fmt)


class JSONHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for JSON content.

    Parameters
    ----------
    document : QTextDocument
        The document to highlight.
    """

    def __init__(self, document: QTextDocument) -> None:
        super().__init__(document)
        self._highlighting_rules: list[tuple[re.Pattern, QTextCharFormat]] = []
        self._setup_formats()
        self._setup_rules()

    def _setup_formats(self) -> None:
        """Set up text formats for different JSON elements."""
        # Keys (property names)
        self._key_format = QTextCharFormat()
        self._key_format.setForeground(QColor("#9cdcfe"))  # Light blue

        # String values
        self._string_format = QTextCharFormat()
        self._string_format.setForeground(QColor("#ce9178"))  # Orange/salmon

        # Numbers
        self._number_format = QTextCharFormat()
        self._number_format.setForeground(QColor("#b5cea8"))  # Light green

        # Booleans and null
        self._keyword_format = QTextCharFormat()
        self._keyword_format.setForeground(QColor("#569cd6"))  # Blue
        self._keyword_format.setFontWeight(QFont.Weight.Bold)

        # Brackets and braces
        self._bracket_format = QTextCharFormat()
        self._bracket_format.setForeground(QColor("#ffd700"))  # Gold

        # Colon and comma
        self._punctuation_format = QTextCharFormat()
        self._punctuation_format.setForeground(QColor("#d4d4d4"))  # Light gray

    def _setup_rules(self) -> None:
        """Set up highlighting rules."""
        # Keys: "key":
        self._highlighting_rules.append(
            (re.compile(r'"[^"]*"\s*(?=:)'), self._key_format)
        )

        # String values (after colon)
        self._highlighting_rules.append(
            (re.compile(r'(?<=:\s)"[^"]*"'), self._string_format)
        )

        # String values in arrays
        self._highlighting_rules.append(
            (re.compile(r'(?<=[\[,]\s*)"[^"]*"(?=\s*[,\]])'), self._string_format)
        )

        # Numbers (integers and floats)
        self._highlighting_rules.append(
            (re.compile(r"-?\b\d+\.?\d*([eE][+-]?\d+)?\b"), self._number_format)
        )

        # Booleans
        self._highlighting_rules.append(
            (re.compile(r"\b(true|false)\b"), self._keyword_format)
        )

        # Null
        self._highlighting_rules.append((re.compile(r"\bnull\b"), self._keyword_format))

        # Brackets and braces
        self._highlighting_rules.append((re.compile(r"[\[\]{}]"), self._bracket_format))

    def highlightBlock(self, text: str) -> None:
        """Highlight a block of text.

        Parameters
        ----------
        text : str
            The text to highlight.
        """
        for pattern, fmt in self._highlighting_rules:
            for match in pattern.finditer(text):
                start = match.start()
                length = match.end() - start
                self.setFormat(start, length, fmt)
