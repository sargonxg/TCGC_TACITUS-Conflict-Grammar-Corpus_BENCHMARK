# Pull Request

## Linked issue

Closes #

## Checklist

- [ ] Linked issue is referenced above
- [ ] Tests added or updated for changed code
- [ ] Docs updated if public API or behavior changed
- [ ] `tcgc validate items/v0.1-sample/` exits 0
- [ ] `pytest -q --cov=tcgc --cov-fail-under=90` green
- [ ] `ruff check .` and `ruff format --check .` clean
- [ ] `mypy --strict tcgc` clean
- [ ] `mkdocs build --strict` clean (if docs changed)

## Summary of changes

## Notes for reviewer
