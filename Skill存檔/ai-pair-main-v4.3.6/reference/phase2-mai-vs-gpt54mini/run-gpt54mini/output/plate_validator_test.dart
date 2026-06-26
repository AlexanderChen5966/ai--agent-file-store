import 'plate_validation_result.dart';
import 'plate_validator.dart';

typedef TestBody = void Function();

void test(String description, TestBody body) {
  try {
    body();
    print('PASS: $description');
  } catch (error, stackTrace) {
    print('FAIL: $description');
    print(error);
    print(stackTrace);
    rethrow;
  }
}

void expect(Object? actual, Object? expected, [String? reason]) {
  if (actual != expected) {
    throw StateError(
      reason ??
          'Expected <$expected>, but got <$actual>.',
    );
  }
}

void main() {
  test('normalize 會去空白並轉大寫', () {
    expect(PlateValidator.normalize('  ab-12  '), 'AB-12');
  });

  test('純數字車號在 2 碼邊界仍然合法', () {
    final result = PlateValidator.validate('12');
    expect(result.isValid, true);
    expect(result.normalized, '12');
    expect(result.message, '車號格式正確');
  });

  test('7 碼含連字號的車號仍然合法', () {
    final result = PlateValidator.validate('ABC-123');
    expect(result.isValid, true);
    expect(result.normalized, 'ABC-123');
  });

  test('含字母與數字的車號合法', () {
    final result = PlateValidator.validate('a7');
    expect(result.isValid, true);
    expect(result.normalized, 'A7');
  });

  test('含中間連字號的車號合法', () {
    final result = PlateValidator.validate('ab-12');
    expect(result.isValid, true);
    expect(result.normalized, 'AB-12');
  });

  test('太短時回傳 tooShort', () {
    final result = PlateValidator.validate('A');
    expect(result.isValid, false);
    expect(result.reason, PlateValidationFailReason.tooShort);
    expect(result.message, '車號長度不足');
  });

  test('太長時回傳 tooLong', () {
    final result = PlateValidator.validate('ABCDEFGH');
    expect(result.isValid, false);
    expect(result.reason, PlateValidationFailReason.tooLong);
    expect(result.message, '車號長度過長');
  });

  test('非法字元時回傳 invalidChar', () {
    final result = PlateValidator.validate('AB_12');
    expect(result.isValid, false);
    expect(result.reason, PlateValidationFailReason.invalidChar);
    expect(result.message, '車號只能包含大寫英文字母、數字與連字號');
  });

  test('連字號在開頭時回傳 invalidHyphen', () {
    final result = PlateValidator.validate('-AB');
    expect(result.isValid, false);
    expect(result.reason, PlateValidationFailReason.invalidHyphen);
    expect(result.message, '連字號位置不正確');
  });

  test('多個連字號時回傳 invalidHyphen', () {
    final result = PlateValidator.validate('A--B');
    expect(result.isValid, false);
    expect(result.reason, PlateValidationFailReason.invalidHyphen);
  });
}
