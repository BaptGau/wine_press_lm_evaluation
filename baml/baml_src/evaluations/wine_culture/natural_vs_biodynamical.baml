class NaturalVsBiodynamical {
    specialised_press_mention string[]? @description("La liste des revues de presse spécialisées mentionnées dans la réponse s'il y en a")
    context bool @description("Si le texte recontextualise la demande - en la répétant et/ou en ajoutant des détails à cette dernière")
    notions_definition bool @description("Si le texte donne une définition du vin nature et une du vin biodynamique")
    synthetical_comparison bool @description("Si le texte fournit une comparaison synthétique du vin nature et du vin biodynamique")
    central_idea_conclusion bool @description("Si le texte conclut son explication par une idée centrale entre la différence entre le vin nature et le vin biodynamique")
    visual_support_proposal bool @description("Si le texte propose un support visuel")

}

function EvaluateNaturalVsBiodynamical(query: string, response: string) -> NaturalVsBiodynamical {
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