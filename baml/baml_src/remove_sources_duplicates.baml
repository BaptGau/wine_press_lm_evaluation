enum ExistingSource {
    @@dynamic
}

class SourceExtracted {
    reasoning string @description("Un raisonnement décrivant les différentes sources, identifiant les points de convergence et les différences permettant de filtrer sur les sources réellement différentes.")
    sources_mapper map<ExistingSource, string> @description("Le mapping des anciennes sources (celles fournies) vers leur nouvelle valeur (celles que tu as identifiées)")
}

function RemoveSourcesDuplicates(sources: string[]) -> SourceExtracted {
    client GPT5

    prompt #"
    {{ _.role("system") }}
    <instructions>
    Nous avons demandé à un agent conversationnel de citer ses sources pour répondre à une question.
    Cependant, certaines de ces sources semblent se recouper. Par exemple:
    "Sources publiques (intégrées au corpus d’entraînement)" et "Données accessibles au public" peuvent être considérées comme la même source.
    Ta mission est d'identifier ces sources dupliquées et de les filtrer pour ne garder que les sources véritablement différentes.
    Pour répondre, tu fourniras un d'abord raisonnement identifiant les différentes sources et les doublons. Puis tu fourniras la liste des sources filtrées.
    Les sources extraites ne doivent pas contenir d'informations commune. Tout se passe comme-ci tu identifiais les composantes principales du vecteur des sources fournies.
    Note: tu peux renommer des sources pour fusionner des sens sémantiques proches proches.
    </instructions>

    <input>
    ## Sources à filtrer:
    """
    {{ sources }}
    """
    </input>

    {{ ctx.output_format }}
    "#
}