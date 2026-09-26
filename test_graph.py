from app.agents.graph import civichelp_graph


def main():

    print("=" * 80)

    print(
        "CIVICHELP AI - LANGGRAPH TEST"
    )

    print("=" * 80)

    query = (
        "I am 72 years old and I live in "
        "Telangana. Am I eligible for the "
        "Vay Vandana scheme?"
    )

    print("\nQUERY")
    print("-" * 80)
    print(query)

    initial_state = {
        "query": query
    }

    print("\nRunning LangGraph...\n")

    final_state = civichelp_graph.invoke(
        initial_state
    )

    print("\n" + "=" * 80)
    print("LANGGRAPH RESULT")
    print("=" * 80)

    print("\nSCHEME")
    print("-" * 80)
    print(
        final_state.get(
            "scheme"
        )
    )

    print("\nPROFILE")
    print("-" * 80)
    print(
        final_state.get(
            "profile"
        )
    )

    print("\nELIGIBILITY")
    print("-" * 80)
    print(
        final_state.get(
            "eligibility"
        )
    )

    print("\nEVIDENCE VALIDATION")
    print("-" * 80)
    print(
        final_state.get(
            "evidence_validation"
        )
    )

    print("\nCITATIONS")
    print("-" * 80)

    for citation in final_state.get(
        "citations",
        [],
    ):

        print(
            f"{citation.get('document_id')} | "
            f"{citation.get('title')} | "
            f"{citation.get('authority')}"
        )

        print(
            f"URL: {citation.get('url')}"
        )

    print("\nANSWER")
    print("-" * 80)

    print(
        final_state.get(
            "answer"
        )
    )

    print("\nFINAL RESPONSE")
    print("-" * 80)

    print(
        final_state.get(
            "response"
        )
    )


if __name__ == "__main__":
    main()