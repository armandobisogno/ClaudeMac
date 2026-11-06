<?php
/**
 * Una intelligenza fantastica: il libro aperto sull'IA.
 *
 * Le versioni arrivano dal Foglio Google «Versioni UIF» (vedi ab_uif_versions()).
 *
 * @package armando-bisogno
 */

get_header();
$versions = ab_uif_versions();
$current  = $versions ? end( $versions ) : null;
?>
<main id="main">
  <div class="hero-band">
    <div class="wrap">
      <div class="hero">
        <div>
          <span class="eyebrow">IA e nuove tecnologie · Libro aperto</span>
          <h1>Una intelligenza <em>fantastica</em></h1>
          <p class="lead">Otto riflessioni aperte sull'intelligenza artificiale, lette con gli occhi di uno studioso di filosofia. Gratuite, in PDF ed ePub.</p>
          <div class="actions">
            <a class="btn btn-primary" href="<?php echo esc_url( home_url( '/download/1909/' ) ); ?>">Scarica il PDF</a>
            <a class="btn btn-ghost" href="<?php echo esc_url( home_url( '/download/1917/' ) ); ?>">Scarica l'ePub</a>
            <a class="btn btn-ghost" href="https://amzn.eu/d/0cGFh5Lr">Copia cartacea su Amazon</a>
          </div>
          <?php if ( $current ) : ?>
            <p class="note" style="margin-top:16px">Versione <?php echo esc_html( $current['versione'] ); ?> · <?php echo esc_html( $current['data'] ); ?></p>
          <?php endif; ?>
        </div>
        <div class="feature-book mock"><img src="<?php echo esc_url( AB_IMG ); ?>libro-uif.png" alt="Copertina di Una intelligenza fantastica"></div>
      </div>
    </div>
  </div>

  <section class="block">
    <div class="wrap">
      <div class="cards" style="grid-template-columns:repeat(auto-fit,minmax(19rem,1fr))">
        <div class="card" style="background:var(--paper-2)">
          <span class="chip">Riflessioni in costruzione</span>
          <h3>Un libro aperto</h3>
          <p>Un orizzonte così vasto e complesso come l'IA non si può analizzare in modo definitivo. Ogni riflessione è un tentativo di mettere in ordine le idee che oggi riusciamo a condensare attorno a questo tema, sapendo che domani saranno già incomplete. Per questo <em>Una intelligenza fantastica</em> è un libro aperto: l'inizio di un percorso che si arricchisce con il tempo, anche grazie alle riflessioni che susciterà.</p>
        </div>
        <div class="card" style="background:var(--paper-2)">
          <span class="chip warm">Riflessioni da condividere</span>
          <h3>Un invito a essere invitato</h3>
          <p><em>Una intelligenza fantastica</em> nasce come il manifesto della mia disponibilità a ragionare di questi temi con le comunità che avranno il piacere di invitarmi: scuole, associazioni, aziende, biblioteche.</p>
          <a class="more" style="font-weight:600;color:var(--accent-ink);text-decoration:none;margin-top:auto" href="<?php echo esc_url( ab_url( 'profilo' ) ); ?>#contatti">Invitami a parlarne →</a>
        </div>
      </div>
    </div>
  </section>

  <?php if ( $versions ) : ?>
  <section class="block tint">
    <div class="wrap">
      <div class="head"><span class="eyebrow">Versioni</span><h2>Come cambia il libro</h2><p class="lead">Ogni nuova versione sostituisce la precedente nei file da scaricare.</p></div>
      <div class="versions">
        <table>
          <thead><tr><th>Versione</th><th>Pubblicata</th><th>Che cosa cambia</th></tr></thead>
          <tbody>
          <?php foreach ( array_reverse( $versions ) as $i => $v ) : ?>
            <tr<?php echo 0 === $i ? ' class="current"' : ''; ?>><td><strong><?php echo esc_html( $v['versione'] ); ?></strong></td><td><?php echo esc_html( $v['data'] ); ?></td><td><?php echo esc_html( $v['note'] ); ?></td></tr>
          <?php endforeach; ?>
          </tbody>
        </table>
      </div>
    </div>
  </section>
  <?php endif; ?>
</main>
<?php
get_footer();
