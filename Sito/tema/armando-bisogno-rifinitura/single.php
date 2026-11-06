<?php
/**
 * Articolo singolo (Post Scriptum).
 *
 * @package armando-bisogno
 */

get_header();
?>
<main id="main">
	<div class="wrap">
		<?php while ( have_posts() ) : the_post(); ?>
			<article class="article">
				<span class="eyebrow">Post Scriptum</span>
				<h1 style="margin-top:12px"><?php the_title(); ?></h1>
				<p class="meta"><?php echo esc_html( mb_strtolower( get_the_date( 'j F Y' ) ) ); ?></p>
				<div class="entry"><?php the_content(); ?></div>
				<a class="back" href="<?php echo esc_url( ab_url( 'post-scriptum' ) ); ?>">← Tutti i Post Scriptum</a>
			</article>
		<?php endwhile; ?>
	</div>
</main>
<?php
get_footer();
