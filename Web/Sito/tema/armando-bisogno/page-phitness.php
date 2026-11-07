<?php
/**
 * Template della pagina.
 *
 * @package armando-bisogno
 */

get_header();
?>
<main id="main">
  <section class="ph-hero">
    <div class="wrap ph-hero-in">
      <div class="ph-hero-txt">
        <a class="phit-lockup" href="https://www.phitness.it/" aria-label="Phitness"><?php echo ab_phitness_mark( 44 ); // SVG statico. ?><span class="phit-word"><b>Phi</b>tness</span></a>
        <span class="eyebrow">Laboratorio di filosofia</span>
        <h1>Cosa resterà?<br><em>Le nostre passioni.</em></h1>
        <p class="lead">Nella stagione dell'IA quello che resta umano è ciò che facciamo per il piacere di farlo.</p>
        <p class="lead"><em>Phitness</em> è proprio questo.</p>
        <p class="lead">Un <em>fitness</em> filosofico con la tua comunità (associazioni, scuole, biblioteche, aziende, etc.) per coltivare tre passioni tutte umane: pensare, leggere, scrivere.</p>
        <div class="actions"><a class="btn btn-primary" href="#richiesta">Richiedi un incontro</a></div>
      </div>
    </div>
  </section>

  <section class="ph-diptych">
    <div class="ph-dip ph-dip--ia">
      <h2>Cosa stiamo delegando<br><em>all’IA?</em></h2>
      <p>L'intelligenza artificiale scrive, riassume, compone. E lo farà sempre meglio.<br>Le affidiamo volentieri i testi che abbiamo sempre vissuto come meccanici e ripetitivi.</p>
    </div>
    <div class="ph-dip ph-dip--noi">
      <h2>Cosa resterà<br><em>sempre nostro?</em></h2>
      <p>Non saremo mai disposti a delegare ciò che ci permette di esprimerci.<br>Le attività nelle quali conta essere noi stessi e non conta il risultato.</p>
      <p class="ph-dip-end"><em>Phitness</em> nasce per allenare e coltivare queste attività.</p>
    </div>
  </section>

  <section class="ph-lab">
    <div class="wrap ph-lab-in">
      <svg class="ph-tre" viewBox="0 0 264 124" aria-hidden="true"><path d="M80.3 26.4 A42 42 0 1 1 62.4 20.2" fill="none" stroke="currentColor" stroke-width="6.5" stroke-linecap="round"/><path d="M154.3 26.4 A42 42 0 1 1 136.4 20.2" fill="none" stroke="currentColor" stroke-width="6.5" stroke-linecap="round"/><path d="M228.3 26.4 A42 42 0 1 1 210.4 20.2" fill="none" stroke="currentColor" stroke-width="6.5" stroke-linecap="round"/><path d="M77.2 29.1 A40 40 0 1 1 24.5 87.6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" opacity=".5"/><path d="M151.2 29.1 A40 40 0 1 1 98.5 87.6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" opacity=".5"/><path d="M225.2 29.1 A40 40 0 1 1 172.5 87.6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" opacity=".5"/></svg>
      <p class="ph-lab-txt"><em>Phitness</em> è un ‘laboratorio guidato’, un momento che puoi organizzare per la tua comunità.<br>È un percorso di un’ora, diviso in tre momenti, per condividere il gusto di <strong>pensare assieme</strong>, <strong>leggere con calma</strong> e <strong>scrivere i propri pensieri</strong>.</p>
    </div>
  </section>

  <div class="ph-rooms-head wrap"><span class="eyebrow">Il metodo</span><h2>Un tema.<br class="ph-mbr"> Tre passioni.<br class="ph-mbr"> Tre esercizi.</h2></div>

  <section class="ph-room ph-room--pensare" id="pensare">
    <figure class="ph-room-img"><img src="<?php echo esc_url( AB_IMG ); ?>phit-rembrandt.jpg" alt="Rembrandt, Filosofo in meditazione: un vecchio seduto accanto a una finestra luminosa, in una stanza in penombra con una scala a chiocciola" loading="lazy"></figure>
    <div class="ph-room-txt">
      <span class="ph-num">1</span>
      <h3>Pensare</h3>
      <p>Un problema della storia della filosofia, presentato in modo chiaro e discusso insieme. È il momento in cui si parla: si chiede, si obietta, si cerca un esempio. Pensare insieme a qualcuno è uno dei piaceri più antichi.</p>
      <p class="ph-credit">Rembrandt, <em>Filosofo in meditazione</em>, 1632 · Musée du Louvre, Parigi<br>Immagine: <a href="https://commons.wikimedia.org/wiki/File:Rembrandt_-_The_Philosopher_in_Meditation_(cleaned).jpg">Wikimedia Commons, pubblico dominio</a></p>
    </div>
  </section>

  <section class="ph-room ph-room--leggere" id="leggere">
    <figure class="ph-room-img"><img src="<?php echo esc_url( AB_IMG ); ?>phit-fragonard.jpg" alt="Fragonard, La lettrice: una giovane in abito giallo legge un piccolo libro, appoggiata a un cuscino" loading="lazy"></figure>
    <div class="ph-room-txt">
      <span class="ph-num">2</span>
      <h3>Leggere</h3>
      <p>Uno o più testi collegati al tema discusso, letti in silenzio, ognuno con il proprio ritmo. Concentrarsi sulle parole per pe(n)sarne il significato e abitare per un po' le parole di un altro.</p>
      <p class="ph-credit">Jean-Honoré Fragonard, <em>La lettrice</em>, 1769 circa · National Gallery of Art, Washington<br>Immagine: <a href="https://commons.wikimedia.org/wiki/File:Jean_Honor%C3%A9_Fragonard,_Young_Girl_Reading,_c._1769,_NGA_46303.jpg">Wikimedia Commons, CC0</a></p>
    </div>
  </section>

  <section class="ph-room ph-room--scrivere" id="scrivere">
    <figure class="ph-room-img"><img src="<?php echo esc_url( AB_IMG ); ?>phit-vermeer.jpg" alt="Vermeer, Donna che scrive una lettera: una giovane in giacca gialla scrive a un tavolo coperto da un panno blu e alza lo sguardo" loading="lazy"></figure>
    <div class="ph-room-txt">
      <span class="ph-num">3</span>
      <h3>Scrivere</h3>
      <p>Una traccia su un argomento collegato al tema, da scrivere a penna o sul proprio dispositivo. Non per consegnare un compito, ma per scoprire che cosa si pensa. Chi vuole, alla fine, lascia il suo testo in forma anonima.</p>
      <p class="ph-credit">Johannes Vermeer, <em>Donna che scrive una lettera</em>, 1665 circa · National Gallery of Art, Washington<br>Immagine: <a href="https://commons.wikimedia.org/wiki/File:Johannes_Vermeer,_A_Lady_Writing,_c._1665,_NGA_46437.jpg">Wikimedia Commons, CC0</a></p>
    </div>
  </section>

  <section class="ph-statement">
    <div class="wrap ph-statement-in">
      <div class="ph-zero">
        <svg class="ph-enso" viewBox="0 0 200 200" aria-hidden="true"><path d="M150 52 C 128 28, 78 24, 50 52 C 22 80, 26 132, 58 156 C 92 181, 146 172, 166 136 C 180 110, 176 82, 162 64" fill="none" stroke="currentColor" stroke-width="7" stroke-linecap="round"/><path d="M150 52 C 128 28, 78 24, 50 52 C 22 80, 26 132, 58 156" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" opacity=".55" transform="translate(-3 2)"/></svg>
        <p class="pull">Zero performance, <em>solo esercizio.</em></p>
      </div>
      <p class="prose">Nessuno viene interrogato, nessuno deve pensare più rapidamente degli altri, leggere più in fretta o scrivere meglio. <em>Phitness</em> non è una gara né una valutazione.</p>
    </div>
  </section>

  <section class="block tint">
    <div class="wrap">
      <?php ab_lessons_carousel(); ?>
    </div>
  </section>

  <section class="block">
    <div class="wrap split" style="align-items:start">
      <div class="head" style="margin:0"><span class="eyebrow">Un incontro</span><h2>Come si svolge un incontro, dall'inizio alla fine</h2></div>
      <ol class="timeline">
        <li><span class="dot"></span><div><strong>Accoglienza</strong><span>Si spiega che cosa accadrà e perché. Si spengono le notifiche.</span></div></li>
        <li><span class="dot"></span><div><strong>Pensare</strong><span>Il problema del giorno, presentato senza tecnicismi. Qui si parla, si chiede, si discute.</span></div></li>
        <li><span class="dot"></span><div><strong>Leggere</strong><span>I testi, in silenzio, ognuno con il proprio ritmo.</span></div></li>
        <li><span class="dot"></span><div><strong>Scrivere</strong><span>A penna o sul proprio dispositivo, su un argomento proposto al momento.</span></div></li>
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


  <section class="block tint" id="richiesta">
    <div class="wrap split">
      <div class="head" style="margin:0">
        <span class="eyebrow">Contatti</span>
        <h2>Vuoi portare <em>Phitness</em> dove vivi, studi o lavori?</h2>
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
