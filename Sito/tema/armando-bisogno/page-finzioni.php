<?php
/**
 * Finzioni: raccolta di esperimenti scritti con Claude.
 * Pagina scura, nel colore delle copertine. I libri sono in ab_finzioni() (functions.php).
 *
 * @package armando-bisogno
 */

get_header();
$allowed = array( 'em' => array(), 'a' => array( 'href' => array() ) );
?>
<main id="main" class="fz">
  <section class="fz-hero">
    <div class="wrap">
      <span class="fz-kicker">Armando Bisogno · con Claude</span>
      <h1>Finzioni</h1>
      <p class="fz-lead">Finzioni è una raccolta di esperimenti e <em>divertissement</em> letterari e di ricerca: testi prodotti integralmente o in massima parte dall'IA. Un modo concreto per provare limiti e potenzialità di questo strumento.</p>
      <p class="fz-ast"><span aria-hidden="true">*</span> Ogni testo dichiara in una nota con l'asterisco quanto vi ha messo la macchina.</p>
    </div>
  </section>

  <section class="fz-catalogo" aria-label="Catalogo">
    <div class="wrap">
      <ol class="fz-list">
        <?php foreach ( ab_finzioni() as $i => $b ) : ?>
          <li class="fz-book">
            <a class="fz-cover" href="<?php echo esc_url( AB_FINZIONI . $b['links'][0][0] . '?v=' . AB_VERSION ); ?>" tabindex="-1" aria-hidden="true">
              <img src="<?php echo esc_url( AB_IMG . $b['img'] ); ?>" alt="" loading="<?php echo $i < 2 ? 'eager' : 'lazy'; ?>" width="640" height="960">
            </a>
            <div class="fz-txt">
              <span class="fz-num"><?php echo esc_html( $b['num'] ); ?></span>
              <h2><?php echo wp_kses( $b['titolo'], $allowed ); ?></h2>
              <p class="fz-sub"><?php echo wp_kses( $b['sottotitolo'], $allowed ); ?></p>
              <p class="fz-meta"><?php echo esc_html( $b['meta'] ); ?></p>
              <p><?php echo wp_kses( $b['testo'], $allowed ); ?></p>
              <ul class="fz-links">
                <?php foreach ( $b['links'] as $l ) : ?>
                  <li><a href="<?php echo esc_url( AB_FINZIONI . $l[0] . '?v=' . AB_VERSION ); ?>"><?php echo wp_kses( $l[1], $allowed ); ?> <span aria-hidden="true">→</span></a></li>
                <?php endforeach; ?>
              </ul>
            </div>
          </li>
        <?php endforeach; ?>
      </ol>
    </div>
  </section>
</main>
<?php
get_footer();
