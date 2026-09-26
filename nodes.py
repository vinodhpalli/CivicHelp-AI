# app/agents/nodes.py

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

CHUNKS_FILE = (
    PROCESSED_DIR / "telangana_chunks.json"
)


# ============================================================
# SERVICE IMPORTS
# ============================================================

from app.services.query_understanding import (
    QueryUnderstanding,
)

from app.services.query_router import (
    QueryRouter,
)

from app.services.query_planner import (
    QueryPlanner,
)

from app.services.scheme_detector import (
    SchemeDetector,
)

from app.services.profile_extractor import (
    ProfileExtractor,
)

from app.services.eligibility_engine import (
    EligibilityEngine,
)

from app.services.answer_generator import (
    AnswerGenerator,
)

from app.services.citation_builder import (
    CitationBuilder,
)

from app.services.scheme_discovery import (
    SchemeDiscovery,
)

from app.services.discovery_evidence import (
    DiscoveryEvidenceService,
)

from app.services.evidence_validator import (
    EvidenceValidator,
)

from app.rag.rag_retriever import (
    RAGRetriever,
)


# ============================================================
# SERVICE INITIALIZATION
# ============================================================

print(
    "Initializing CivicHelp AI Nodes..."
)


# ------------------------------------------------------------
# Query services
# ------------------------------------------------------------

query_understanding = (
    QueryUnderstanding()
)

query_router = QueryRouter()

query_planner = QueryPlanner()


# ------------------------------------------------------------
# Scheme services
# ------------------------------------------------------------

scheme_detector = SchemeDetector()

scheme_discovery = SchemeDiscovery()


# ------------------------------------------------------------
# Profile / eligibility
# ------------------------------------------------------------

profile_extractor = ProfileExtractor()

eligibility_engine = EligibilityEngine()


# ------------------------------------------------------------
# RAG / evidence
# ------------------------------------------------------------

