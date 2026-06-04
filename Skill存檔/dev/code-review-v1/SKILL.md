---
name: code-review
version: "1.0.0"
description: Comprehensive code review skill for Flutter + Riverpod projects, with automatic invocation of code-reviewer subagent for deep analysis. Use this skill when the user requests code review (e.g., "/review", "review this code", "check my changes") or after completing feature development. Focuses on Flutter Web architecture compliance (ConsumerState, SingleTaskState, CacheableState), Riverpod best practices, OAuth2 security, and project-specific coding standards.
---

# Code Review

Conduct thorough code reviews for Flutter + Riverpod projects with automatic quality checks and architectural compliance verification.

## Overview

This skill enables comprehensive code reviews focused on:

1. **State Management Architecture** - Verify correct usage of ConsumerState, SingleTaskState, and CacheableState
2. **Riverpod Best Practices** - Check ref.watch vs ref.read usage patterns
3. **Security Analysis** - OAuth2, API security, and sensitive data handling
4. **Code Quality** - Performance, maintainability, and style compliance
5. **Project Standards** - Adherence to minimal, incremental change policy

## Review Workflow

### Step 1: Identify Changed Files

Determine what files have been modified or created:

```bash
# Check git status for modified files
git status

# See detailed changes
git diff

# For staged changes
git diff --cached
```

If the user hasn't specified which files to review, ask them or check git status to identify the scope.

### Step 2: Determine Review Scope

Based on the changed files, identify the review focus:

**Page/Widget Changes** (lib/page/\*\*/\*.dart):
- Check State type selection (ConsumerState, SingleTaskState, CacheableState)
- Verify lifecycle methods (initState, dispose, onVisibleChange, onRefresh)
- Review UI structure and Scaffold usage

**StateNotifier Changes** (lib/api/notifier/\*\*/\*.dart):
- Check Riverpod state management patterns
- Verify TaskManager usage for critical operations
- Review API call handling and error management

**API/Request/Response Changes** (lib/api/\*\*/\*.dart):
- Verify Retrofit usage and annotations
- Check request/response serialization
- Review API security and validation

**Utility/Widget Changes** (lib/util/\*\*/\*.dart, lib/page/common/widgets/\*.dart):
- Check for reusability and proper abstraction
- Verify consistent usage of project utilities
- Review const optimization

### Step 3: Invoke Code-Reviewer Subagent

Launch the specialized code-reviewer agent to perform deep analysis:

```dart
// Use the Task tool to invoke the code-reviewer subagent
Task(
  subagent_type: 'code-reviewer',
  description: 'Review Flutter code changes',
  prompt: '''
  Review the following code changes for a Flutter + Riverpod Web project:

  Files to review:
  [List of changed files with paths]

  Focus areas:
  1. State management architecture (ConsumerState/SingleTaskState/CacheableState)
  2. Riverpod usage (ref.watch vs ref.read)
  3. Lifecycle management (initState, dispose)
  4. Security (OAuth2, sensitive data handling)
  5. Code quality (performance, maintainability, style)
  6. Project compliance (minimal changes, architecture consistency)

  Project context:
  - Flutter Web application (no mobile)
  - Riverpod for state management
  - OAuth2 with PKCE for authentication
  - TaskManager singleton for critical operations
  - See CLAUDE.md for complete architecture rules

  Reference the review checklist in references/review-checklist.md for detailed criteria.
  '''
)
```

**Important**: Always pass the code-reviewer subagent:
- List of files to review
- Specific focus areas based on file types
- Project context (Flutter Web, Riverpod, OAuth2, etc.)
- Reference to review-checklist.md

### Step 4: Process Review Results

After the code-reviewer agent completes:

1. **Categorize Findings** by severity:
   - 🔴 **Critical**: Security issues, architecture violations, breaking changes
   - 🟡 **Warning**: Code smells, performance concerns, style inconsistencies
   - 🟢 **Suggestion**: Optional improvements, refactoring opportunities

2. **Prioritize Issues**:
   - Address critical issues first (security, architecture)
   - Group related issues together
   - Provide actionable fix recommendations

3. **Generate Report** with:
   - Summary of review scope
   - Categorized findings with file locations and line numbers
   - Specific recommendations for each issue
   - Compliance checklist results

### Step 5: Present Review Summary

Format the review results for the user:

