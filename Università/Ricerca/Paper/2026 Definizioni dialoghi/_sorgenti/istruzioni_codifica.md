# Istruzioni per la codifica delle definizioni esplicite nei dialoghi di Agostino (codebook bozza 11.3)

Queste istruzioni sono tutto ciò che il codificatore riceve, insieme al testo latino diviso in frasi.

## Compito

Leggi il testo latino frase per frase e segna le frasi in cui l'opera fornisce una definizione, secondo i criteri qui sotto. Il criterio è dichiarato e va applicato com'è scritto: non usare conoscenze esterne sul dialogo, sull'autore o sulla letteratura critica; giudica soltanto sulla base del testo che hai davanti.

## Unità

L'unità è la frase (chiusa da punto, punto interrogativo o esclamativo), già divisa nel file. Ogni riga del file è: riferimento della frase (libro.capitolo.paragrafo.frase, oppure capitolo.paragrafo.frase), proposta automatica dell'indicatore 1 (le forme di *definio/definitio* trovate nella frase, se ci sono), testo latino.

## Indicatori

Per ogni frase poniti queste domande. Una frase può avere più indicatori.

- **1** — La frase usa il verbo «definire» o la parola «definizione» (*definio*, *definitio*, e le loro forme; anche *finio/finitio* quando valgono «definire» e non «terminare»)? Le frasi con una forma di *defin-* arrivano già con la proposta automatica: confermala o respingila (respingila solo se la parola non ha senso definitorio). *Descriptio* non vale come indicatore 1.
- **2** — La frase usa un altro verbo al posto di «definire» per dire che cos'è X, e lo spiega? Verbi di dire (*dico*), pensare (*puto, arbitror, existimo, censeo*), volere (*volo*), stabilire o accettare (*constat, placet, statuo, constituo*), nominare (*voco, appello, nomino*), delimitare il concetto (*determino*), o la forma «per noi X è» (*nobis X est*); di solito con la struttura «X *esse* Y». L'elenco è **aperto**: vale qualunque verbo che introduca la definizione al posto di «definire» (per esempio *videri, iudicare, intellegere, significare*); se *constat* vale «consiste di», è una copula e la frase va al 3.
- **3** — La frase dà una definizione senza alcun verbo che la introduca, semplicemente «X è Y»?
- **P** — La frase afferma o esclude una **proprietà definitoria** di X: una proprietà che vale per X in quanto X (universale, non legata a un caso singolo), detta dentro una discussione su X? Per esempio «Beatus errare non potest» (definizione per negazione). È una definizione parziale: si registra con il suo definiendum, distinta da 1, 2, 3. Non vanno segnate le mosse puramente argomentative (concedere o rifiutare, premesse su altro, conclusioni che non dicono nulla di X) né le proprietà di un caso singolo («Licentius est stanco»).

**Conclusioni.** *Ergo*, *igitur* e la posizione della frase nel ragionamento (premessa, conclusione, risposta) non decidono il segno: decide che cosa la frase dice di X. Un'identità piena («Bona ergo fides est, ex animi sententia») è 3; una proprietà o condizione di X in quanto X («Deum qui habet, beatus est») è P; un'affermazione su un caso singolo non si segna. La posizione si può annotare nella nota («Esse (conclusione: ergo)»).

**Glosse, relative, figure.**
- Una glossa con *id est* / *hoc est* vale 3 solo se il termine glossato è oggetto del discorso in quel passo (il passo ne discute la definizione o le proprietà); altrimenti non si segna, e se utile si annota «Id est (glossa)».
- Una definizione contenuta in una relativa («sapientiam quae in investigatione posita est») si tratta come se fosse nella principale: 2 o 3 se dice che cos'è X, P se ne dà una proprietà.
- Le identificazioni allegoriche o figurate (un personaggio, un luogo, un'immagine che «rappresenta» qualcosa) non si segnano come definizioni; si possono registrare con il definiendum e la nota «Allegoria», senza indicatore.

**Filtro per 2 e 3.** L'enunciato conta solo se dice che cosa X è, anche per cause o per effetti; non quando esprime un'opinione su X. «Penso che X sia stanco» non è una definizione; «penso che X sia stanco perché vuole andar via o perché dorme» definisce la stanchezza dagli effetti.

## Campi da compilare per ogni frase segnata

- **ind**: gli indicatori separati da spazio (es. `1`, `2 3`, `P`).
- **definiendum**: il termine di cui si cerca o si dà la definizione, **nella forma in cui compare nel testo** (es. *Beate vivere*, *Errare*, *Sapientiam*), con l'iniziale maiuscola. Più termini separati da «; ». Quando la frase parla del definire in sé (chiedere una definizione, discuterne l'utilità), il definiendum è *Definire*.
- **nuovo_ep**: `x` se la frase apre una ripresa separata di un termine già definito prima (una discussione nuova sullo stesso termine); altrimenti vuoto.
- **nota**: il verbo con cui la definizione è introdotta, in forma di **infinito latino con l'iniziale maiuscola** (*Velle*, *Placere*, *Dicere*, *Vocare*, *Esse* per l'indicatore 3…), seguito eventualmente tra parentesi da particolarità brevi (es. «Dicere (autorità: Zeno)», «Esse (interrogativa)»). Se nella frase ci sono due definienda con verbi diversi: «Termine: Verbo; Termine: Verbo».

**Definizioni ipotetiche, respinte o riferite.** Contano come le altre: l'indicatore registra che il testo definisce, non che la definizione sia accettata. Nella nota si aggiunge tra parentesi lo stato quando è evidente: «(ipotetica)», «(respinta)», «(corretta)», «(autorità: …)».

Si possono registrare con definiendum ma **senza indicatore** anche le domande del tipo «quid est X?» che aprono una definizione (nota: «Quid est (domanda, senza indicatore)»).

## Formato di uscita

File TSV con intestazione, una riga per frase segnata, colonne separate da tabulazione:

```
frase	ind	definiendum	nuovo_ep	nota
```

Le frasi non segnate non compaiono.
