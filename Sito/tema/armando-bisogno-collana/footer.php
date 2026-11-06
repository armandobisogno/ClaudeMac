<?php
/**
 * Piè di pagina.
 *
 * @package armando-bisogno
 */

?>
<footer>
	<div class="wrap">
		<div><h4>Armando Bisogno</h4><p><?php echo esc_html( AB_EMAIL ); ?></p><?php ab_social_links( 'on-dark' ); ?></div>
		<div><h4>Sezioni</h4><ul>
			<?php
			foreach ( ab_sections() as $s ) {
				printf( '<li><a href="%s">%s</a></li>', esc_url( ab_url( $s[0] ) ), esc_html( $s[1] ) );
			}
			?>
		</ul></div>
		<div><h4>Archivio</h4><ul><li><a href="<?php echo esc_url( ab_url( 'post-scriptum' ) ); ?>">Post Scriptum</a></li><li><a href="<?php echo esc_url( home_url( '/rassegna/' ) ); ?>">Rassegna stampa</a></li></ul></div>
	</div>
</footer>
<script>
(function(){var h=document.querySelector('header.site'),b=h&&h.querySelector('.menu-btn');if(!b)return;
b.addEventListener('click',function(){var o=h.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});})();
document.querySelectorAll('[data-carousel]').forEach(function(c){var tr=c.querySelector('.lessons-track');c.querySelectorAll('.lessons-btn').forEach(function(b){b.addEventListener('click',function(){var card=tr.querySelector('.lesson');var step=card?card.getBoundingClientRect().width+22:320;tr.scrollBy({left:step*parseInt(b.dataset.dir,10),behavior:'smooth'});});});});
document.addEventListener('click',function(e){var y=e.target.closest('.yt-facade');if(!y)return;var f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+y.dataset.yt+'?autoplay=1&rel=0';f.title=y.getAttribute('aria-label')||'Video';f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';f.allowFullscreen=true;f.referrerPolicy='strict-origin-when-cross-origin';y.replaceWith(f);});
</script>
<?php wp_footer(); ?>
</body>
</html>
