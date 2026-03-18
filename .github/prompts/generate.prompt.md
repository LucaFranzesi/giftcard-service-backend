````prompt
---
agent: Generating Agent
description: Generate implementation documentation from a development plan
---

Generate complete, copy-paste ready implementation documentation from an existing development plan.

## Goal
Transform a `plan.md` into a detailed `implementation.md` with complete code blocks ready for copy-paste. DO NOT directly edit files - only generate documentation.

## Workflow

### Step 1: Parse Plan & Research
1. Read `plans/{feature-name}/plan.md`
2. Extract feature name, branch, and all implementation steps
3. Research the codebase comprehensively:
   - Project structure and conventions
   - Existing code patterns in affected files
   - Import conventions and dependencies
   - Error handling patterns

### Step 2: Generate Implementation Document
Create `plans/{feature-name}/implementation.md` with:
- Complete, copy-paste ready code (NO placeholders, NO TODOs)
- Exact file paths
- Markdown checkboxes for every action
- Verification checklists for each step
- STOP & COMMIT points between steps

## Output Structure

```markdown
# {Feature Name}

## Goal
{What this implementation accomplishes}

## Prerequisites
Ensure you are on the `{branch-name}` branch before beginning.

### Step-by-Step Instructions

#### Step 1: {Action}
- [ ] {Instruction}
- [ ] Copy and paste into `{file}`:

\`\`\`python
{COMPLETE CODE - NO PLACEHOLDERS}
\`\`\`

##### Step 1 Verification
- [ ] No build errors
- [ ] {Specific test to verify}

#### Step 1 STOP & COMMIT
**STOP & COMMIT:** Test, stage, and await for user confirmation for commit before continuing.

#### Step 2: {Action}
...
```

## User Request
Generate implementation for: {{{ input }}}

````