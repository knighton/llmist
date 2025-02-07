# The Joy of Unicode

“Unicode is the mind-killer” -George Washington 

## 1. Unicode Normalization Forms

  - NFC, NFD (canonical)
  - NFKC, NFKD (compatibility)

## 2. ASCII Control Characters (0x00-0x1F, 0x7F)

  - Null byte
  - Line/paragraph separators
  - Form feed, vertical tab, etc.

## 3. Whitespace Characters

  - Space (U+0020)
  - Non-breaking space (U+00A0)
  - Zero-width space (U+200B)
  - Em/en space (U+2003/U+2002)
  - Thin/hair space (U+2009/U+200A)
  - Ideographic space (U+3000)
  - Figure space (U+2007)
  - Punctuation space (U+2008)
  - Mathematical space (U+205F)
  - Narrow no-break space (U+202F)
  - Medium mathematical space (U+205F)

## 4. Combining Characters

  - Diacritical marks (U+0300-U+036F)
  - Extended combining marks
  - Enclosing marks
  - Multiple stacked combining characters
  - Vowel signs and virama

## 5. Bidirectional Controls

  - LTR/RTL marks (U+200E/U+200F)
  - LTR/RTL embeddings (U+202A/U+202B)
  - LTR/RTL overrides (U+202D/U+202E)
  - Pop directional formatting (U+202C)
  - First strong isolate (U+2068)
  - Pop directional isolate (U+2069)

## 6. Zero-width Characters

  - Joiner/non-joiner (U+200D/U+200C)
  - Space (U+200B)
  - Word joiner (U+2060)
  - No-break (U+FEFF)
  - Soft hyphen (U+00AD)

## 7. Variation Selectors

  - Standard variations (U+FE00-U+FE0F)
  - Ideographic variations (U+E0100-U+E01EF)
  - Emoji variations
  - Text presentation vs emoji presentation

## 8. Homoglyphs

  - Latin/Cyrillic/Greek crossovers
  - Digits across scripts
  - Punctuation marks
  - Mathematical symbols
  - Different script versions (fullwidth/halfwidth)
  - Enclosed/circled variants
  - Superscript/subscript forms

## 9. Line/Paragraph Separators

  - CR, LF, CRLF
  - Line separator (U+2028)
  - Paragraph separator (U+2029)
  - Next line (U+0085)

## 10. Mathematical Variants

  - Bold/italic math symbols
  - Double-struck characters
  - Script/cursive forms
  - Fraktur variants

## 11. Width and Height Variants

  - Fullwidth forms (U+FF00-U+FFEF)
  - Halfwidth forms
  - Small forms
  - Vertical forms
  - Stretched/compressed forms

## 12. Special Processing Characters

  - Byte order mark (BOM)
  - Interlinear annotation markers
  - Object replacement character
  - Language tag characters

## 13. Contextual Forms

  - Initial/medial/final forms
  - Isolated forms
  - Ligatures
  - Contextual alternates

## 14. Phonetic Extensions

  - IPA extensions
  - Modifier letters
  - Tone letters
  - Extended IPA

## 15. Format Controls

  - Joiners and non-joiners
  - Inhibit symmetric swapping (U+206A)
  - Activate symmetric swapping (U+206B)
  - National digit shapes (U+206E/U+206F)

## 16. Numeric Variants

  - Native digits of different scripts
  - Circled/parenthesized numbers
  - Subscript/superscript numbers
  - Roman numerals
  - Fractions

## 17. Invisible Operators

  - Function application (U+2061)
  - Invisible times (U+2062)
  - Invisible separator (U+2063)
  - Invisible plus (U+2064)

## 18. Special-Purpose Characters

  - Tag characters (U+E0000-U+E007F)
  - Variation selectors supplement
  - Private use areas
  - Surrogate code points

## 19. Text Presentation Controls

  - Ideographic space
  - Word joiner vs zero-width non-break space
  - Mongolian vowel separator
  - Various quotation marks

## 20. Character Property Variants

  - Default ignorable code points
  - Deprecated characters
  - Noncharacters
  - Unassigned code points
