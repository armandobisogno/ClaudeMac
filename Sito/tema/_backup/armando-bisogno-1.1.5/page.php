<?php
/**
 * Pagina generica (per le pagine che non hanno un template dedicato).
 *
 * @package armando-bisogno
 */

get_header();
?>
<main id="main">
	<div class="wrap">
		<?php while ( have_posts() ) : the_post(); ?>
			<article class="article">
				<h1><?php the_title(); ?></h1>
				<div class="entry"><?php the_content(); ?></div>
			</article>
		<?php endwhile; ?>
	</div>
</main>
<?php
get_footer();
