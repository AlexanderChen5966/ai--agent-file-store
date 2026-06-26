enum PlateValidationFailReason {
  tooShort,
  tooLong,
  invalidChar,
  invalidHyphen,
}

class PlateValidationResult {
  final bool isValid;
  final String normalized;
  final PlateValidationFailReason? reason;

  const PlateValidationResult.valid(this.normalized)
      : isValid = true,
        reason = null;

  const PlateValidationResult.fail(this.reason, this.normalized)
      : isValid = false;

  String get message {
    if (isValid) {
      return '車號格式正確';
    }

    switch (reason) {
      case PlateValidationFailReason.tooShort:
        return '車號長度不足';
      case PlateValidationFailReason.tooLong:
        return '車號長度過長';
      case PlateValidationFailReason.invalidChar:
        return '車號只能包含大寫英文字母、數字與連字號';
      case PlateValidationFailReason.invalidHyphen:
        return '連字號位置不正確';
      case null:
        return '車號格式有誤';
    }
  }
}
