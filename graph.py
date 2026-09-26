# ============================================================
# CIVICHELP AI
# LANGGRAPH WORKFLOW
# ============================================================

from typing import Any, TypedDict

from langgraph.graph import StateGraph, START, END

from app.agents.nodes import (
    understand_query,
    plan_query,
    route_query,
    detect_scheme,
    extract_profile,
    retrieve_evidence,
    validate_evidence,
    evaluate_eligibility,
    build_citations,
    discover_schemes,
    retrieve_discovery_evidence,
    generate_answer,
    build_response,
)


# ============================================================
# GRAPH STATE
# ============================================================

class CivicHelpState(TypedDict, total=False):

    query: str

    query_context: Any
    query_plan: Any
    retrieval_queries: list[str]

    query_route: Any

    scheme: Any
    profile: Any

    evidence: list[dict[str, Any]]

    discovery_results: list[dict[str, Any]]
    discovery_evidence: list[dict[str, Any]]

    eligibility: Any

    evidence_validation: dict[str, Any]

    citations: list[dict[str, Any]]

    answer: str
    response: Any

    status: str
    message: str


# ============================================================
# GET INTENT
# ============================================================

def get_intent(state: CivicHelpState) -> str:

    query_context = state.get(
        "query_context"
    )

    if query_context is None:
        return ""

    intent = getattr(
        query_context,
        "intent",
        None,
    )

    if (
        intent is None
        and isinstance(
            query_context,
            dict,
        )
    ):
        intent = query_context.get(
            "intent"
        )

    if intent is None:
        return ""

    if hasattr(
        intent,
        "value",
    ):
        intent = intent.value

    return str(
        intent
    ).upper().strip()


# ============================================================
# ROUTE BY INTENT
# ============================================================

def route_by_intent(
    state: CivicHelpState,
) -> str:

    intent = get_intent(state)

    print("\n" + "=" * 70)
    print("[GRAPH ROUTING - INTENT]")
    print("=" * 70)

    print(
        f"Intent: {intent}"
    )

    if intent == "SCHEME_DISCOVERY":

        print(
            "Next Node: discover_schemes"
        )

        print("=" * 70)

        return "scheme_discovery"

    print(
        "Next Node: detect_scheme"
    )

    print("=" * 70)

    return "scheme_query"


# ============================================================
# ROUTE AFTER SCHEME DETECTION
# ============================================================

def route_after_scheme_detection(
    state: CivicHelpState,
) -> str:

    status = str(
        state.get(
            "status",
            "",
        )
    ).upper().strip()

    scheme = state.get(
        "scheme"
    )

    print("\n" + "=" * 70)
    print("[GRAPH ROUTING - SCHEME]")
    print("=" * 70)

    print(
        f"Status: {status}"
    )

    print(
        f"Scheme: {scheme}"
    )

    if status == "SCHEME_IDENTIFIED":

        print(
            "Next Node: extract_profile"
        )

        print("=" * 70)

        return "scheme_identified"

    print(
        "Next Node: retrieve_evidence"
    )

    print("=" * 70)

    return "scheme_not_identified"


# ============================================================
# ROUTE AFTER VALIDATION
# ============================================================

def route_after_validation(
    state: CivicHelpState,
) -> str:

    intent = get_intent(state)

    print("\n" + "=" * 70)
    print("[GRAPH ROUTING - VALIDATION]")
    print("=" * 70)

    print(
        f"Intent: {intent}"
    )

    if intent == "ELIGIBILITY":

        print(
            "Next Node: evaluate_eligibility"
        )

        print("=" * 70)

        return "eligibility"

    print(
        "Next Node: generate_answer"
    )

    print("=" * 70)

    return "answer"


# ============================================================
# CREATE GRAPH
# ============================================================

builder = StateGraph(
    CivicHelpState
)


# ============================================================
# ADD NODES
# ============================================================

builder.add_node(
    "understand_query",
    understand_query,
)

builder.add_node(
    "plan_query",
    plan_query,
)

builder.add_node(
    "route_query",
    route_query,
)

builder.add_node(
    "detect_scheme",
    detect_scheme,
)

builder.add_node(
    "extract_profile",
    extract_profile,
)

builder.add_node(
    "retrieve_evidence",
    retrieve_evidence,
)

builder.add_node(
    "validate_evidence",
    validate_evidence,
)

builder.add_node(
    "evaluate_eligibility",
    evaluate_eligibility,
)

builder.add_node(
    "build_citations",
    build_citations,
)

builder.add_node(
    "discover_schemes",
    discover_schemes,
)

builder.add_node(
    "retrieve_discovery_evidence",
    retrieve_discovery_evidence,
)

builder.add_node(
    "generate_answer",
    generate_answer,
)

builder.add_node(
    "build_response",
    build_response,
)


# ============================================================
# START
# ============================================================

builder.add_edge(
    START,
    "understand_query",
)


# ============================================================
# QUERY PIPELINE
# ============================================================

builder.add_edge(
    "understand_query",
    "plan_query",
)

builder.add_edge(
    "plan_query",
    "route_query",
)


# ============================================================
# QUERY ROUTING
# ============================================================

builder.add_conditional_edges(
    "route_query",
    route_by_intent,
    {
        "scheme_discovery": "discover_schemes",
        "scheme_query": "detect_scheme",
    },
)


# ============================================================
# DISCOVERY PIPELINE
# ============================================================

builder.add_edge(
    "discover_schemes",
    "retrieve_discovery_evidence",
)

# IMPORTANT:
# Discovery must also go through evidence validation.

builder.add_edge(
    "retrieve_discovery_evidence",
    "validate_evidence",
)


# ============================================================
# NORMAL RAG PIPELINE
# ============================================================

builder.add_conditional_edges(
    "detect_scheme",
    route_after_scheme_detection,
    {
        "scheme_identified": "extract_profile",
        "scheme_not_identified": "retrieve_evidence",
    },
)

builder.add_edge(
    "extract_profile",
    "retrieve_evidence",
)

builder.add_edge(
    "retrieve_evidence",
    "validate_evidence",
)


# ============================================================
# VALIDATION ROUTING
# ============================================================

builder.add_conditional_edges(
    "validate_evidence",
    route_after_validation,
    {
        "eligibility": "evaluate_eligibility",
        "answer": "generate_answer",
    },
)


# ============================================================
# ELIGIBILITY
# ============================================================

builder.add_edge(
    "evaluate_eligibility",
    "generate_answer",
)


# ============================================================
# ANSWER → CITATIONS
# ============================================================

builder.add_edge(
    "generate_answer",
    "build_citations",
)


# ============================================================
# CITATIONS → RESPONSE
# ============================================================

builder.add_edge(
    "build_citations",
    "build_response",
)


# ============================================================
# RESPONSE → END
# ============================================================

builder.add_edge(
    "build_response",
    END,
)


# ============================================================
# COMPILE
# ============================================================

civichelp_graph = builder.compile()


# ============================================================
# OPTIONAL TEST
# ============================================================

if __name__ == "__main__":

    print("\n" + "=" * 70)
    print("CIVICHELP AI GRAPH")
    print("=" * 70)

    try:

        print(
            civichelp_graph
            .get_graph()
            .draw_ascii()
        )

    except Exception as exc:

        print(
            "Graph visualization unavailable:",
            exc,
        )

    print("=" * 70)
    print(
        "Graph compiled successfully."
    )
    print("=" * 70)