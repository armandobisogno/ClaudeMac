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
          <span class="eyebrow">Profilo e contatti</span>
          <h1>Studioso, docente, <em>life addicted</em></h1>
          <div class="prose muted">
            <p>Laurea in Storia della filosofia medievale all'Università di Napoli Federico II, con Valeria Sorge, sul libero arbitrio in Giovanni Scoto. Dottorato all'Università di Salerno con Giulio d'Onofrio, sull'età carolingia.</p>
            <p>Oggi insegno Storia della filosofia medievale all'Università di Salerno, dove sono anche Direttore del Dipartimento di Scienze del Patrimonio Culturale.</p>
          </div>
        </div>
        <figure class="cutout">
          <img src="<?php echo esc_url( AB_IMG ); ?>armando-cutout.png" alt="Ritratto di Armando Bisogno">
        </figure>
      </div>
    </div>
  </div>
  <section class="block band" id="contatti">
    <div class="wrap split">
      <div class="head" style="margin:0"><span class="eyebrow">Contatti</span><h2>Inviti, conferenze, collaborazioni</h2></div>
      <div>
        <p style="font-family:var(--display);font-size:clamp(26px,3.4vw,38px);color:var(--on-band)">arbisogno@unisa.it</p>
        <div style="margin-top:14px"><span class="eyebrow" style="display:block;margin-bottom:10px">Mi trovi anche qui</span><?php ab_social_links( 'on-dark' ); ?></div>
        <div class="formbox" style="margin-top:22px;color:var(--ink)">
          <h3 style="font-size:24px;color:var(--ink)">Scrivimi da qui</h3>
          <?php ab_contact_form( 'contatti' ); ?>
        </div>
      </div>
    </div>
  </section>
</main>
<?php
get_footer();
