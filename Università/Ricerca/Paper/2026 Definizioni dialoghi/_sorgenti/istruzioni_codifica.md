# Istruzioni per la codifica delle definizioni esplicite nei dialoghi di Agostino (codebook bozza 10.1)

Queste istruzioni sono tutto ciò che il codificatore riceve, insieme al testo latino diviso in frasi.

## Compito

Leggi il testo latino frase per frase e segna le frasi in cui l'opera fornisce una definizione, secondo i criteri qui sotto. Il criterio è dichiarato e va applicato com'è scritto: non usare conoscenze esterne sul dialogo, sull'autore o sulla letteratura critica; giudica soltanto sulla base del testo che hai davanti.

## Unità

L'unità è la frase (chiusa da punto, punto interrogativo o esclamativo), già divisa nel file. Ogni riga del file è: riferimento della frase (libro.capitolo.paragrafo.frase, oppure capitolo.paragrafo.frase), proposta automatica dell'indicatore 1 (le forme di *definio/definitio* trovate nella frase, se ci sono), testo latino.

## Indicatori

Per ogni frase poniti queste domande. Una frase può avere più indicatori.

- **1** — La frase usa il verbo «definire» o la parola «definizione» (*definio*, *definitio*, e le loro forme; anche *finio/finitio* quando valgono «definire» e non «terminare»)? Le frasi con una forma di *defin-* arrivano già con la proposta automatica: confermala o respingila (respingila solo se la parola non ha senso definitorio). *Descriptio* non vale come indicatore 1.
- **2** — La frase usa un altro verbo al posto di «definire» per dire che cos'è X, e lo spiega? Verbi di dire (*dico*), pensare (*puto, arbitror, existimo, censeo*), volere (*volo*), stabilire o accettare (*constat, placet, statuo, constituo*), nominare (*voco, appello, nomino*), o la forma «per noi X è» (*nobis X est*); di solito con la struttura «X *esse* Y».
- **3** — La frase dà una definizione senza alcun verbo che la introduca, semplicemente «X è Y»?
- **T** — La frase non definisce X ma è una **tesi** su X: ne nega o esclude una proprietà, la ricava come conclusione (*igitur*, *ergo*), la concede o la rifiuta, la pone come premessa. Non conta come definizione, ma si registra con il suo definiendum.

**Filtro per 2 e 3.** L'enunciato conta solo se dice che cosa X è, anche per cause o per effetti; non quando esprime un'opinione su X. «Penso che X sia stanco» non è una definizione; «penso che X sia stanco perché vuole andar via o perché dorme» definisce la stanchezza dagli effetti.

## Campi da compilare per ogni frase segnata

- **ind**: gli indicatori separati da spazio (es. `1`, `2 3`, `T`).
- **definiendum**: il termine di cui si cerca o si dà la definizione, **nella forma in cui compare nel testo** (es. *Beate vivere*, *Errare*, *Sapientiam*), con l'iniziale maiuscola. Più termini separati da «; ». Quando la frase parla del definire in sé (chiedere una definizione, discuterne l'utilità), il definiendum è *Definire*.
- **nuovo_ep**: `x` se la frase apre una ripresa separata di un termine già definito prima (una discussione nuova sullo stesso termine); altrimenti vuoto.
- **nota**: il verbo con cui la definizione è introdotta, in forma di **infinito latino con l'iniziale maiuscola** (*Velle*, *Placere*, *Dicere*, *Vocare*, *Esse* per l'indicatore 3…), seguito eventualmente tra parentesi da particolarità brevi (es. «Dicere (autorità: Zeno)», «Esse (interrogativa)»). Se nella frase ci sono due definienda con verbi diversi: «Termine: Verbo; Termine: Verbo».

Si possono registrare con definiendum ma **senza indicatore** anche le domande del tipo «quid est X?» che aprono una definizione (nota: «Quid est (domanda, senza indicatore)»).

## Formato di uscita

File TSV con intestazione, una riga per frase segnata, colonne separate da tabulazione:

```
frase	ind	definiendum	nuovo_ep	nota
```

Le frasi non segnate non compaiono.
