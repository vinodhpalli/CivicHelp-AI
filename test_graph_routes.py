import json
from pathlib import Path

from app.agents.graph import civichelp_graph


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CHUNKS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "telangana_chunks.json"
)


with open(
    CHUNKS_PATH,
    "r",
    encoding="utf-8",
) as file:

    chunks = json.load(file)


print(
    f"Loaded {len(chunks)} chunks from "
    f"{CHUNKS_PATH}"
)


TEST_QUERIES = [

    "I am 72 years old and I live in Telangana. "
    "Am I eligible for the Vay Vandana scheme?",

    "What documents are required for ePASS?",

    "How do I apply for Telangana scholarship?",

    "My scholarship application was rejected. "
    "What should I do?",

    "What government schemes are available for farmers?",

    "What is the Rythu Bharosa scheme?",
]


print("=" * 80)
print("CIVICHELP AI - LANGGRAPH ROUTING TEST")
print("=" * 80)


for index, query in enumerate(
    TEST_QUERIES,
    start=1,
):

    print(
        "\n\n"
        + "=" * 80
    )

    print(
        f"TEST {index}"
    )

    print(
        "=" * 80
    )

    print(
        "\nQUERY\n"
        + "-" * 80
    )

    print(query)

    initial_state = {
        "query": query
    }

    result = civichelp_graph.invoke(
        initial_state
    )

    print(
        "\nROUTE\n"
        + "-" * 80
    )

    print(
        result.get(
            "query_route"
        )
    )

    print(
        "\nSCHEME\n"
        + "-" * 80
    )

    print(
        result.get(
            "scheme"
        )
    )

    print(
        "\nSTATUS\n"
        + "-" * 80
    )

    print(
        result.get(
            "status"
        )
    )

    print(
        "\nELIGIBILITY\n"
        + "-" * 80
    )

    print(
        result.get(
            "eligibility"
        )
    )

    print(
        "\nEVIDENCE VALIDATION\n"
        + "-" * 80
    )

    evidence_validation = (
        result.get(
            "evidence_validation",
            {}
        )
    )

    print(
        "status:",
        evidence_validation.get(
            "status"
        )
    )

    print(
        "answer_supported:",
        evidence_validation.get(
            "answer_supported"
        )
    )

    print(
        "query_support_score:",
        evidence_validation.get(
            "query_support_score"
        )
    )

    print(
        "\nPRIMARY EVIDENCE\n"
        + "-" * 80
    )

    print(
        evidence_validation.get(
            "primary_evidence",
            []
        )
    )

    print(
        "\nSUPPORTING EVIDENCE\n"
        + "-" * 80
    )

    print(
        evidence_validation.get(
            "supporting_evidence",
            []
        )
    )

    print(
        "\nUNRELATED EVIDENCE\n"
        + "-" * 80
    )

    print(
        evidence_validation.get(
            "unrelated_evidence",
            []
        )
    )

    print(
        "\nVERIFIED CITATIONS\n"
        + "-" * 80
    )

    print(
        result.get(
            "citations",
            []
        )
    )

    print(
        "\nANSWER\n"
        + "-" * 80
    )

    print(
        result.get(
            "answer"
        )
    )

    print(
        "\nFINAL RESPONSE\n"
        + "-" * 80
    )

    print(
        result.get(
            "response"
        )
    )


print(
    "\n\n"
    + "=" * 80
)

print(
    "ALL TESTS COMPLETED"
)

print(
    "=" * 80
)