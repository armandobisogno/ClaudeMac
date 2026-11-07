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
          <span class="eyebrow">Scrittura · I romanzi</span>
          <h1>I gialli del commissario <em>Malversi</em></h1>
          <p class="lead"><em>Terapie</em> e <em>Mosaici</em> sono due romanzi ambientati a Fossa Etrusca, città immaginaria di provincia. Le indagini di Malversi passano attraverso le pagine di un diario terapeutico, tra istituzioni, tracce e blues.</p>
          <div class="actions"><a class="btn btn-primary" href="https://detomieditore.it/products/terapie-mosaici-collezione">Acquista su De Tomi</a></div>
        </div>
        <div class="feature-book mock"><img src="<?php echo esc_url( AB_IMG ); ?>libro-romanzi.png" alt="Mockup dei romanzi Terapie e Mosaici"></div>
      </div>
    </div>
  </div>
</main>
<?php
get_footer();
