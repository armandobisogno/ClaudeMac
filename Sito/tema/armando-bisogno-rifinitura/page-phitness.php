<?php
/**
 * Template della pagina.
 *
 * @package armando-bisogno
 */

get_header();
?>
<main id="main">
  <div class="hero-band">
    <div class="wrap">
      <div class="hero">
        <div>
          <a class="phit-lockup" href="https://www.phitness.it/" aria-label="Phitness"><?php echo ab_phitness_mark( 44 ); // SVG statico. ?><span class="phit-word"><b>Phi</b>tness</span></a>
          <span class="eyebrow">Laboratorio di filosofia</span>
          <h1>Un allenamento per <em>il pensiero</em></h1>
          <p class="lead">Phitness è un <em>fitness</em> filosofico.</p>
          <p class="lead" style="margin-top:12px">Porta nella tua azienda o nella tua comunità un esercizio guidato per recuperare tre capacità che il tempo di oggi consuma: concentrarsi su un problema, leggere con attenzione, scrivere dopo aver pensato.</p>
          <div class="actions"><a class="btn btn-primary" href="#richiesta">Richiedi un incontro</a></div>
        </div>
        <figure class="portrait bw">
          <div class="frame" style="aspect-ratio:3/4"><img src="<?php echo esc_url( AB_IMG ); ?>armando-palco.jpg" alt="Armando Bisogno durante un incontro pubblico, in bianco e nero"></div>
        </figure>
      </div>
    </div>
  </div>

  <section class="block">
    <div class="wrap split">
      <div class="head" style="margin:0"><span class="eyebrow">Il perché</span><h2>Perché un laboratorio di pensiero, di lettura e di scrittura?</h2></div>
      <div class="prose muted">
        <span class="sublabel">Il problema</span>
        <p>Da decenni gli studi registrano un lento declino delle nostre capacità cognitive. Vediamo e produciamo contenuti veloci, che non chiedono attenzione né a chi li scrive né a chi li legge. Siamo sempre connessi, ma raramente presenti.</p>
        <p>L'intelligenza artificiale ha amplificato il fenomeno: riassume i testi e li scrive al posto nostro. E più perdiamo l'abitudine di concentrarci, di leggere a fondo, di costruire un'idea prima di metterla per iscritto, più ci sembra naturale lasciarlo fare alla macchina.</p>
        <span class="sublabel">La risposta</span>
        <p>Il problema, però, non è la macchina: è quello che smettiamo di fare noi. Pensare chiede tempo e presenza, cioè esserci davvero davanti a una domanda. La lettura attenta nutre, perché ci fa abitare per un po' le parole di un altro. La scrittura consapevole non serve solo a dire quello che pensiamo: è il modo in cui scopriamo che cosa pensiamo.</p>
        <p>Sono capacità che si allenano, come un muscolo. Per questo abbiamo bisogno di un allenamento vero e proprio, un <em>fitness</em> cognitivo.</p>
        <p><strong class="brand-word">Phitness</strong> nasce da qui.</p>
      </div>
    </div>
  </section>

  <section class="block tint">
    <div class="wrap">
      <div class="head"><span class="eyebrow">Il metodo</span><h2>Tre esercizi, sempre in quest'ordine</h2></div>
      <ol class="steps">
        <li><h3>Esercizio filosofico</h3><p>Un problema della storia della filosofia, presentato in modo chiaro, per allenare la mente a restare focalizzata su un solo tema, per approfondirlo e discuterlo insieme.</p></li>
        <li><h3>Esercizio di lettura</h3><p>Uno o più testi, letti in silenzio. Concentrarsi sulle parole per pe(n)sarne il significato. Poi ci si confronta insieme: chi vuole racconta che cosa ha trovato in quelle pagine.</p></li>
        <li><h3>Esercizio di scrittura</h3><p>Scrivere un testo su un argomento dato al momento. Perché mai si è scritto così tanto come oggi e mai si è dedicato così poco tempo a farlo bene. Alla fine della sessione, chi vuole può condividere il suo testo in forma anonima e ricevere un <em>feedback</em>.</p></li>
      </ol>
    </div>
  </section>

  <section class="block band">
    <div class="wrap split">
      <p class="pull">Zero performance, <em>solo esercizio.</em></p>
      <p class="prose">Phitness non è una gara né una valutazione. Nessuno viene interrogato, nessuno deve scrivere più o meglio dei colleghi. È un tempo restituito al pensiero, con i ritmi di ciascuno.</p>
    </div>
  </section>

  <section class="block tint">
    <div class="wrap">
      <?php ab_lessons_carousel(); ?>
    </div>
  </section>

  <section class="block">
    <div class="wrap split" style="align-items:start">
      <div class="head" style="margin:0"><span class="eyebrow">Un incontro</span><h2>Come si svolge, dall'inizio alla fine</h2></div>
      <ol class="timeline">
        <li><span class="dot"></span><div><strong>Accoglienza</strong><span>Si spiega che cosa accadrà e perché. Si spengono le notifiche.</span></div></li>
        <li><span class="dot"></span><div><strong>Esercizio filosofico</strong><span>Il problema del giorno, presentato senza tecnicismi e discusso insieme.</span></div></li>
        <li><span class="dot"></span><div><strong>Esercizio di lettura</strong><span>I testi, prima in silenzio, ognuno con il proprio ritmo. Poi un confronto a voce: che cosa ci ha colpito, quali parole sono rimaste.</span></div></li>
        <li><span class="dot"></span><div><strong>Esercizio di scrittura</strong><span>Proviamo a scrivere, a mano o sul proprio dispositivo, su un argomento proposto al momento.</span></div></li>
        <li class="key"><span class="dot"></span><div><strong>Consegna, se vuoi</strong><span>Chi lo desidera consegna il proprio testo, in forma anonima, e riceverà una restituzione personalizzata.</span><br><a class="go-on" href="#restituzione">Come funziona ↓</a></div>
          <a class="arrow-down" href="#restituzione" aria-label="Vai a come funziona la restituzione"><svg viewBox="0 0 120 190" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 4 C 10 60, 96 70, 78 176"/><path d="M62 160 L 78 178 L 94 158"/></svg></a></li>
      </ol>
    </div>
  </section>

  <section class="block band deep" id="restituzione">
    <div class="wrap">
      <div class="head"><span class="eyebrow">Dopo l'incontro</span><h2>Una restituzione personale, <em>in forma anonima</em></h2><p class="lead">Scrivere è l'esercizio più esposto, per questo è anche il più protetto. Consegnare il testo è una scelta, mai un obbligo.</p></div>
      <div class="give">
        <div><b>Chi vuole, consegna</b><p>Alla fine dell'incontro ognuno decide se lasciare il proprio testo. Chi preferisce tenerlo per sé lo porta via, e nessuno lo leggerà.</p></div>
        <div><b>Senza nome</b><p>Il testo si consegna in forma completamente anonima. Nessuno saprà chi ha scritto cosa. Nemmeno io.</p></div>
        <div><b>Una lettura dedicata</b><p>Ogni testo consegnato riceve una restituzione personalizzata: una lettura attenta, con osservazioni su come il pensiero è stato costruito e messo per iscritto.</p></div>
      </div>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="head"><span class="eyebrow">Formati</span></div>
      <div class="formats">
        <div class="format">
          <span class="chip">Un incontro</span>
          <h3>La sessione singola</h3>
          <p>Un laboratorio per far conoscere il metodo al gruppo. Adatto a una giornata di formazione, a un evento interno, a una pausa dal lavoro ordinario.</p>
          <ul><li>Un tema filosofico scelto per l'occasione</li><li>I tre esercizi completi</li><li>La restituzione personalizzata per chi consegna il testo</li></ul>
        </div>
        <div class="format color">
          <span class="chip" style="background:var(--card)">Più incontri</span>
          <h3>Il percorso</h3>
          <p>Gli stessi tre esercizi della sessione singola, in un ciclo di incontri. Il percorso dei temi si concorda insieme e i <em>feedback</em> vengono ripresi e discussi di incontro in incontro: ne nasce una specie di itinerario.</p>
          <ul><li>In ogni incontro, i tre esercizi completi</li><li>Numero, frequenza e percorso dei temi concordati insieme</li><li>I <em>feedback</em> ripresi e discussi all'incontro successivo, sempre in forma anonima</li><li>Un itinerario che cresce da un incontro all'altro</li></ul>
        </div>
      </div>
    </div>
  </section>

  <section class="block tint" id="richiesta">
    <div class="wrap split">
      <div class="head" style="margin:0">
        <span class="eyebrow">Contatti</span>
        <h2>Vuoi portare Phitness nella tua azienda o nella tua comunità?</h2>
        <p class="lead">Lascia il tuo contatto: ti ricontatterò per capire insieme come organizzare un appuntamento.</p>
      </div>
      <div class="formbox">
        <?php ab_contact_form( 'phitness' ); ?>
      </div>
    </div>
  </section>
</main>
<?php
get_footer();
