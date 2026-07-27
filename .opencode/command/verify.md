# /verify — проверка качества кода

Checks code quality before commit/commit.

## Usage

```
/verify              → auto-detect language
/verify python       → run Python checks
/verify js           → run JS/TS checks
/verify --fast       → fast mode (ruff only)
```

## What it does

1. Detects project language
2. Runs relevant checks (ruff, mypy, eslint, tsc)
3. Reports summary
4. Blocks if any check fails

## Examples

```
/verify
→ [ruff] ✓
→ [mypy] ✓
✓ All checks passed
```

```
/verify python
→ [ruff] ✗
→ [mypy] ✓
❌ 1 check failed
```

## Integration

- Runs automatically before `/finish-task`
- Can be called manually before any commit
- Uses `scripts/verify.ps1`