import 'plate_validation_result.dart';

class PlateValidator {
  static final RegExp _allowedPattern = RegExp(r'^[A-Z0-9-]+$');

  static String normalize(String input) {
    return input.trim().toUpperCase();
  }

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

    if (!_allowedPattern.hasMatch(normalized)) {
      return PlateValidationResult.fail(
        PlateValidationFailReason.invalidChar,
        normalized,
      );
    }

    if (!_isHyphenPlacementValid(normalized)) {
      return PlateValidationResult.fail(
        PlateValidationFailReason.invalidHyphen,
        normalized,
      );
    }

    return PlateValidationResult.valid(normalized);
  }

  static bool _isHyphenPlacementValid(String value) {
    final hyphenIndex = value.indexOf('-');
    if (hyphenIndex == -1) {
      return true;
    }

    if (hyphenIndex == 0 || hyphenIndex == value.length - 1) {
      return false;
    }

    return value.indexOf('-', hyphenIndex + 1) == -1;
  }
}
