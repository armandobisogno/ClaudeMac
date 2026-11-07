<?php
/**
 * Plugin Name: Rassegna
 * Description: Rassegna stampa personale su /rassegna. Riceve le edizioni via REST dalla routine cloud, le serve protette da password e non indicizzate.
 * Version: 1.0.0
 * Requires PHP: 7.4
 * Author: Armando Bisogno
 * License: GPL-2.0-or-later
 */

if (!defined('ABSPATH')) {
	exit;
}

const RASSEGNA_CPT = 'rassegna_ed';
const RASSEGNA_META = '_rassegna_html';
const RASSEGNA_COOKIE = 'rassegna_auth';
// Hash bcrypt della password iniziale della pagina. Si cambia da Impostazioni → Rassegna.
const RASSEGNA_DEFAULT_HASH = '$2y$10$bt0/hBlQMjrCf.pz8PDkq.l2/7t1EFLWdIxEBrCy2fjcQsfiUPP.O';

/* ---------- Registrazione ---------- */

function rassegna_register() {
	register_post_type(RASSEGNA_CPT, [
		'label'               => 'Rassegna',
		'labels'              => ['name' => 'Rassegna', 'singular_name' => 'Edizione'],
		'public'              => false,
		'publicly_queryable'  => false,
		'exclude_from_search' => true,
		'show_ui'             => true,
		'show_in_menu'        => true,
		'show_in_rest'        => false,
		'menu_icon'           => 'dashicons-media-document',
		'supports'            => ['title'],
	]);
	add_rewrite_rule('^rassegna/?$', 'index.php?rassegna_view=latest', 'top');
	add_rewrite_rule('^rassegna/archivio/?$', 'index.php?rassegna_view=archive', 'top');
	add_rewrite_rule('^rassegna/([a-z0-9-]+)/?$', 'index.php?rassegna_view=single&rassegna_slug=$matches[1]', 'top');
}
add_action('init', 'rassegna_register');

add_filter('query_vars', function ($vars) {
	$vars[] = 'rassegna_view';
	$vars[] = 'rassegna_slug';
	return $vars;
});

register_activation_hook(__FILE__, function () {
	rassegna_register();
	flush_rewrite_rules();
	add_option('rassegna_pass_hash', RASSEGNA_DEFAULT_HASH, '', false);
	add_option('rassegna_publisher', 'rassegna', '', false);
});
register_deactivation_hook(__FILE__, 'flush_rewrite_rules');

/* ---------- REST: la routine pubblica e rilegge ---------- */

function rassegna_can_publish() {
	$u = wp_get_current_user();
	if (!$u || !$u->exists()) {
		return false;
	}
	return $u->user_login === get_option('rassegna_publisher', 'rassegna') || current_user_can('manage_options');
}

add_action('rest_api_init', function () {
	register_rest_route('rassegna/v1', '/edizioni', [
		'methods'             => 'POST',
		'callback'            => 'rassegna_rest_save',
		'permission_callback' => 'rassegna_can_publish',
		'args'                => [
			'slug'   => ['required' => true, 'type' => 'string', 'pattern' => '^[a-z0-9-]{3,80}$'],
			'titolo' => ['required' => true, 'type' => 'string'],
			'html'   => ['required' => true, 'type' => 'string'],
		],
	]);
	register_rest_route('rassegna/v1', '/edizioni/ultima', [
		'methods'             => 'GET',
		'callback'            => 'rassegna_rest_last',
		'permission_callback' => 'rassegna_can_publish',
	]);
});

function rassegna_rest_save(WP_REST_Request $r) {
	$slug = $r['slug'];
	$html = (string) $r['html'];
	if (strlen($html) > 3 * 1024 * 1024) {
		return new WP_Error('troppo_grande', 'HTML oltre 3 MB.', ['status' => 413]);
	}
	if (stripos(ltrim($html), '<!doctype html') !== 0) {
		return new WP_Error('html_non_valido', 'Serve un documento HTML completo che inizi con <!doctype html>.', ['status' => 400]);
	}
	$post = [
		'post_type'   => RASSEGNA_CPT,
		'post_status' => 'publish',
		'post_title'  => sanitize_text_field($r['titolo']),
		'post_name'   => $slug,
	];
	$existing = get_page_by_path($slug, OBJECT, RASSEGNA_CPT);
	if ($existing) {
		$post['ID'] = $existing->ID;
		$id = wp_update_post($post, true);
	} else {
		$id = wp_insert_post($post, true);
	}
	if (is_wp_error($id)) {
		return $id;
	}
	// Nel meta, non in post_content: così kses non tocca stile e script dell'edizione.
	update_post_meta($id, RASSEGNA_META, wp_slash($html));
	return [
		'ok'     => true,
		'id'     => $id,
		'url'    => home_url('/rassegna/' . $slug . '/'),
		'ultima' => home_url('/rassegna/'),
	];
}

