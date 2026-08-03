import 'plate_validation_result.dart';

class PlateValidator {
  /// 去除前後空白並將英文字母轉為大寫，供外部重用。
  static String normalize(String input) {
    return input.trim().toUpperCase();
  }

  /// 驗證車號格式，回傳包含驗證結果、正規化字串與錯誤原因的物件。
  static PlateValidationResult validate(String input) {
    final normalized = normalize(input);
    final length = normalized.length;

    if (length < 2) {
      return PlateValidationResult.fail(
        PlateValidationFailReason.tooShort,
        normalized,
      );
    }

    if (length > 7) {
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
}
