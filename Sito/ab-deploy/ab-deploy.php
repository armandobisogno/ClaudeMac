<?php
/**
 * Plugin Name: Armando Deploy
 * Description: Permette di installare/aggiornare temi e plugin e di attivare un tema via REST, autenticandosi con una password applicazione da amministratore. Nessuna interfaccia: serve solo agli aggiornamenti fatti da Claude.
 * Version: 1.2.0
 * Requires at least: 6.0
 * Requires PHP: 7.4
 * Author: Armando Bisogno
 *
 * @package ab-deploy
 */

defined( 'ABSPATH' ) || exit;

/*
 * Anteprima privata di un tema: chi apre il sito con ?ab_preview=CHIAVE vede il tema
 * indicato (un cookie la mantiene durante la navigazione). I visitatori normali non
 * vedono nulla di diverso. La chiave scade da sola.
 */
( function () {
	$cfg = get_option( 'ab_deploy_preview' );
	if ( ! is_array( $cfg ) || empty( $cfg['key'] ) || empty( $cfg['theme'] ) || time() > (int) $cfg['expires'] ) {
		return;
	}
	$given = '';
	if ( isset( $_GET['ab_preview'] ) ) {
		$given = sanitize_text_field( wp_unslash( $_GET['ab_preview'] ) );
	} elseif ( isset( $_COOKIE['ab_preview'] ) ) {
		$given = sanitize_text_field( wp_unslash( $_COOKIE['ab_preview'] ) );
	}
	if ( '' === $given || ! hash_equals( $cfg['key'], $given ) ) {
		return;
	}
	if ( isset( $_GET['ab_preview'] ) && ! headers_sent() ) {
		setcookie( 'ab_preview', $given, (int) $cfg['expires'], COOKIEPATH ? COOKIEPATH : '/', COOKIE_DOMAIN, is_ssl(), true );
	}
	if ( ! headers_sent() ) {
		header( 'Cache-Control: no-store, private' );
		header( 'X-Robots-Tag: noindex' );
	}
	$theme = $cfg['theme'];
	add_filter( 'pre_option_stylesheet', fn() => $theme );
	add_filter( 'pre_option_template', fn() => $theme );
} )();

