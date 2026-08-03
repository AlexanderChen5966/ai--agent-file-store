import 'plate_validation_result.dart';

class PlateValidator {
  static PlateValidationResult validate(String input) {
    final normalized = normalize(input);

    if (normalized.length < 2) {
      return PlateValidationResult.fail(
        PlateValidationFailReason.tooShort,
        normalized,
      );
    }

    if (normalized.length > 7) {
      return PlateValidationResult.fail(
        PlateValidationFailReason.tooLong,
        normalized,
      );
    }

    if (!_containsOnlyAllowedCharacters(normalized)) {
      return PlateValidationResult.fail(
        PlateValidationFailReason.invalidChar,
        normalized,
      );
    }

    if (!_hasValidHyphenPlacement(normalized)) {
      return PlateValidationResult.fail(
        PlateValidationFailReason.invalidHyphen,
        normalized,
      );
    }

    return PlateValidationResult.valid(normalized);
  }

  static String normalize(String input) {
    return input.trim().toUpperCase();
  }

  static bool _containsOnlyAllowedCharacters(String value) {
    for (final char in value.split('')) {
      if (!_isAllowedCharacter(char)) {
        return false;
      }
    }
    return true;
  }

  static bool _isAllowedCharacter(String char) {
    return char.codeUnitAt(0) >= 48 && char.codeUnitAt(0) <= 57 ||
        char.codeUnitAt(0) >= 65 && char.codeUnitAt(0) <= 90 ||
        char == '-';
  }

  static bool _hasValidHyphenPlacement(String value) {
    final hyphenCount = value.split('-').length - 1;

    if (hyphenCount > 1) {
      return false;
    }

    if (hyphenCount == 0) {
      return true;
    }

    final hyphenIndex = value.indexOf('-');
    return hyphenIndex > 0 && hyphenIndex < value.length - 1;
  }
}
