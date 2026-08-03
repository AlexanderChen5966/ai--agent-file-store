import 'package:test/test.dart';

import 'plate_validation_result.dart';
import 'plate_validator.dart';

void main() {
  test('純數字車號合法', () {
    final result = PlateValidator.validate('12');

    expect(result.isValid, isTrue);
    expect(result.normalized, '12');
    expect(result.message, '車號格式正確');
  });

  test('含字母車號合法', () {
    final result = PlateValidator.validate('ABC123');

    expect(result.isValid, isTrue);
    expect(result.reason, isNull);
  });

  test('含中間連字號車號合法', () {
    final result = PlateValidator.validate('AB-123');

    expect(result.isValid, isTrue);
    expect(result.normalized, 'AB-123');
  });

  test('小寫字母會正規化為大寫', () {
    final result = PlateValidator.validate(' ab-12 ');

    expect(result.isValid, isTrue);
    expect(result.normalized, 'AB-12');
  });

  test('七碼邊界合法', () {
    expect(PlateValidator.validate('ABC1234').isValid, isTrue);
  });

  test('少於兩碼太短', () {
    final result = PlateValidator.validate('A');

    expect(result.isValid, isFalse);
    expect(result.reason, PlateValidationFailReason.tooShort);
  });

  test('超過七碼太長', () {
    final result = PlateValidator.validate('ABC12345');

    expect(result.isValid, isFalse);
    expect(result.reason, PlateValidationFailReason.tooLong);
  });

  test('含非法字元', () {
    final result = PlateValidator.validate('AB_12');

    expect(result.isValid, isFalse);
    expect(result.reason, PlateValidationFailReason.invalidChar);
  });

  test('連字號位於開頭或結尾不合法', () {
    expect(
      PlateValidator.validate('-AB12').reason,
      PlateValidationFailReason.invalidHyphen,
    );
    expect(
      PlateValidator.validate('AB12-').reason,
      PlateValidationFailReason.invalidHyphen,
    );
  });

  test('連字號超過一個不合法', () {
    final result = PlateValidator.validate('A-B-12');

    expect(result.isValid, isFalse);
    expect(result.reason, PlateValidationFailReason.invalidHyphen);
  });
}