add_action(
	'rest_api_init',
	function () {
		$ns = 'ab-deploy/v1';

		register_rest_route(
			$ns,
			'/status',
			array(
				'methods'             => 'GET',
				'permission_callback' => fn() => current_user_can( 'switch_themes' ),
				'callback'            => function () {
					$t = wp_get_theme();
					if ( ! function_exists( 'get_plugins' ) ) {
						require_once ABSPATH . 'wp-admin/includes/plugin.php';
					}
					$plugins = array();
					foreach ( get_plugins() as $file => $p ) {
						$plugins[] = array(
							'file'    => $file,
							'name'    => $p['Name'],
							'version' => $p['Version'],
							'active'  => is_plugin_active( $file ),
						);
					}
					return array(
						'wp'       => get_bloginfo( 'version' ),
						'php'      => PHP_VERSION,
						'theme'    => array( 'stylesheet' => $t->get_stylesheet(), 'name' => $t->get( 'Name' ), 'version' => $t->get( 'Version' ) ),
						'themes'   => array_keys( wp_get_themes() ),
						'plugins'  => $plugins,
						'front'    => array( 'show_on_front' => get_option( 'show_on_front' ), 'page_on_front' => (int) get_option( 'page_on_front' ) ),
					);
				},
			)
		);

		// Installa o sovrascrive un tema o un plugin da uno zip (campo "package", parametro "type" = theme|plugin).
		register_rest_route(
			$ns,
			'/package',
			array(
				'methods'             => 'POST',
				'permission_callback' => function ( WP_REST_Request $r ) {
					return 'plugin' === $r->get_param( 'type' ) ? current_user_can( 'install_plugins' ) : current_user_can( 'install_themes' );
				},
				'callback'            => function ( WP_REST_Request $r ) {
					$files = $r->get_file_params();
					if ( empty( $files['package']['tmp_name'] ) ) {
						return new WP_Error( 'no_file', 'Manca il file zip (campo "package").', array( 'status' => 400 ) );
					}
					require_once ABSPATH . 'wp-admin/includes/file.php';
					require_once ABSPATH . 'wp-admin/includes/class-wp-upgrader.php';
					require_once ABSPATH . 'wp-admin/includes/misc.php';
					WP_Filesystem();
					$tmp = wp_tempnam( 'ab-deploy.zip' );
					if ( ! @move_uploaded_file( $files['package']['tmp_name'], $tmp ) && ! @copy( $files['package']['tmp_name'], $tmp ) ) {
						return new WP_Error( 'move', 'Impossibile salvare lo zip sul server.', array( 'status' => 500 ) );
					}
					$skin     = new WP_Ajax_Upgrader_Skin();
					$is_plugin = ( 'plugin' === $r->get_param( 'type' ) );
					$upgrader = $is_plugin ? new Plugin_Upgrader( $skin ) : new Theme_Upgrader( $skin );
					$result   = $upgrader->install( $tmp, array( 'overwrite_package' => true ) );
					@unlink( $tmp );
					if ( is_wp_error( $result ) || ! $result ) {
						$err = is_wp_error( $result ) ? $result : $skin->get_errors();
						return new WP_Error( 'install', is_wp_error( $err ) ? $err->get_error_message() : 'Installazione non riuscita.', array( 'status' => 500, 'messages' => $skin->get_upgrade_messages() ) );
					}
					return array(
						'ok'       => true,
						'type'     => $is_plugin ? 'plugin' : 'theme',
						'result'   => $is_plugin ? $upgrader->plugin_info() : $upgrader->theme_info()->get_stylesheet(),
						'messages' => $skin->get_upgrade_messages(),
					);
				},
			)
		);

		// Crea (o rinnova) la chiave di anteprima per un tema installato. Valida 3 giorni.
		register_rest_route(
			$ns,
			'/preview',
			array(
				'methods'             => 'POST',
				'permission_callback' => fn() => current_user_can( 'switch_themes' ),
				'callback'            => function ( WP_REST_Request $r ) {
					$slug = sanitize_key( (string) $r->get_param( 'stylesheet' ) );
					if ( 'off' === $slug ) {
						delete_option( 'ab_deploy_preview' );
						return array( 'ok' => true, 'preview' => 'off' );
					}
					if ( ! wp_get_theme( $slug )->exists() ) {
						return new WP_Error( 'missing', 'Tema non trovato: ' . $slug, array( 'status' => 404 ) );
					}
					$key = wp_generate_password( 20, false, false );
					update_option( 'ab_deploy_preview', array( 'theme' => $slug, 'key' => $key, 'expires' => time() + 3 * DAY_IN_SECONDS ), false );
					return array( 'ok' => true, 'url' => add_query_arg( 'ab_preview', $key, home_url( '/' ) ) );
				},
			)
		);

		// Svuota tutta la cache di Aruba (plugin Aruba HiSpeed Cache), se presente.
		register_rest_route(
			$ns,
			'/purge',
			array(
				'methods'             => 'POST',
				'permission_callback' => fn() => current_user_can( 'manage_options' ),
				'callback'            => function () {
					if ( ! class_exists( '\\ArubaSPA\\HiSpeedCache\\Purger\\WpPurger' ) || ! defined( 'AHSC_PURGER' ) ) {
						wp_cache_flush();
						return array( 'ok' => true, 'aruba' => false );
					}
					$c = new \ArubaSPA\HiSpeedCache\Purger\WpPurger();
					$c->setPurger( AHSC_PURGER );
					$c->purgeAll();
					return array( 'ok' => true, 'aruba' => true );
				},
			)
		);

		// Attiva un tema già installato.
		register_rest_route(
			$ns,
			'/activate-theme',
			array(
				'methods'             => 'POST',
				'permission_callback' => fn() => current_user_can( 'switch_themes' ),
				'callback'            => function ( WP_REST_Request $r ) {
					$slug  = sanitize_key( (string) $r->get_param( 'stylesheet' ) );
					$theme = wp_get_theme( $slug );
					if ( ! $theme->exists() ) {
						return new WP_Error( 'missing', 'Tema non trovato: ' . $slug, array( 'status' => 404 ) );
					}
					switch_theme( $slug );
					delete_option( 'ab_deploy_preview' );
					return array( 'ok' => true, 'active' => wp_get_theme()->get_stylesheet() );
				},
			)
		);
	}
);
