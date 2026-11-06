<?php
/**
 * Intestazione.
 *
 * @package armando-bisogno
 */

?><!doctype html>
<html <?php language_attributes(); ?>>
<head>
<meta charset="<?php bloginfo( 'charset' ); ?>">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#4F7CB6">
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="skip" href="#main">Vai al contenuto</a>
<header class="site">
	<div class="wrap">
		<a class="brand" href="<?php echo esc_url( home_url( '/' ) ); ?>">Armando <span>Bisogno</span></a>
		<button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu-principale"><span class="bars" aria-hidden="true"></span>Menu</button>
		<nav class="main" id="menu-principale" aria-label="Sezioni">
			<?php
			foreach ( ab_sections() as $s ) {
				$current = is_page( $s[0] ) ? ' aria-current="page"' : '';
				printf( '<a href="%s"%s>%s</a>', esc_url( ab_url( $s[0] ) ), $current, esc_html( $s[1] ) );
			}
			?>
		</nav>
	</div>
</header>
