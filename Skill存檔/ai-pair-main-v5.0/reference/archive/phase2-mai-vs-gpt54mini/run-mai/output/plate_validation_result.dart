enum PlateValidationFailReason {
  tooShort,
  tooLong,
  invalidChar,
  invalidHyphen,
}

class PlateValidationResult {
  const PlateValidationResult._({
    required this.isValid,
    required this.normalized,
    this.reason,
  });

  factory PlateValidationResult.valid(String normalized) {
    return PlateValidationResult._(
      isValid: true,
      normalized: normalized,
    );
  }

  factory PlateValidationResult.fail(
    PlateValidationFailReason reason,
    String normalized,
  ) {
    return PlateValidationResult._(
      isValid: false,
      normalized: normalized,
      reason: reason,
    );
  }

  final bool isValid;
  final String normalized;
  final PlateValidationFailReason? reason;

  String get message {
    if (isValid) {
      return '車號格式正確';
    }

    switch (reason) {
      case PlateValidationFailReason.tooShort:
        return '車號長度至少為 2 碼';
      case PlateValidationFailReason.tooLong:
        return '車號長度不可超過 7 碼';
      case PlateValidationFailReason.invalidChar:
        return '車號只能包含大寫英文字母、數字與單一連字號';
      case PlateValidationFailReason.invalidHyphen:
        return '連字號只能出現在中間，且最多只能有一個';
      case null:
        return '車號格式不正確';
    }
  }
}
