<?php
/**
 * Elenco generico (archivi, categorie, ricerca).
 *
 * @package armando-bisogno
 */

get_header();
?>
<main id="main">
	<div class="wrap">
		<div class="article">
			<h1><?php echo esc_html( wp_strip_all_tags( get_the_archive_title() ) ); ?></h1>
			<ul class="posts" style="margin-top:32px">
				<?php while ( have_posts() ) : the_post(); ?>
					<li><a href="<?php the_permalink(); ?>"><h3><?php the_title(); ?></h3><span><?php echo esc_html( mb_strtolower( get_the_date( 'j F Y' ) ) ); ?></span></a></li>
				<?php endwhile; ?>
			</ul>
			<?php
			$links = paginate_links( array( 'type' => 'array' ) );
			if ( $links ) {
				echo '<nav class="pager">' . wp_kses_post( implode( '', $links ) ) . '</nav>';
			}
			?>
		</div>
	</div>
</main>
<?php
get_footer();
