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
      <div class="hero home">
        <div>
          <h1>Usare la filosofia per capire <em>il presente</em></h1>
          <p class="lead">Insegno Storia della filosofia medievale e studio Agostino da trent'anni. Scrivo di intelligenza artificiale, racconto storie di provincia e porto la filosofia fuori dall'aula. Sono da sempre appassionato di tecnologia, musica, chitarra, letteratura, videogiochi, scacchi. E molto altro.</p>
        </div>
        <figure class="cutout">
          <img src="<?php echo esc_url( AB_IMG ); ?>armando-cutout.png" alt="Ritratto di Armando Bisogno">
        </figure>
      </div>
    </div>
  </div>

  <section class="quote-band">
    <div class="wrap quote-line">
      <span class="mark" aria-hidden="true">“</span>
      <p>È presto giorno, ancora uno. Fa' ciò che puoi.</p>
      <span class="who">Czesław Miłosz</span>
    </div>
  </section>

  <section class="block">
    <div class="wrap">
      <div class="head"><span class="eyebrow">Che cosa faccio</span><h2>Un metodo, molti luoghi</h2></div>
      <div class="paths">
        <a class="path p-ricerca" href="<?php echo esc_url( ab_url( 'ricerca' ) ); ?>"><span class="chip">Ricerca</span><h3>Agostino e il Medioevo</h3><p>Cinque libri sul pensiero tardoantico e altomedievale e un manifesto per le Humanities di oggi.</p><span class="more">Scopri la ricerca →</span></a>
        <a class="path p-ia" href="<?php echo esc_url( ab_url( 'ia-e-nuove-tecnologie' ) ); ?>"><span class="chip">IA e nuove tecnologie</span><h3>Le macchine, lette da un umanista</h3><p>La newsletter <em>Macchine Pensanti</em>, il podcast <em>Macchine Parlanti</em>, il libro <em>Una intelligenza fantastica</em>.</p><span class="more">Leggi e ascolta →</span></a>
        <a class="path p-romanzi" href="<?php echo esc_url( ab_url( 'romanzi' ) ); ?>"><span class="chip warm">Romanzi</span><h3>Il commissario Malversi</h3><p><em>Terapie</em> e <em>Mosaici</em>, due gialli pubblicati da De Tomi.</p><span class="more">Scopri i romanzi →</span></a>
        <a class="path p-phitness" href="<?php echo esc_url( ab_url( 'phitness' ) ); ?>"><span class="chip chip-phit"><?php echo ab_phitness_mark( 16 ); // SVG statico. ?>Phitness</span><h3>Filosofia per aziende e comunità</h3><p>Un laboratorio per allenarsi a concentrarsi, leggere con attenzione, scrivere con metodo.</p><span class="more">Come funziona →</span></a>
      </div>
    </div>
  </section>


  <section class="block tint">
    <div class="wrap">
      <div class="head"><span class="eyebrow">Ultime uscite</span><h2>Da leggere e ascoltare</h2></div>
      <?php ab_latest_feed(); ?>
    </div>
  </section>
</main>
<?php
get_footer();