def _load_chunks() -> list[dict[str, Any]]:
    """
    Load processed chunks used by the RAG retriever.
    """

    if not CHUNKS_FILE.exists():

        raise FileNotFoundError(
            f"Chunks file not found: "
            f"{CHUNKS_FILE}"
        )

    with open(
        CHUNKS_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        chunks = json.load(file)

    if not isinstance(
        chunks,
        list,
    ):

        raise ValueError(
            "telangana_chunks.json "
            "must contain a list."
        )

    print(
        f"[INFO] Loaded "
        f"{len(chunks)} chunks"
    )

    return chunks


chunks = _load_chunks()


print(
    "\nInitializing Hybrid Retriever..."
)

rag_retriever = RAGRetriever(
    chunks
)


# ------------------------------------------------------------
# Other services
# ------------------------------------------------------------

citation_builder = CitationBuilder()

answer_generator = AnswerGenerator()

discovery_evidence_service = (
    DiscoveryEvidenceService()
)

evidence_validator = EvidenceValidator()


# ============================================================
# HELPER
# ============================================================

def get_field(
    obj: Any,
    field_name: str,
    default: Any = None,
) -> Any:
    """
    Safely read a field from:
    - dictionary
    - dataclass
    - normal object
    """

    if obj is None:
        return default

    if isinstance(
        obj,
        dict,
    ):

        return obj.get(
            field_name,
            default,
        )

    return getattr(
        obj,
        field_name,
        default,
    )


# ============================================================
# 1. QUERY UNDERSTANDING
# ============================================================

def understand_query(
    state: dict[str, Any],
) -> dict[str, Any]:

    query = state.get(
        "query",
        "",
    )

    if not isinstance(
        query,
        str,
    ):

        query = str(query)

    query = query.strip()

    if not query:

        return {
            **state,
            "query_context": None,
            "status": "INVALID_QUERY",
            "message": (
                "Query cannot be empty."
            ),
        }

    print(
        "\n[QUERY UNDERSTANDING]"
    )

    context = (
        query_understanding.understand(
            query
        )
    )

    print(
        f"Intent: "
        f"{get_field(context, 'intent')}"
    )

    print(
        f"State: "
        f"{get_field(context, 'state')}"
    )

    print(
        f"Category: "
        f"{get_field(context, 'category')}"
    )

    print(
        f"Age: "
        f"{get_field(context, 'age')}"
    )

    return {
        **state,
        "query_context": context,
        "status": "QUERY_UNDERSTOOD",
    }


# ============================================================
# 2. QUERY ROUTER
# ============================================================

def route_query(
    state: dict[str, Any],
) -> dict[str, Any]:

    query = state.get(
        "query",
        "",
    )

    if not isinstance(
        query,
        str,
    ):

        query = str(query)

    query = query.strip()

    if not query:

        return {
            **state,
            "query_route": None,
            "status": "INVALID_QUERY",
            "message": (
                "Query cannot be empty."
            ),
        }

    print(
        "\n[QUERY ROUTER]"
    )

    route = query_router.route(
        query
    )

    print(
        f"Intent: "
        f"{get_field(route, 'intent')}"
    )

    print(
        f"Confidence: "
        f"{get_field(route, 'confidence')}"
    )

    return {
        **state,
        "query_route": route,
        "status": "QUERY_ROUTED",
    }


# ============================================================
# 3. QUERY PLANNER
# ============================================================

def plan_query(
    state: dict[str, Any],
) -> dict[str, Any]:

    context = state.get(
        "query_context"
    )

    query = state.get(
        "query",
        "",
    )

    if context is None:

        return {
            **state,
            "query_plan": None,
            "status": "QUERY_PLAN_FAILED",
        }

    print(
        "\n[QUERY PLANNER]"
    )

    plan = query_planner.plan(
        context
    )

    print(
        f"Intent: "
        f"{get_field(plan, 'intent')}"
    )

    print(
        f"State: "
        f"{get_field(plan, 'state')}"
    )

    print(
        f"Category: "
        f"{get_field(plan, 'category')}"
    )

    print(
        f"Filters: "
        f"{get_field(plan, 'filters')}"
    )

    print(
        f"Retrieval Queries: "
        f"{get_field(plan, 'retrieval_queries')}"
    )

    return {
        **state,
        "query_plan": plan,
        "status": "QUERY_PLANNED",
    }


# ============================================================
# 4. SCHEME DETECTOR
# ============================================================

def detect_scheme(
    state: dict[str, Any],
) -> dict[str, Any]:

    query = state.get(
        "query",
        "",
    )

    if not isinstance(
        query,
        str,
    ):

        query = str(query)

    query = query.strip()

    if not query:

        return {
            **state,
            "scheme": None,
            "status": (
                "SCHEME_NOT_IDENTIFIED"
            ),
        }

    print(
        "\n[SCHEME DETECTOR]"
    )

    scheme = scheme_detector.detect(
        query
    )

    if scheme is None:

        print(
            "No specific scheme identified."
        )

        return {
            **state,
            "scheme": None,
            "status": (
                "SCHEME_NOT_IDENTIFIED"
            ),
        }

    print(
        f"Scheme ID: "
        f"{get_field(scheme, 'scheme_id')}"
    )

    print(
        f"Scheme Name: "
        f"{get_field(scheme, 'scheme_name')}"
    )

    return {
        **state,
        "scheme": scheme,
        "status": "SCHEME_IDENTIFIED",
    }


# ============================================================
# 5. PROFILE EXTRACTION
# ============================================================

def extract_profile(
    state: dict[str, Any],
) -> dict[str, Any]:

    query = state.get(
        "query",
        "",
    )

    if not isinstance(
        query,
        str,
    ):

        query = str(query)

    query = query.strip()

    print(
        "\n[PROFILE EXTRACTOR]"
    )

    profile = (
        profile_extractor.extract(
            query
        )
    )

    print(
        f"Age: "
        f"{get_field(profile, 'age')}"
    )

    print(
        f"State: "
        f"{get_field(profile, 'state')}"
    )

    print(
        f"District: "
        f"{get_field(profile, 'district')}"
    )

    return {
        **state,
        "profile": profile,
        "status": "PROFILE_EXTRACTED",
    }


# ============================================================
# 6. NORMAL RAG RETRIEVAL
# ============================================================

def retrieve_evidence(
    state: dict[str, Any],
) -> dict[str, Any]:

    query = state.get(
        "query",
        "",
    )

    if not isinstance(
        query,
        str,
    ):

        query = str(query)

    query = query.strip()

    scheme = state.get(
        "scheme"
    )

    query_plan = state.get(
        "query_plan"
    )

    # --------------------------------------------------------
    # Determine filters
    # --------------------------------------------------------

    scheme_state = get_field(
        scheme,
        "state",
    )

    category = get_field(
        scheme,
        "category",
    )

    filters = get_field(
        query_plan,
        "filters",
        {},
    )

    if isinstance(
        filters,
        dict,
    ):

        scheme_state = (
            filters.get(
                "state"
            )
            or scheme_state
        )

        category = (
            filters.get(
                "category"
            )
            or category
        )

    # --------------------------------------------------------
    # Retrieve
    # --------------------------------------------------------

    print(
        "\n[RAG RETRIEVER]"
    )

    try:

        evidence = (
            rag_retriever.retrieve(
                query=query,
                top_k=5,
                state=scheme_state,
                category=category,
            )
        )

    except TypeError:

        evidence = (
            rag_retriever.retrieve(
                query=query,
                top_k=5,
            )
        )

    if evidence is None:
        evidence = []

    print(
        f"Retrieved "
        f"{len(evidence)} chunks."
    )

    # --------------------------------------------------------
    # Do NOT blindly filter evidence by scheme ID.
    #
    # A scheme can have multiple supporting
    # documents.
    # --------------------------------------------------------

    return {
        **state,
        "evidence": evidence,
        "status": (
            "EVIDENCE_RETRIEVED"
            if evidence
            else "NO_EVIDENCE_FOUND"
        ),
    }


# ============================================================
# 7. SCHEME DISCOVERY
# ============================================================

def discover_schemes(
    state: dict[str, Any],
) -> dict[str, Any]:

    query = state.get(
        "query",
        "",
    )

    if not isinstance(
        query,
        str,
    ):

        query = str(query)

    query = query.strip()

    if not query:

        return {
            **state,
            "discovery_results": [],
            "status": "NO_SCHEMES_FOUND",
            "message": (
                "Query cannot be empty."
            ),
        }

    print(
        "\n[SCHEME DISCOVERY]"
    )

    results = (
        scheme_discovery.discover(
            query=query,
            top_k=5,
        )
    )

    if results is None:
        results = []

    print(
        f"Found {len(results)} schemes."
    )

    for result in results:

        print(
            "  - "
            f"{result.get('scheme_id')} | "
            f"{result.get('scheme_name')} | "
            f"score={result.get('score')}"
        )

    if not results:

        return {
            **state,
            "discovery_results": [],
            "status": "NO_SCHEMES_FOUND",
            "message": (
                "No schemes were found in "
                "the currently indexed "
                "government sources."
            ),
        }

    return {
        **state,
        "discovery_results": results,
        "status": "SCHEMES_DISCOVERED",
    }


# ============================================================
# 8. DISCOVERY EVIDENCE
# ============================================================

def retrieve_discovery_evidence(
    state: dict[str, Any],
) -> dict[str, Any]:

    schemes = (
        state.get(
            "discovery_results"
        )
        or []
    )

    query = state.get(
        "query",
        "",
    )

    if not schemes:

        return {
            **state,
            "discovery_evidence": [],
            "status": (
                "DISCOVERY_EVIDENCE_NOT_FOUND"
            ),
        }

    print(
        "\n[DISCOVERY EVIDENCE]"
    )

    discovery_evidence = (
        discovery_evidence_service.build(
            discovered_schemes=schemes,
            query=query,
            max_chunks_per_document=2,
        )
    )

    if discovery_evidence is None:

        discovery_evidence = []

    accepted = 0

    for scheme in discovery_evidence:

        accepted += len(
            scheme.get(
                "evidence",
                [],
            )
        )

    print(
        f"Discovery schemes: "
        f"{len(discovery_evidence)}"
    )

    print(
        f"Accepted evidence chunks: "
        f"{accepted}"
    )

    return {
        **state,
        "discovery_evidence": (
            discovery_evidence
        ),
        "status": (
            "DISCOVERY_EVIDENCE_FOUND"
            if discovery_evidence
            else "DISCOVERY_EVIDENCE_NOT_FOUND"
        ),
    }


# ============================================================
# 9. ELIGIBILITY ENGINE
# ============================================================

def evaluate_eligibility(
    state: dict[str, Any],
) -> dict[str, Any]:

    scheme = state.get(
        "scheme"
    )

    profile = state.get(
        "profile"
    )

    if scheme is None:

        return {
            **state,
            "eligibility": None,
            "status": (
                "ELIGIBILITY_NOT_EVALUATED"
            ),
        }

    if profile is None:

        return {
            **state,
            "eligibility": None,
            "status": (
                "ELIGIBILITY_NEEDS_INFORMATION"
            ),
        }

    scheme_id = get_field(
        scheme,
        "scheme_id",
    )

    if not scheme_id:

        return {
            **state,
            "eligibility": None,
            "status": (
                "ELIGIBILITY_NOT_EVALUATED"
            ),
        }

    print(
        "\n[ELIGIBILITY ENGINE]"
    )

    print(
        f"Evaluating: "
        f"{scheme_id}"
    )

    eligibility = (
        eligibility_engine.evaluate(
            scheme_id=scheme_id,
            profile=profile,
        )
    )

    print(
        f"Result: "
        f"{get_field(eligibility, 'status')}"
    )

    return {
        **state,
        "eligibility": eligibility,
        "status": "ELIGIBILITY_EVALUATED",
    }


# ============================================================
# 10. EVIDENCE VALIDATION
# ============================================================

def validate_evidence(
    state: dict[str, Any],
) -> dict[str, Any]:

    query = state.get(
        "query",
        "",
    )

    if not isinstance(
        query,
        str,
    ):

        query = str(query)

    query = query.strip()

    query_context = state.get(
        "query_context"
    )

    # --------------------------------------------------------
    # Get intent
    # --------------------------------------------------------

    intent = get_field(
        query_context,
        "intent",
    )

    if hasattr(
        intent,
        "value",
    ):

        intent = intent.value

    intent = (
        str(intent).upper().strip()
        if intent
        else ""
    )

    evidence = (
        state.get("evidence")
        or []
    )

    discovery_results = (
        state.get(
            "discovery_results"
        )
        or []
    )

    discovery_evidence = (
        state.get(
            "discovery_evidence"
        )
        or []
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "[EVIDENCE VALIDATION]"
    )

    print(
        "=" * 70
    )

    print(
        f"Query: {query}"
    )

    print(
        f"Intent: {intent}"
    )

    print(
        f"Normal Evidence: "
        f"{len(evidence)}"
    )

    print(
        f"Discovery Results: "
        f"{len(discovery_results)}"
    )

    print(
        f"Discovery Evidence: "
        f"{len(discovery_evidence)}"
    )

    # ========================================================
    # DISCOVERY VALIDATION
    # ========================================================

    if (
        intent == "SCHEME_DISCOVERY"
        or discovery_results
        or discovery_evidence
    ):

        print(
            "[VALIDATION] "
            "Discovery query detected."
        )

        # ----------------------------------------------------
        # Validate scheme results
        # ----------------------------------------------------

        valid_discovery_results = []

        for scheme in discovery_results:

            if not isinstance(
                scheme,
                dict,
            ):
                continue

            scheme_id = scheme.get(
                "scheme_id"
            )

            scheme_name = scheme.get(
                "scheme_name"
            )

            if (
                scheme_id
                and scheme_name
            ):

                valid_discovery_results.append(
                    scheme
                )

        # ----------------------------------------------------
        # Validate discovery evidence
        # ----------------------------------------------------

        valid_discovery_evidence = []

        for scheme in discovery_evidence:

            if not isinstance(
                scheme,
                dict,
            ):
                continue

            scheme_id = scheme.get(
                "scheme_id"
            )

            scheme_name = scheme.get(
                "scheme_name"
            )

            scheme_chunks = (
                scheme.get(
                    "evidence"
                )
                or []
            )

            evidence_status = (
                scheme.get(
                    "evidence_status"
                )
            )

            if (
                scheme_id
                and scheme_name
                and scheme_chunks
                and evidence_status == "VALID"
            ):

                valid_discovery_evidence.append(
                    scheme
                )

        # ----------------------------------------------------
        # Flatten evidence
        # ----------------------------------------------------

        discovery_flat_evidence = []

        for scheme in (
            valid_discovery_evidence
        ):

            scheme_chunks = (
                scheme.get(
                    "evidence"
                )
                or []
            )

            for chunk in scheme_chunks:

                if isinstance(
                    chunk,
                    dict,
                ):

                    discovery_flat_evidence.append(
                        chunk
                    )

        # ----------------------------------------------------
        # Build citations
        # ----------------------------------------------------

        discovery_citations = []

        if discovery_flat_evidence:

            try:

                discovery_citations = (
                    citation_builder.build_citations(
                        discovery_flat_evidence
                    )
                )

            except Exception as exc:

                print(
                    "[WARNING] Discovery "
                    "citation building failed:",
                    exc,
                )

        # ----------------------------------------------------
        # Determine support
        # ----------------------------------------------------

        has_discovery_results = (
            len(
                valid_discovery_results
            ) > 0
        )

        has_discovery_evidence = (
            len(
                valid_discovery_evidence
            ) > 0
        )

        answer_supported = (
            has_discovery_results
            and has_discovery_evidence
        )

        if answer_supported:

            query_support_score = 1.0

        elif has_discovery_results:

            query_support_score = 0.70

        else:

            query_support_score = 0.0

        validation_status = (
            "VERIFIED"
            if answer_supported
            else "UNVERIFIED"
        )

        validation = {

            "status":
                validation_status,

            "answer_supported":
                answer_supported,

            "query_support_score":
                query_support_score,

            "intent":
                intent,

            "discovery_results_count":
                len(
                    valid_discovery_results
                ),

            "discovery_evidence_count":
                len(
                    valid_discovery_evidence
                ),

            "verified_citations":
                discovery_citations,

            "validation_type":
                "DISCOVERY",
        }

        print(
            f"Answer Supported: "
            f"{answer_supported}"
        )

        print(
            f"Query Support Score: "
            f"{query_support_score}"
        )

        print(
            f"Evidence Status: "
            f"{validation_status}"
        )

        print(
            f"Verified Citations: "
            f"{len(discovery_citations)}"
        )

        print(
            "=" * 70
        )

        return {
            **state,
            "evidence_validation":
                validation,
            "citations":
                discovery_citations,
            "status":
                (
                    "EVIDENCE_VERIFIED"
                    if answer_supported
                    else "EVIDENCE_UNVERIFIED"
                ),
        }

    # ========================================================
    # NORMAL RAG VALIDATION
    # ========================================================

    print(
        "[VALIDATION] "
        "Normal RAG query detected."
    )

    if not evidence:

        validation = {
            "status": "UNKNOWN",
            "answer_supported": False,
            "query_support_score": 0.0,
            "relevant_evidence": [],
            "verified_citations": [],
        }

        return {
            **state,
            "evidence_validation":
                validation,
            "citations": [],
            "status":
                "EVIDENCE_UNVERIFIED",
        }

    scheme = state.get(
        "scheme"
    )

    scheme_id = get_field(
        scheme,
        "scheme_id",
    )

    # --------------------------------------------------------
    # Run EvidenceValidator
    # --------------------------------------------------------

    try:

        validation = (
            evidence_validator.validate(
                query=query,
                evidence=evidence,
                scheme_id=scheme_id,
            )
        )

    except TypeError:

        try:

            validation = (
                evidence_validator.validate(
                    query=query,
                    evidence=evidence,
                )
            )

        except TypeError:

            validation = (
                evidence_validator.validate(
                    query=query,
                    evidence=evidence,
                    citations=[],
                )
            )

    except Exception as exc:

        print(
            "[ERROR] Evidence validation failed:",
            exc,
        )

        validation = {
            "status": "UNVERIFIED",
            "answer_supported": False,
            "query_support_score": 0.0,
            "relevant_evidence": [],
            "verified_citations": [],
        }

    if validation is None:

        validation = {
            "status": "UNKNOWN",
            "answer_supported": False,
            "query_support_score": 0.0,
            "relevant_evidence": [],
            "verified_citations": [],
        }

    # --------------------------------------------------------
    # Build citations
    # --------------------------------------------------------

    relevant_evidence = (
        validation.get(
            "relevant_evidence",
            [],
        )
        or []
    )

    citation_evidence = []

    if relevant_evidence:

        citation_evidence = (
            relevant_evidence
        )

    else:

        citation_evidence = evidence

    try:

        citations = (
            citation_builder.build_citations(
                citation_evidence
            )
        )

    except Exception as exc:

        print(
            "[WARNING] Citation building failed:",
            exc,
        )

        citations = []

    answer_supported = bool(
        validation.get(
            "answer_supported",
            False,
        )
        and citations
    )

    query_support_score = float(
        validation.get(
            "query_support_score",
            0.0,
        )
        or 0.0
    )

    validation["answer_supported"] = (
        answer_supported
    )

    validation["query_support_score"] = (
        query_support_score
    )

    validation["verified_citations"] = (
        citations
    )

    validation["status"] = (
        "VERIFIED"
        if answer_supported
        else "UNVERIFIED"
    )

    print(
        f"Answer Supported: "
        f"{answer_supported}"
    )

    print(
        f"Query Support Score: "
        f"{query_support_score}"
    )

    print(
        f"Evidence Status: "
        f"{validation['status']}"
    )

    print(
        f"Verified Citations: "
        f"{len(citations)}"
    )

    print(
        "=" * 70
    )

    return {
        **state,
        "evidence_validation":
            validation,
        "citations":
            citations,
        "status":
            (
                "EVIDENCE_VERIFIED"
                if answer_supported
                else "EVIDENCE_UNVERIFIED"
            ),
    }


# ============================================================
# 11. ANSWER GENERATION
# ============================================================

def generate_answer(
    state: dict[str, Any],
) -> dict[str, Any]:

    print(
        "\n[ANSWER GENERATION]"
    )

    query = state.get(
        "query",
        "",
    )

    if not isinstance(
        query,
        str,
    ):

        query = str(query)

    query = query.strip()

    if not query:

        return {
            **state,
            "answer": "Query is empty.",
            "status": "ERROR",
        }

    evidence = (
        state.get("evidence")
        or []
    )

    citations = (
        state.get("citations")
        or []
    )

    eligibility = state.get(
        "eligibility"
    )

    discovery_results = (
        state.get(
            "discovery_results"
        )
        or []
    )

    discovery_evidence = (
        state.get(
            "discovery_evidence"
        )
        or []
    )

    query_route = state.get(
        "query_route"
    )

    evidence_validation = (
        state.get(
            "evidence_validation"
        )
        or {}
    )

    print(
        f"Normal Evidence: "
        f"{len(evidence)}"
    )

    print(
        f"Discovery Results: "
        f"{len(discovery_results)}"
    )

    print(
        f"Discovery Evidence: "
        f"{len(discovery_evidence)}"
    )

    print(
        f"Citations: "
        f"{len(citations)}"
    )

    # --------------------------------------------------------
    # IMPORTANT
    #
    # Never do:
    #
    # answer_generator.generate(state)
    #
    # --------------------------------------------------------

    try:

        answer = (
            answer_generator.generate(
                query=query,
                evidence=evidence,
                citations=citations,
                eligibility=eligibility,
                discovery_results=(
                    discovery_results
                ),
                discovery_evidence=(
                    discovery_evidence
                ),
                query_route=query_route,
                evidence_validation=(
                    evidence_validation
                ),
            )
        )

    except Exception as exc:

        print(
            "[ERROR] Answer generation failed:",
            exc,
        )

        return {
            **state,
            "answer": (
                "I was unable to generate "
                "an answer from the available "
                "government evidence."
            ),
            "status": "ANSWER_GENERATION_ERROR",
            "answer_error": str(exc),
        }

    return {
        **state,
        "answer": answer,
        "status": "ANSWER_GENERATED",
    }


# ============================================================
# 12. BUILD CITATIONS
# ============================================================

def build_citations(
    state: dict[str, Any],
) -> dict[str, Any]:

    print(
        "\n[CITATION BUILDING]"
    )

    existing_citations = (
        state.get(
            "citations"
        )
        or []
    )

    evidence = (
        state.get(
            "evidence"
        )
        or []
    )

    discovery_evidence = (
        state.get(
            "discovery_evidence"
        )
        or []
    )

    all_evidence = []

    # --------------------------------------------------------
    # Normal RAG evidence
    # --------------------------------------------------------

    for item in evidence:

        if isinstance(
            item,
            dict,
        ):

            all_evidence.append(
                item
            )

    # --------------------------------------------------------
    # Discovery evidence
    # --------------------------------------------------------

    for scheme in discovery_evidence:

        if not isinstance(
            scheme,
            dict,
        ):
            continue

        chunks_for_scheme = (
            scheme.get(
                "evidence"
            )
            or []
        )

        for chunk in chunks_for_scheme:

            if isinstance(
                chunk,
                dict,
            ):

                all_evidence.append(
                    chunk
                )

    # --------------------------------------------------------
    # Build citations
    # --------------------------------------------------------

    generated_citations = []

    if all_evidence:

        try:

            generated_citations = (
                citation_builder.build_citations(
                    all_evidence
                )
            )

        except Exception as exc:

            print(
                "[WARNING] Citation builder failed:",
                exc,
            )

    # --------------------------------------------------------
    # Merge existing + generated
    # --------------------------------------------------------

    merged = []

    seen = set()

    for citation in (
        existing_citations
        + generated_citations
    ):

        if not isinstance(
            citation,
            dict,
        ):
            continue

        document_id = citation.get(
            "document_id"
        )

        chunk_id = citation.get(
            "chunk_id"
        )

        key = (
            document_id,
            chunk_id,
        )

        if key in seen:

            continue

        seen.add(key)

        merged.append(
            citation
        )

    print(
        f"Final citations: "
        f"{len(merged)}"
    )

    return {
        **state,
        "citations": merged,
    }


# ============================================================
# 13. BUILD FINAL RESPONSE
# ============================================================

def build_response(
    state: dict[str, Any],
) -> dict[str, Any]:

    answer = state.get(
        "answer",
        "",
    )

    citations = (
        state.get(
            "citations"
        )
        or []
    )

    scheme = state.get(
        "scheme"
    )

    eligibility = state.get(
        "eligibility"
    )

    query_route = state.get(
        "query_route"
    )

    evidence_validation = (
        state.get(
            "evidence_validation"
        )
        or {}
    )

    discovery_results = (
        state.get(
            "discovery_results"
        )
        or []
    )

    # --------------------------------------------------------
    # Scheme information
    # --------------------------------------------------------

    scheme_info = None

    if scheme:

        scheme_info = {
            "scheme_id": get_field(
                scheme,
                "scheme_id",
            ),

            "scheme_name": get_field(
                scheme,
                "scheme_name",
            ),

            "category": get_field(
                scheme,
                "category",
            ),

            "state": get_field(
                scheme,
                "state",
            ),
        }

    # --------------------------------------------------------
    # Final response
    # --------------------------------------------------------

    response = {

        "answer":
            answer,

        "citations":
            citations,

        "scheme":
            scheme_info,

        "eligibility":
            eligibility,

        "discovery_results":
            discovery_results,

        "evidence_validation":
            evidence_validation,

        "status":
            "COMPLETED",
    }

    # --------------------------------------------------------
    # Query route metadata
    # --------------------------------------------------------

    if query_route:

        response["intent"] = (
            get_field(
                query_route,
                "intent",
            )
        )

        response["confidence"] = (
            get_field(
                query_route,
                "confidence",
            )
        )

    return {
        **state,
        "response": response,
        "status": "COMPLETED",
    }