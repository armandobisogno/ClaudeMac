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
          <span class="eyebrow">IA e nuove tecnologie</span>
          <h1>Le macchine, lette <em>da un umanista</em></h1>
          <p class="lead">Una newsletter, un podcast e un libro aperto. Tre modi di fare la stessa cosa: leggere le nuove tecnologie con gli strumenti delle Humanities.</p>
        </div>
      </div>
    </div>
  </div>

  <section class="block">
    <div class="wrap">
      <div class="cards" style="grid-template-columns:repeat(auto-fit,minmax(17rem,1fr))">
        <div class="media-card"><div class="img" style="background:#FFFFFF"><img src="<?php echo esc_url( AB_IMG ); ?>logo-mp.png" alt="Logo di Macchine Pensanti"></div><div class="txt"><span class="chip">Newsletter</span><h3>Macchine Pensanti</h3><p>Una lettura umanistica delle nuove tecnologie e in particolare dell'intelligenza artificiale.</p><a class="more" href="https://armandobisogno.substack.com">Iscriviti su Substack →</a></div></div>
        <div class="media-card"><div class="img" style="background:#FB6D1B;padding:0"><img src="<?php echo esc_url( AB_IMG ); ?>logo-mparl.jpg" alt="Copertina di Macchine Parlanti"></div><div class="txt"><span class="chip warm">Micropodcast</span><h3>Macchine Parlanti</h3><p>Puntate brevi sulle nuove tecnologie e sulla cultura contemporanea.</p><a class="more" href="https://macchineparlanti.substack.com/">Ascolta →</a></div></div>
        <div class="media-card"><div class="img"><img src="<?php echo esc_url( AB_IMG ); ?>libro-uif.png" alt="Mockup di Una intelligenza fantastica"></div><div class="txt"><span class="chip">Libro aperto</span><h3>Una intelligenza fantastica</h3><p>Otto riflessioni aperte sull'intelligenza artificiale, lette con gli occhi di uno studioso di filosofia. Un libro che cresce con gli inviti delle comunità che vogliono discuterne.</p><a class="more" href="https://www.armandobisogno.it/una-intelligenza-fantastica/">Scaricalo gratis →</a></div></div>
      </div>
    </div>
  </section>
  <section class="block tint">
    <div class="wrap">
      <div class="head"><span class="eyebrow">Interviste</span><h2>Due conversazioni con Raffaele Gaito</h2><p class="lead">Sul canale YouTube di Raffaele Gaito, a proposito di creatività, scrittura e intelligenza artificiale.</p></div>
      <div class="videos">
        <figure class="video-card">
          <button class="yt-facade" type="button" data-yt="vSJJ7Qz-0Ok" aria-label="Guarda il video: Se l'IA può replicare la nostra creatività, cosa ci rimane?">
            <img src="<?php echo esc_url( AB_IMG ); ?>yt-vSJJ7Qz-0Ok.jpg" alt="" loading="lazy">
            <span class="yt-play" aria-hidden="true"></span>
          </button>
          <figcaption><span class="chip">Intervista 1</span><h3>Se l'IA può replicare la nostra creatività, che cosa ci rimane?</h3></figcaption>
        </figure>
        <figure class="video-card">
          <button class="yt-facade" type="button" data-yt="4VpAuIZK5Rg" aria-label="Guarda il video: Verificare se un testo è umano è inutile">
            <img src="<?php echo esc_url( AB_IMG ); ?>yt-4VpAuIZK5Rg.jpg" alt="" loading="lazy">
            <span class="yt-play" aria-hidden="true"></span>
          </button>
          <figcaption><span class="chip">Intervista 2</span><h3>Verificare se un testo è umano è inutile</h3></figcaption>
        </figure>
      </div>
      <p class="note" style="margin-top:16px">Il video si carica da YouTube solo quando premi play.</p>
    </div>
  </section>
</main>
<?php
get_footer();
