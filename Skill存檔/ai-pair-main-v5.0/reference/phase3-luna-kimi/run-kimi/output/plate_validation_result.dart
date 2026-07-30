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

  const PlateValidationResult.fail(
    this.reason,
    this.normalized,
  )   : isValid = false;

  String get message {
    if (isValid) return '車號格式正確';

    switch (reason!) {
      case PlateValidationFailReason.tooShort:
        return '車號長度過短，至少需要 2 碼';
      case PlateValidationFailReason.tooLong:
        return '車號長度過長，最多 7 碼';
      case PlateValidationFailReason.invalidChar:
        return '車號包含非法字元，僅允許大寫字母、數字與連字號';
      case PlateValidationFailReason.invalidHyphen:
        return '連字號位置錯誤或數量超過一個';
    }
  }
}
