import 'package:test/test.dart';

import 'plate_validation_result.dart';
import 'plate_validator.dart';

void main() {
  group('PlateValidator', () {
    test('accepts numeric plates', () {
      final result = PlateValidator.validate('1234');
      expect(result.isValid, isTrue);
      expect(result.normalized, '1234');
      expect(result.reason, isNull);
      expect(result.message, '車號格式正確');
    });

    test('accepts alphabetic plates', () {
      final result = PlateValidator.validate('ABC');
      expect(result.isValid, isTrue);
      expect(result.normalized, 'ABC');
    });

    test('accepts mixed plates', () {
      final result = PlateValidator.validate('AB12');
      expect(result.isValid, isTrue);
      expect(result.normalized, 'AB12');
    });

    test('accepts hyphenated plates', () {
      final result = PlateValidator.validate('AB-12');
      expect(result.isValid, isTrue);
      expect(result.normalized, 'AB-12');
    });

    test('normalizes lowercase input', () {
      final result = PlateValidator.validate(' ab12 ');
      expect(result.isValid, isTrue);
      expect(result.normalized, 'AB12');
    });

    test('rejects plates that are too short', () {
      final result = PlateValidator.validate('A');
      expect(result.isValid, isFalse);
      expect(result.reason, PlateValidationFailReason.tooShort);
      expect(result.message, '車號長度至少為 2 碼');
    });

    test('rejects plates that are too long', () {
      final result = PlateValidator.validate('ABCDEFGH');
      expect(result.isValid, isFalse);
      expect(result.reason, PlateValidationFailReason.tooLong);
      expect(result.message, '車號長度不可超過 7 碼');
    });

    test('rejects plates with invalid characters', () {
      final result = PlateValidator.validate('AB!');
      expect(result.isValid, isFalse);
      expect(result.reason, PlateValidationFailReason.invalidChar);
      expect(result.message, '車號只能包含大寫英文字母、數字與單一連字號');
    });

    test('rejects plates with invalid hyphen placement', () {
      final result = PlateValidator.validate('-ABC');
      expect(result.isValid, isFalse);
      expect(result.reason, PlateValidationFailReason.invalidHyphen);
      expect(result.message, '連字號只能出現在中間，且最多只能有一個');
    });

    test('rejects plates with multiple hyphens', () {
      final result = PlateValidator.validate('AB--12');
      expect(result.isValid, isFalse);
      expect(result.reason, PlateValidationFailReason.invalidHyphen);
    });

    test('normalizes input independently', () {
      expect(PlateValidator.normalize(' aB12 '), 'AB12');
    });
  });
}
