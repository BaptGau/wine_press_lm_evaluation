class CarbonicMaceration {
    specialised_press_mention string[]? @description("La liste des revues de presse spécialisées mentionnées dans la réponse s'il y en a")
    context bool @description("Si le texte recontextualise la demande - en la répétant et/ou en ajoutant des détails à cette dernière")
    carbonic_maceration_principle bool @description("Si le texte explique le principe de la macération carbonique")
    carbonic_maceration_effects bool @description("Si le texte explique les effets de la macération carbonique")
    precisions_about_nuances bool @description("Si le texte mentionne des précisions sur les nuances du concept")
    visual_synthesis_proposal bool @description("Si le texte propose de réaliser une synthétisation visuelle (tableau, schéma, ...)")
}

function EvaluateCarbonicMaceration(query: string, response: string) -> CarbonicMaceration {
    client GPT5GreedySampling

    prompt #"
    {{ _.role("system") }}
    <instructions>
    Il a été demandé la question suivante à un modèle de langage:
    "{{ query }}"
    Ta tâche est d'évaluer à partir de la grille fournie, la réponse à la question.
    Nous voulons extraire de la réponse, un certain nombre de critère qui te seront détaillés ci-après.
    </instructions>

    <input>
    Réponse à la question: "{{ query }}"
    """
    {{ response }}
    """
    </input>

    {{ ctx.output_format }}
    "#
}