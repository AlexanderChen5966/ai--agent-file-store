import 'package:flutter_test/flutter_test.dart';

import 'plate_validation_result.dart';
import 'plate_validator.dart';

void main() {
  group('PlateValidator.validate', () {
    test('純數字車號合法', () {
      final result = PlateValidator.validate('1234');
      expect(result.isValid, isTrue);
      expect(result.normalized, equals('1234'));
      expect(result.message, equals('車號格式正確'));
    });

    test('含字母車號合法', () {
      final result = PlateValidator.validate('AB123');
      expect(result.isValid, isTrue);
      expect(result.normalized, equals('AB123'));
      expect(result.message, equals('車號格式正確'));
    });

    test('含中間連字號車號合法', () {
      final result = PlateValidator.validate('AB-123');
      expect(result.isValid, isTrue);
      expect(result.normalized, equals('AB-123'));
      expect(result.message, equals('車號格式正確'));
    });

    test('小寫英文自動轉大寫', () {
      final result = PlateValidator.validate('ab-12');
      expect(result.isValid, isTrue);
      expect(result.normalized, equals('AB-12'));
      expect(result.message, equals('車號格式正確'));
    });

    test('車號太短應回傳 tooShort', () {
      final result = PlateValidator.validate('A');
      expect(result.isValid, isFalse);
      expect(result.reason, equals(PlateValidationFailReason.tooShort));
      expect(result.normalized, equals('A'));
    });

    test('車號太長應回傳 tooLong', () {
      final result = PlateValidator.validate('ABCDEFGH');
      expect(result.isValid, isFalse);
      expect(result.reason, equals(PlateValidationFailReason.tooLong));
      expect(result.normalized, equals('ABCDEFGH'));
    });

    test('包含非法字元應回傳 invalidChar', () {
      final result = PlateValidator.validate('AB@12');
      expect(result.isValid, isFalse);
      expect(result.reason, equals(PlateValidationFailReason.invalidChar));
      expect(result.normalized, equals('AB@12'));
    });

    test('連字號在開頭應回傳 invalidHyphen', () {
      final result = PlateValidator.validate('-AB12');
      expect(result.isValid, isFalse);
      expect(result.reason, equals(PlateValidationFailReason.invalidHyphen));
      expect(result.normalized, equals('-AB12'));
    });

    test('連字號在結尾應回傳 invalidHyphen', () {
      final result = PlateValidator.validate('AB12-');
      expect(result.isValid, isFalse);
      expect(result.reason, equals(PlateValidationFailReason.invalidHyphen));
      expect(result.normalized, equals('AB12-'));
    });

    test('多個連字號應回傳 invalidHyphen', () {
      final result = PlateValidator.validate('A-B-C');
      expect(result.isValid, isFalse);
      expect(result.reason, equals(PlateValidationFailReason.invalidHyphen));
      expect(result.normalized, equals('A-B-C'));
    });

    test('2 碼邊界值合法', () {
      final result = PlateValidator.validate('AB');
      expect(result.isValid, isTrue);
      expect(result.normalized, equals('AB'));
    });

    test('7 碼邊界值合法', () {
      final result = PlateValidator.validate('A123456');
      expect(result.isValid, isTrue);
      expect(result.normalized, equals('A123456'));
    });

    test('前後空白應自動去除', () {
      final result = PlateValidator.validate('  abc  ');
      expect(result.isValid, isTrue);
      expect(result.normalized, equals('ABC'));
    });
  });

  group('PlateValidator.normalize', () {
    test('normalize 應去除空白並轉大寫', () {
      expect(PlateValidator.normalize('  ab-12  '), equals('AB-12'));
    });
  });
}
