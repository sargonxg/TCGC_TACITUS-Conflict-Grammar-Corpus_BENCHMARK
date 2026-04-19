"""StrEnums and the canonical task_type -> metric map."""
from __future__ import annotations
from enum import StrEnum


class Domain(StrEnum):
    WORKPLACE = "workplace"
    COMMERCIAL = "commercial"
    GOVERNANCE = "governance"
    PEACE_PROCESS = "peace-process"
    POLICY = "policy"
    FAMILY = "family"
    DIPLOMATIC = "diplomatic"


class TaskType(StrEnum):
    ACTOR_RESOLUTION = "actor-resolution"
    CLAIM_EXTRACTION = "claim-extraction"
    INTEREST_EXTRACTION = "interest-extraction"
    CONSTRAINT_EXTRACTION = "constraint-extraction"
    LEVERAGE_MAPPING = "leverage-mapping"
    COMMITMENT_TRACKING = "commitment-tracking"
    EVENT_ORDERING = "event-ordering"
    NARRATIVE_DRIFT = "narrative-drift"
    CAUSAL_CHAIN = "causal-chain"
    CONTRADICTION_DETECTION = "contradiction-detection"
    PROVENANCE_ATTRIBUTION = "provenance-attribution"
    COMMITMENT_CLAIM_MISMATCH = "commitment-claim-mismatch"
    POSITION_INTEREST_SEPARATION = "position-interest-separation"
    CROSS_DOCUMENT_SYNTHESIS = "cross-document-synthesis"


class Metric(StrEnum):
    GRAPH_OVERLAP = "graph_overlap"
    PROVENANCE_F1 = "provenance_f1"
    KENDALL_TAU = "kendall_tau"
    CONTRADICTION_PAIR_F1 = "contradiction_pair_f1"
    LLM_JUDGE_ANCHORED = "llm_judge_anchored"


TASK_METRIC_MAP: dict[str, str] = {
    TaskType.ACTOR_RESOLUTION:             Metric.GRAPH_OVERLAP,
    TaskType.CLAIM_EXTRACTION:             Metric.GRAPH_OVERLAP,
    TaskType.INTEREST_EXTRACTION:          Metric.LLM_JUDGE_ANCHORED,
    TaskType.CONSTRAINT_EXTRACTION:        Metric.GRAPH_OVERLAP,
    TaskType.LEVERAGE_MAPPING:             Metric.GRAPH_OVERLAP,
    TaskType.COMMITMENT_TRACKING:          Metric.GRAPH_OVERLAP,
    TaskType.EVENT_ORDERING:               Metric.KENDALL_TAU,
    TaskType.NARRATIVE_DRIFT:              Metric.LLM_JUDGE_ANCHORED,
    TaskType.CAUSAL_CHAIN:                 Metric.GRAPH_OVERLAP,
    TaskType.CONTRADICTION_DETECTION:      Metric.CONTRADICTION_PAIR_F1,
    TaskType.PROVENANCE_ATTRIBUTION:       Metric.PROVENANCE_F1,
    TaskType.COMMITMENT_CLAIM_MISMATCH:    Metric.GRAPH_OVERLAP,
    TaskType.POSITION_INTEREST_SEPARATION: Metric.LLM_JUDGE_ANCHORED,
    TaskType.CROSS_DOCUMENT_SYNTHESIS:     Metric.GRAPH_OVERLAP,
}
