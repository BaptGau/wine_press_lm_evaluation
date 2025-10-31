
class RetrievedSourcesFWPairing {
    reasoning string @description("Un raisonnement rapide et concis sur les sources mentionnées par le modèle.")
    sources string[]? @description("La liste des sources mentionnées par l'agent.")
}

function RetrieveSourcesFoodWinePairing(history: string, source_retrieval_query: string, response: string) -> RetrievedSourcesFWPairing {
    client GPT5GreedySampling

    prompt #"
    {{ _.role("system") }}
    <instructions>
    Il a été posé une question à un agent conversationnel. Après sa réponse nous lui avons demandé de citer ses sources.
    Ta tâche est de récupérer les sources mentionnées par l'agent.
    </instructions>

    <input>
    ## Interactions précédentes:
    """
    {{ history }}
    """
    ----

    Réponse à la question "{{ source_retrieval_query }}":
    """
    {{ response }}
    """
    </input>

    {{ ctx.output_format }}
    "#
}