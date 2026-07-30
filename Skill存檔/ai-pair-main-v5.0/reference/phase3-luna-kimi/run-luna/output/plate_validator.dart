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
    if (!RegExp(r'^[A-Z0-9-]+$').hasMatch(normalized)) {
      return PlateValidationResult.fail(
        PlateValidationFailReason.invalidChar,
        normalized,
      );
    }

    final hyphenCount = '-'.allMatches(normalized).length;
    if (hyphenCount > 1 ||
        normalized.startsWith('-') ||
        normalized.endsWith('-')) {
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
}
