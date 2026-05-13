# TCGC — common developer workflows.
# Use `make help` to see everything.

PY ?= python
RUN_ID ?= $(shell date -u +%Y%m%dT%H%M%SZ)
ITEMS ?= items
MODEL_ANTHROPIC ?= claude-opus-4-7
MODEL_OPENAI    ?= gpt-5

.PHONY: help install validate test typecheck lint format docs \
        experiment-dry experiment-anthropic experiment-openai experiment-report \
        clean

help:
	@echo "TCGC — common workflows"
	@echo ""
	@echo "  make install                    # pip install -e '.[dev,experiments]'"
	@echo "  make validate                   # tcgc validate items/"
	@echo "  make test                       # pytest -q with coverage"
	@echo "  make typecheck                  # mypy --strict tcgc"
	@echo "  make lint                       # ruff check + format"
	@echo "  make docs                       # mkdocs build --strict"
	@echo ""
	@echo "  Experiments — vanilla vs typed comparisons"
	@echo "  -------------------------------------------------"
	@echo "  make experiment-dry             # echo client (no API). ITEMS=items/v0.2-public-domain/"
	@echo "  make experiment-anthropic       # real run with Anthropic. needs ANTHROPIC_API_KEY"
	@echo "  make experiment-openai          # real run with OpenAI.    needs OPENAI_API_KEY"
	@echo "  make experiment-report RUN=runs/<id>   # produce REPORT.md from a run dir"
	@echo ""
	@echo "Overridable variables: RUN_ID, ITEMS, MODEL_ANTHROPIC, MODEL_OPENAI."

install:
	pip install -e '.[dev,experiments]'

validate:
	tcgc validate $(ITEMS)

test:
	pytest -q --cov=tcgc --cov-report=term-missing

typecheck:
	mypy --strict tcgc

lint:
	ruff check .
	ruff format --check .

format:
	ruff format .

docs:
	mkdocs build --strict

experiment-dry:
	$(PY) -m experiments.llm_vs_typed.orchestrate \
		--client echo \
		--items $(ITEMS) \
		--out-dir runs/echo-$(RUN_ID)
	@echo "Dry run complete. To produce the report:"
	@echo "  make experiment-report RUN=runs/echo-$(RUN_ID)"

experiment-anthropic:
	@test -n "$$ANTHROPIC_API_KEY" || (echo "ERROR: ANTHROPIC_API_KEY is not set." && exit 1)
	$(PY) -m experiments.llm_vs_typed.orchestrate \
		--client anthropic:$(MODEL_ANTHROPIC) \
		--items $(ITEMS) \
		--out-dir runs/anthropic-$(MODEL_ANTHROPIC)-$(RUN_ID)

experiment-openai:
	@test -n "$$OPENAI_API_KEY" || (echo "ERROR: OPENAI_API_KEY is not set." && exit 1)
	$(PY) -m experiments.llm_vs_typed.orchestrate \
		--client openai:$(MODEL_OPENAI) \
		--items $(ITEMS) \
		--out-dir runs/openai-$(MODEL_OPENAI)-$(RUN_ID)

experiment-report:
	@test -n "$(RUN)" || (echo "ERROR: pass RUN=runs/<id>." && exit 1)
	$(PY) -m experiments.llm_vs_typed.orchestrate --report $(RUN)

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage site/ build/ dist/ *.egg-info
