Execute the implementation plan by writing production-quality code incrementally, validating as you go.

## Behavior contract
- Require a plan document (from `@plan_tempalte_doc.md` or manually created) before implementing
- Implement only what the plan specifies; no scope creep or "improvements" unless explicitly requested
- Write production-ready code: typed, documented, tested, and following existing project conventions
- Work incrementally: implement, verify, commit conceptually before moving to the next component
- Surface blockers and unknowns immediately rather than making assumptions

## Prerequisites
1. A plan document exists (typically in `tasks/` directory)
2. You have read the relevant research document (if referenced in the plan)
3. You understand the existing codebase structure and conventions
4. Required dependencies are identified in the plan

## Implementation steps

### 1. Intake and validation
- Read the plan document fully
- Confirm you understand:
  - What needs to be built/changed
  - Which files/components are affected
  - Dependencies and integration points
  - Acceptance criteria
- If anything is unclear, ask before proceeding

### 2. Environment preparation
- Verify development environment is ready
- Check that required dependencies exist or can be added
- Ensure you can run existing tests
- Create feature branch if needed (follow project conventions)

### 3. Incremental implementation
Implement in this order to minimize risk:

**a) Core data structures and types first**
- Define interfaces, types, schemas, models
- Create foundational classes or modules
- Add comprehensive type hints/annotations
- Document public APIs with docstrings/comments

**b) Core business logic second**
- Implement the main functionality
- Keep functions focused and testable
- Handle edge cases identified in the plan
- Add inline comments for complex logic

**c) Integration points third**
- Wire up the new code to existing systems
- Handle data transformations at boundaries
- Add proper error handling and logging
- Validate inputs and outputs

**d) Configuration and deployment concerns last**
- Add/update configuration files
- Create or update database migrations
- Update environment variables documentation
- Add feature flags if specified in plan

### 4. Validation at each step
After each increment:
- Write unit tests for new code (or update existing tests)
- Run the test suite and fix failures
- Manually verify the behavior if applicable
- Check for type errors, linting issues
- Confirm no unintended side effects

### 5. Documentation
As you implement, maintain:
- Inline code comments for "why" (not "what")
- Docstrings for all public functions/classes/modules
- README updates if user-facing functionality changed
- Architecture notes if patterns changed

### 6. Pre-completion checklist
Before declaring implementation complete:
- [ ] All planned functionality implemented
- [ ] Tests written and passing
- [ ] No new linting/type errors introduced
- [ ] Error handling covers failure modes from plan
- [ ] Logging added at appropriate levels
- [ ] Configuration externalized (no hardcoded values)
- [ ] Documentation updated
- [ ] Security considerations addressed (input validation, secrets handling)
- [ ] Performance considerations addressed (if noted in plan)

## Code quality standards

### Follow existing conventions
- Match the indentation, naming, and style of the existing codebase
- Use the same patterns for error handling, logging, and testing
- Import and organize code the same way as similar files
- Maintain consistency in file/folder structure

### Write self-documenting code
```python
# Good: Clear names, types, and structure
def calculate_user_subscription_renewal_date(
    user_id: str,
    current_period_end: datetime,
    billing_interval: BillingInterval
) -> datetime:
    """Calculate when a user's subscription will renew.
    
    Args:
        user_id: Unique identifier for the user
        current_period_end: When the current billing period ends
        billing_interval: Monthly, yearly, etc.
        
    Returns:
        The datetime when the next billing cycle starts
        
    Raises:
        ValueError: If billing_interval is not supported
    """
    # Implementation here
    pass

# Bad: Unclear, untyped, undocumented
def calc(uid, cpe, bi):
    # does the thing
    pass
```

### Handle errors explicitly
- Anticipate failure modes identified in the plan
- Use appropriate error types (don't catch generic Exception unless necessary)
- Log errors with context before re-raising or handling
- Fail fast and loud in development; gracefully in production

### Make it testable
- Keep functions pure when possible (same inputs → same outputs)
- Inject dependencies rather than hardcoding them
- Expose test hooks when needed
- Write tests as you implement, not after

## Common patterns

### When adding a new feature
1. Create new module/file following project structure
2. Define public interface/API first
3. Implement core logic with tests
4. Integrate with existing code
5. Update configuration and docs

### When modifying existing code
1. Read and understand current implementation fully
2. Write tests for current behavior (if missing)
3. Make changes incrementally
4. Ensure tests still pass (or update them appropriately)
5. Look for other callsites that might be affected

### When refactoring
1. Ensure existing tests cover current behavior
2. Make behavior-preserving changes only
3. Run tests after each small change
4. Update documentation to match new structure
5. Note if further cleanup is needed but out of scope

## Handling blockers

### When you encounter unknowns
- **Stop implementing and ask** rather than guessing
- Document what you know vs. what you need to know
- Propose options if you have ideas, but don't decide unilaterally

### When the plan is incomplete or wrong
- Point out the gap or inconsistency clearly
- Reference specific sections of the plan
- Suggest updates to the plan before implementing
- Don't work around plan issues silently

### When requirements conflict
- Surface the conflict immediately
- Explain the trade-offs you see
- Wait for clarification before choosing a direction

## Output format

As you implement, provide progress updates:

```
## Implementation Progress

Completed:
✅ Core data models (`src/models/feature.py:1-145`)
✅ Business logic (`src/services/feature_service.py:1-230`)
✅ Unit tests (`tests/test_feature_service.py:1-180`)

In Progress:
🔨 Integration with existing API (`src/api/routes/feature.py`)

Remaining:
⏳ Database migration
⏳ Update configuration
⏳ Integration tests

Blockers/Questions:
❓ Should we add rate limiting here or handle at API gateway?
```

## Final deliverable

When implementation is complete:
1. All code committed to version control (or ready to be)
2. Tests written and passing
3. Documentation updated
4. Ready for code review (if applicable)
5. Ready for testing phase (`/test`)

## Anti-patterns to avoid
- ❌ Implementing without reading the plan
- ❌ Gold-plating: adding features not in the plan
- ❌ Skipping tests "to move faster"
- ❌ Copy-pasting code without understanding it
- ❌ Leaving TODOs or commented-out code in "final" implementation
- ❌ Hardcoding configuration values
- ❌ Ignoring existing conventions "because I prefer X"
- ❌ Making breaking changes without documenting them
- ❌ Proceeding when blocked instead of asking for help

## Notes
- Implementation is where the plan meets reality; finding gaps in the plan is normal and valuable
- Perfect code doesn't exist; production-ready code with known trade-offs is the goal
- When in doubt, bias toward simplicity and maintainability over cleverness
- Your code will be read more times than it's written; optimize for readability
