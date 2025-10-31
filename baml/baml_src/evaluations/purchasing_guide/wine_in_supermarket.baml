class WineInSupermarket {
    specialised_press_mention string[]? @description("La liste des revues de presse spécialisées mentionnées dans la réponse s'il y en a")
    context bool @description("Si le texte recontextualise la demande - en la répétant et/ou en ajoutant des détails à cette dernière")
    precise_objective bool @description("Si le texte définit un objectif précis de sélection du vin") // bancal
    region_reference bool @description("Si le texte continent une référence pour une ou plusieurs région(s) de production")
    calling_reference bool @description("Si le texte contient une référence pour une plusieurs appellation(s)")
    label_analysis_advices bool @description("Si le texte contient un ou plusieurs conseils vis à l'analyse des étiquettes des vins")
    wine_advices bool @description("Si le texte fourni des conseils œnologiques généraux")
    precision_proposal bool @description("Si le texte propose de préciser la demande initiale par des informations complémentaires")
}

function EvaluateWineInSupermarket(query: string, response: string) -> WineInSupermarket {
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