function rassegna_rest_last() {
	$p = rassegna_latest();
	if (!$p) {
		return ['trovata' => false];
	}
	return [
		'trovata' => true,
		'slug'    => $p->post_name,
		'titolo'  => $p->post_title,
		'data'    => $p->post_date,
		'html'    => get_post_meta($p->ID, RASSEGNA_META, true),
	];
}

function rassegna_latest() {
	$q = get_posts(['post_type' => RASSEGNA_CPT, 'post_status' => 'publish', 'numberposts' => 1, 'orderby' => 'date', 'order' => 'DESC']);
	return $q ? $q[0] : null;
}

/* ---------- Accesso con password ---------- */

function rassegna_token() {
	return hash_hmac('sha256', (string) get_option('rassegna_pass_hash', RASSEGNA_DEFAULT_HASH), wp_salt('auth'));
}

function rassegna_authed() {
	if (is_user_logged_in() && current_user_can('manage_options')) {
		return true;
	}
	return isset($_COOKIE[RASSEGNA_COOKIE]) && hash_equals(rassegna_token(), (string) $_COOKIE[RASSEGNA_COOKIE]);
}

function rassegna_try_login() {
	$ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '0';
	$key = 'rassegna_try_' . md5($ip);
	$tries = (int) get_transient($key);
	if ($tries >= 10) {
		return 'Troppi tentativi. Riprova fra un quarto d\'ora.';
	}
	$pw = isset($_POST['rassegna_pw']) ? (string) wp_unslash($_POST['rassegna_pw']) : '';
	if ($pw !== '' && password_verify($pw, (string) get_option('rassegna_pass_hash', RASSEGNA_DEFAULT_HASH))) {
		delete_transient($key);
		setcookie(RASSEGNA_COOKIE, rassegna_token(), [
			'expires'  => time() + 90 * DAY_IN_SECONDS,
			'path'     => '/rassegna',
			'secure'   => is_ssl(),
			'httponly' => true,
			'samesite' => 'Lax',
		]);
		wp_safe_redirect(home_url(strtok($_SERVER['REQUEST_URI'], '?')));
		exit;
	}
	set_transient($key, $tries + 1, 15 * MINUTE_IN_SECONDS);
	return 'Password non corretta.';
}

/* ---------- Pagine pubbliche ---------- */

add_action('template_redirect', function () {
	$view = get_query_var('rassegna_view');
	if (!$view) {
		return;
	}
	if (!defined('DONOTCACHEPAGE')) {
		define('DONOTCACHEPAGE', true);
	}
	nocache_headers();
	header('X-Robots-Tag: noindex, nofollow, noarchive', true);
	header('Content-Type: text/html; charset=utf-8');

	if (!rassegna_authed()) {
		$error = ($_SERVER['REQUEST_METHOD'] === 'POST') ? rassegna_try_login() : '';
		echo rassegna_shell('Rassegna', rassegna_gate_body($error));
		exit;
	}

	if ($view === 'archive') {
		echo rassegna_shell('Rassegna · Archivio', rassegna_archive_body());
		exit;
	}

	$post = ($view === 'single')
		? get_page_by_path(get_query_var('rassegna_slug'), OBJECT, RASSEGNA_CPT)
		: rassegna_latest();

	if (!$post) {
		status_header($view === 'single' ? 404 : 200);
		$msg = $view === 'single'
			? '<p>Questa edizione non esiste. <a href="' . esc_url(home_url('/rassegna/archivio/')) . '">Vai all\'archivio</a>.</p>'
			: '<p>La prima edizione arriva alle 06:45.</p>';
		echo rassegna_shell('Rassegna', '<h1>Rassegna</h1>' . $msg);
		exit;
	}

	echo get_post_meta($post->ID, RASSEGNA_META, true); // Documento completo prodotto dalla routine.
	exit;
});

function rassegna_gate_body($error) {
	$err = $error ? '<p class="err">' . esc_html($error) . '</p>' : '';
	return '<h1>Rassegna</h1>
<form method="post" class="gate">
  <label for="rassegna_pw">Password</label>
  <input id="rassegna_pw" name="rassegna_pw" type="password" autocomplete="current-password" autofocus required>
  <button type="submit">Entra</button>
  ' . $err . '
</form>';
}

