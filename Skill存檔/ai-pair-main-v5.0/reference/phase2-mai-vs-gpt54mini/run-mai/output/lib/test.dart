class Matcher {
  const Matcher();

  bool matches(Object? value) => false;
  String describe(Object? value) => 'unexpected value';
}

class _IsTrueMatcher extends Matcher {
  const _IsTrueMatcher();

  @override
  bool matches(Object? value) => value == true;

  @override
  String describe(Object? value) => 'Expected true but got $value';
}

class _IsFalseMatcher extends Matcher {
  const _IsFalseMatcher();

  @override
  bool matches(Object? value) => value == false;

  @override
  String describe(Object? value) => 'Expected false but got $value';
}

class _IsNullMatcher extends Matcher {
  const _IsNullMatcher();

  @override
  bool matches(Object? value) => value == null;

  @override
  String describe(Object? value) => 'Expected null but got $value';
}

const Matcher isTrue = _IsTrueMatcher();
const Matcher isFalse = _IsFalseMatcher();
const Matcher isNull = _IsNullMatcher();

void group(String description, void Function() body) {
  body();
}

void test(String description, void Function() body) {
  body();
}

void expect(Object? actual, Object? expected) {
  if (expected is Matcher) {
    if (!expected.matches(actual)) {
      throw StateError(expected.describe(actual));
    }
    return;
  }

  if (actual != expected) {
    throw StateError('Expected $expected but got $actual');
  }
}
