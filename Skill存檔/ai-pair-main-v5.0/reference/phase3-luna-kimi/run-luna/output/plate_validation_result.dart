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
    switch (reason) {
      case null:
        return '車號格式正確';
      case PlateValidationFailReason.tooShort:
        return '車號長度不可少於 2 碼';
      case PlateValidationFailReason.tooLong:
        return '車號長度不可超過 7 碼';
      case PlateValidationFailReason.invalidChar:
        return '車號僅允許英文字母、數字與連字號';
      case PlateValidationFailReason.invalidHyphen:
        return '連字號不可位於開頭或結尾，且最多一個';
    }
  }
}