function rassegna_archive_body() {
	$posts = get_posts(['post_type' => RASSEGNA_CPT, 'post_status' => 'publish', 'numberposts' => 200, 'orderby' => 'date', 'order' => 'DESC']);
	$out = '<h1>Archivio</h1><p><a href="' . esc_url(home_url('/rassegna/')) . '">← Ultima edizione</a></p><ul class="arch">';
	foreach ($posts as $p) {
		$out .= '<li><a href="' . esc_url(home_url('/rassegna/' . $p->post_name . '/')) . '">' . esc_html($p->post_title) . '</a></li>';
	}
	return $out . '</ul>';
}

function rassegna_shell($title, $body) {
	return '<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>' . esc_html($title) . '</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500&family=IBM+Plex+Sans+Condensed:wght@400;500&display=swap">
<style>
:root{--ground:#EDF0F3;--ink:#18202B;--ink-3:#7A8491;--rule:#D5DBE2;--rubric:#A3203A;--sheet:#F8F9FB}
@media (prefers-color-scheme:dark){:root{color-scheme:dark;--ground:#12161C;--ink:#E6E9EE;--ink-3:#7F8995;--rule:#2C3440;--rubric:#E0677D;--sheet:#1A2029}}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:Newsreader,Georgia,serif;font-size:18px;line-height:1.5;padding:48px 16px}
main{max-width:520px;margin:0 auto}
h1{font-size:64px;font-weight:500;letter-spacing:-.02em;margin:0 0 24px;line-height:1}
a{color:var(--rubric)}
.gate{display:grid;gap:10px;background:var(--sheet);padding:20px;border-radius:10px}
label{font-family:"IBM Plex Sans Condensed",sans-serif;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}
input{font:inherit;padding:10px 12px;border:1px solid var(--rule);border-radius:6px;background:var(--ground);color:var(--ink)}
button{font-family:"IBM Plex Sans Condensed",sans-serif;font-size:16px;padding:10px;border:0;border-radius:6px;background:var(--rubric);color:#fff;cursor:pointer}
.err{color:var(--rubric);margin:0;font-family:"IBM Plex Sans Condensed",sans-serif}
.arch{list-style:none;padding:0;display:grid;gap:0}
.arch li{border-bottom:1px solid var(--rule);padding:10px 0}
.arch a{color:var(--ink);text-decoration:none}
</style></head><body><main>' . $body . '</main></body></html>';
}

/* ---------- Impostazioni ---------- */

add_action('admin_menu', function () {
	add_options_page('Rassegna', 'Rassegna', 'manage_options', 'rassegna', 'rassegna_settings_page');
});

function rassegna_settings_page() {
	if (!current_user_can('manage_options')) {
		return;
	}
	$msg = '';
	if (isset($_POST['rassegna_save']) && check_admin_referer('rassegna_settings')) {
		$new = isset($_POST['rassegna_new_pw']) ? (string) wp_unslash($_POST['rassegna_new_pw']) : '';
		if ($new !== '') {
			update_option('rassegna_pass_hash', password_hash($new, PASSWORD_BCRYPT), false);
			$msg .= 'Password aggiornata: chi era entrato dovrà reinserirla. ';
		}
		$pub = sanitize_user(wp_unslash($_POST['rassegna_publisher'] ?? ''));
		if ($pub !== '') {
			update_option('rassegna_publisher', $pub, false);
			$msg .= 'Utente della routine salvato.';
		}
	}
	?>
	<div class="wrap">
		<h1>Rassegna</h1>
		<?php if ($msg) : ?><div class="notice notice-success"><p><?php echo esc_html($msg); ?></p></div><?php endif; ?>
		<p>La rassegna è su <a href="<?php echo esc_url(home_url('/rassegna/')); ?>" target="_blank"><?php echo esc_html(home_url('/rassegna/')); ?></a>. È protetta da password e non viene indicizzata.</p>
		<form method="post">
			<?php wp_nonce_field('rassegna_settings'); ?>
			<table class="form-table">
				<tr><th><label for="rassegna_new_pw">Nuova password della pagina</label></th>
					<td><input id="rassegna_new_pw" name="rassegna_new_pw" type="text" class="regular-text" autocomplete="off"><p class="description">Lascia vuoto per non cambiarla.</p></td></tr>
				<tr><th><label for="rassegna_publisher">Utente della routine</label></th>
					<td><input id="rassegna_publisher" name="rassegna_publisher" type="text" class="regular-text" value="<?php echo esc_attr(get_option('rassegna_publisher', 'rassegna')); ?>"><p class="description">L'utente WordPress la cui password per le applicazioni usa la routine cloud.</p></td></tr>
			</table>
			<p><button class="button button-primary" name="rassegna_save" value="1">Salva</button></p>
		</form>
	</div>
	<?php
}
