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
      <div class="hero solo">
        <div>
          <span class="eyebrow">Ricerca</span>
          <h1>Leggere il Medioevo, ripensare <em>le Humanities</em></h1>
          <p class="lead">Dalla tesi sul libero arbitrio in Giovanni Scoto al dottorato sull'età carolingia, fino ad Agostino. Sullo sfondo, la filosofia del linguaggio, il rapporto tra politica, religione e filosofia, quello tra discipline umanistiche e mondo contemporaneo.</p>
        </div>
      </div>
    </div>
  </div>

  <section class="block">
    <div class="wrap">
      <div class="head"><span class="eyebrow">Monografie</span><h2>Cinque libri sul Medioevo</h2></div>
      <ol class="shelf">
        <li class="book"><div class="cover"><span class="book3d"><img src="<?php echo esc_url( AB_IMG ); ?>libro-carolingio.png" alt="Copertina de Il metodo carolingio"></span></div><span class="yr">2008</span><h3>Il metodo carolingio</h3><p>I filosofi e i teologi delle corti carolinge pensati come un unico pensatore, con un'unità di intenzione e di metodo.</p><a class="pub" href="https://www.brepols.net/products/IS-9782503528625-1">Brepols · Nutrix →</a></li>
        <li class="book"><div class="cover"><span class="book3d"><img src="<?php echo esc_url( AB_IMG ); ?>libro-sententiae.png" alt="Copertina di Sententiae philosophorum"></span></div><span class="yr">2011</span><h3>Sententiae philosophorum</h3><p>Che cos'è la storia della filosofia? Perché gli altomedievali leggevano i pensatori del passato, e con quale metodo.</p><a class="pub" href="https://edizionicittanuova.it/autori/armando-bisogno/">Città Nuova · Collationes →</a></li>
        <li class="book"><div class="cover"><span class="book3d"><img src="<?php echo esc_url( AB_IMG ); ?>libro-demagistro.png" alt="Copertina de Il De magistro di Agostino"></span></div><span class="yr">2014</span><h3>Il De magistro di Agostino</h3><p>Traduzione commentata. Quanto le parole servono a farsi capire, e quanto diventano un ostacolo.</p><a class="pub" href="https://edizionicittanuova.it/autori/armando-bisogno/">Città Nuova · Traditiones →</a></li>
        <li class="book"><div class="cover"><span class="book3d"><img src="<?php echo esc_url( AB_IMG ); ?>libro-eterno.png" alt="Copertina de L'eterno assente"></span></div><span class="yr">2021</span><h3>L'eterno assente</h3><p>Il percorso intellettuale di Agostino letto come una ricerca della verità.</p><a class="pub" href="https://edizionicittanuova.it/autori/armando-bisogno/">Città Nuova · Institutiones →</a></li>
        <li class="book"><div class="cover"><span class="book3d"><img src="<?php echo esc_url( AB_IMG ); ?>cover-fragile.jpg" alt="Copertina de Il racconto fragile"></span></div><span class="chip">Accesso aperto</span><h3>Il racconto fragile</h3><p>Le <em>Confessioni</em> come racconto di una fragilità esposta. Una versione più breve, in attesa della versione più ampia, che uscirà nel 2027, anch'essa ad accesso aperto.</p><a class="pub" style="font-weight:600;color:var(--accent-ink)" href="https://doi.org/10.5281/zenodo.17847701">Scaricalo gratis su Zenodo →</a></li>
      </ol>
    </div>
  </section>

  <section class="block band">
    <div class="wrap split">
      <div>
        <div class="head" style="margin-bottom:22px"><span class="eyebrow">Ermenetica</span><h2>Un manifesto per le Humanities di oggi</h2></div>
        <div class="prose">
          <p><em>Ermenetica</em> è un neologismo: ermeneutica più etica. Oggi chi si occupa di discipline umanistiche non può interpretare senza assumersi una responsabilità.</p>
          <p>Il nostro tempo ha bisogno di sguardi umanistici, purché chi li offre non si nasconda dietro la presunta oggettività dei numeri e rivendichi il proprio ruolo di interprete posizionato, con la sua storia intellettuale e culturale.</p>
        </div>
        <div class="actions" style="margin-top:26px"><a class="btn btn-light" href="https://doi.org/10.5281/zenodo.17997307">Scaricalo gratis su Zenodo</a></div>
      </div>
      <div class="feature-book"><span class="book3d"><img src="<?php echo esc_url( AB_IMG ); ?>cover-ermenetica.jpg" alt="Copertina di Ermenetica. Il sapere umanistico come esercizio di responsabilità"></span></div>
    </div>
  </section>
</main>
<?php
get_footer();