```markdown
## Code Review Summary

**Files Reviewed**: [Count] files
**State Type**: [ConsumerState/SingleTaskState/CacheableState/Mixed]
**Overall Status**: [✅ Approved / ⚠️ Needs Attention / ❌ Requires Changes]

### Critical Issues (🔴)
[List critical issues with file:line references]

### Warnings (🟡)
[List warnings with file:line references]

### Suggestions (🟢)
[List optional improvements]

### Compliance Checklist
- [x] State type selection correct
- [x] Riverpod usage patterns correct
- [ ] All resources properly disposed
- [x] No hardcoded values or magic numbers
- [ ] Security best practices followed

### Recommendations
1. [Specific actionable recommendation]
2. [Another recommendation]

### References
- See [references/review-checklist.md](references/review-checklist.md) for detailed criteria
- See docs/widget/STATE_MANAGEMENT_GUIDE.md for State type selection guide
- See CLAUDE.md for complete architecture rules
```

## Review Categories

### State Management Review

**For ConsumerState pages**:
- [ ] Inherits `StatefulHookConsumerWidget` and `ConsumerState<T>`
- [ ] Defines `static const String ROUTE_NAME`
- [ ] Uses `const` constructor
- [ ] Proper use of `ref.watch()` for reactive state
- [ ] Proper use of `ref.read()` for actions

**For SingleTaskState pages**:
- [ ] Inherits `SingleTaskState<T>`
- [ ] Implements `onVisibleChange(bool isVisible)`
- [ ] Implements `onRefresh()`
- [ ] Implements `buildContent(BuildContext context)`
- [ ] Properly disposes timers and controllers
- [ ] Uses `addTask()` for async operations

**For CacheableState pages**:
- [ ] Inherits `CacheableState<T, R>`
- [ ] Implements `getCacheableRequest()`
- [ ] Properly clears transient search fields after cache load
- [ ] Disposes `PaginatorController` if used
- [ ] Uses `addTask()` and `cancelAllTask()` correctly

### Riverpod Pattern Review

**ref.watch vs ref.read**:
- `ref.watch()` - Used for reading state that triggers rebuilds
- `ref.watch(notifier.select())` - Optimized with select for specific fields
- `ref.read()` - Used for one-time reads or calling methods
- `ref.read(notifier.notifier)` - Used for accessing StateNotifier methods

**Common mistakes to flag**:
- Using `ref.read()` in build method for reactive state
- Not using `select()` for performance optimization
- Calling `ref.watch()` inside event handlers

### Security Review

**OAuth2 and Authentication**:
- [ ] Uses TaskManager for OAuth operations
- [ ] Tokens stored securely (FlutterSecureStorage)
- [ ] No sensitive data in logs or URLs
- [ ] Proper token refresh handling via interceptors

**API Security**:
- [ ] HTTPS endpoints only
- [ ] Input validation for user data
- [ ] No hardcoded secrets or credentials
- [ ] Proper error handling without exposing internals

### Code Quality Review

**Performance**:
- [ ] No unnecessary rebuilds
- [ ] ListView.builder for long lists
- [ ] const widgets where possible
- [ ] Avoid complex computations in build methods

**Maintainability**:
- [ ] Clear naming conventions
- [ ] Proper code organization
- [ ] Adequate comments for complex logic
- [ ] No duplicated code

**Style**:
- [ ] Consistent formatting (dart format)
- [ ] No magic numbers or hardcoded strings
- [ ] Uses project constants (SLColor, kPagePadding)
- [ ] Follows Dart style guide

## Resources

### Review Checklist

See [references/review-checklist.md](references/review-checklist.md) for a comprehensive checklist covering:
- State management architecture
- Riverpod usage patterns
- Lifecycle management
- TaskManager and OAuth2
- UI architecture
- Code quality standards
- Security considerations
- Project-specific compliance

Use this checklist as the basis for the code-reviewer subagent's analysis.

## Usage Examples

**Example 1: Review after completing a feature**

User: "I just finished implementing the order stats page, can you review it?"

```
1. Check git status to see modified files
2. Identify the State type (likely SingleTaskState for dashboard)
3. Invoke code-reviewer subagent with file list and focus areas
4. Process results and categorize findings
5. Present formatted review with actionable recommendations
```

**Example 2: Pre-commit review**

User: "/review"

```
1. Run git diff to see all staged changes
2. Determine review scope based on file types
3. Invoke code-reviewer subagent with complete context
4. Generate compliance report
5. Highlight critical issues before commit
```

**Example 3: Review specific files**

User: "Review the changes in group_account_change_log_page.dart"

```
1. Read the specified file
2. Check if it's a page (State type) or other component
3. Invoke code-reviewer subagent with targeted focus
4. Provide detailed analysis of that specific file
5. Compare against architecture standards
```

## Integration with Project Architecture

This skill is specifically designed for the B2B Manager Flutter Web project and integrates with:

- **CLAUDE.md** - Project rules and architecture overview
- **docs/widget/STATE_MANAGEMENT_GUIDE.md** - State type selection guide
- **docs/widget/architecture/\*.md** - Architecture standards for each State type
- **code-reviewer subagent** - Deep analysis and pattern detection

Always reference these documents when conducting reviews to ensure consistency with project standards.
