class WineForAperitif {
    specialised_press_mention string[]? @description("La liste des revues de presse spécialisées mentionnées dans la réponse s'il y en a")
    context bool @description("Si le texte recontextualise la demande - en la répétant et/ou en ajoutant des détails à cette dernière")
    concrete_suggestions bool @description("Si le text m'indique vers quelles bouteilles me tourner. Une famille ou un cépage n'est pas assez concret, il faut des mentions de bouteilles")
    region_suggestion bool @description("Si le texte continent une suggestion d’une région de production particulière")
    cepage_suggestion bool @description("Si le texte continent une suggestion d’un cépage particulier")
    domain_suggestion bool @description("Si le texte continent une suggestion d'un domaine particulier")
    aromatics_notes bool @description("Si le texte contient des précisions sur les notes aromatiques d'au moins un des vins mentionnés")
    purchase_place bool @description("Si le texte fourni continent une suggestion d'un lieu d'achat des vins")
    price_mention bool @description("Si le text contient une/des mention(s) de prix concernant au moins un des vins")
    wine_advices bool @description("Si le texte fourni des conseils œnologiques généraux")
    precision_proposal bool @description("Si le texte propose de préciser la demande initiale par des informations complémentaires")
}

function EvaluateWineForAperitif(query: string, response: string) -> WineForAperitif {
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