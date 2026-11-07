<?php
/**
 * Post Scriptum: archivio degli articoli del sito (non pubblicizzato).
 *
 * @package armando-bisogno
 */

get_header();
$paged = max( 1, (int) get_query_var( 'paged' ) );
$q     = new WP_Query(
	array(
		'post_type'      => 'post',
		'posts_per_page' => 20,
		'paged'          => $paged,
	)
);
?>
<main id="main">
	<div class="wrap">
		<div class="article">
			<span class="eyebrow">Archivio</span>
			<h1 style="margin-top:12px">Post Scriptum</h1>
			<p class="lead" style="margin-top:14px">Appunti, riflessioni e materiali scritti nel tempo.</p>
			<ul class="posts" style="margin-top:32px">
				<?php while ( $q->have_posts() ) : $q->the_post(); ?>
					<li><a href="<?php the_permalink(); ?>"><h3><?php the_title(); ?></h3><span><?php echo esc_html( mb_strtolower( get_the_date( 'j F Y' ) ) ); ?></span></a></li>
				<?php endwhile; wp_reset_postdata(); ?>
			</ul>
			<?php
			$links = paginate_links(
				array(
					'total'   => $q->max_num_pages,
					'current' => $paged,
					'type'    => 'array',
				)
			);
			if ( $links ) {
				echo '<nav class="pager">' . wp_kses_post( implode( '', $links ) ) . '</nav>';
			}
			?>
		</div>
	</div>
</main>
<?php
get_footer();
