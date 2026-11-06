<?php
/**
 * Pagina non trovata.
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
					<span class="eyebrow">Errore 404</span>
					<h1>Questa pagina <em>non c'è</em></h1>
					<p class="lead">Forse è stata spostata durante il rinnovo del sito.</p>
					<div class="actions"><a class="btn btn-primary" href="<?php echo esc_url( home_url( '/' ) ); ?>">Torna alla home</a></div>
				</div>
			</div>
		</div>
	</div>
</main>
<?php
get_footer();
