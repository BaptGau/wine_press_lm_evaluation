class WineIssues {
    specialised_press_mention string[]? @description("La liste des revues de presse spécialisées mentionnées dans la réponse s'il y en a")
    context bool @description("Si le texte recontextualise la demande - en la répétant et/ou en ajoutant des détails à cette dernière")
    organize_per_category bool @description("Si le texte est organisé par catégorie de défaut (une section par type de défaut)")
    same_organisation_per_fault_type bool @description("Si pour chaque type de défaut mentionné, l'organisation de la réponse est similaire")
    precision_proposal bool @description("Si le texte propose de préciser la demande initiale par des informations complémentaires")
    visual_synthesis_proposal bool @description("Si le texte propose de réaliser une synthétisation visuelle (tableau, schéma, ...)")
}

function EvaluateWineIssues(query: string, response: string) -> WineIssues {
    client GPT5

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