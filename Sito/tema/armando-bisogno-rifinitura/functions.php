<?php
/**
 * Tema armando-bisogno: funzioni.
 *
 * Il tema non usa page builder: ogni sezione del sito è un template PHP
 * (page-{slug}.php). I contenuti si cambiano nei template.
 *
 * @package armando-bisogno
 */

defined( 'ABSPATH' ) || exit;

define( 'AB_VERSION', '1.2.0' );
define( 'AB_IMG', get_template_directory_uri() . '/assets/img/' );
define( 'AB_EMAIL', 'arbisogno@unisa.it' );

/** Le sezioni del sito: chiave => [slug, titolo]. */
function ab_sections() {
	return array(
		'ricerca'               => array( 'ricerca', 'Ricerca' ),
		'ia-e-nuove-tecnologie' => array( 'ia-e-nuove-tecnologie', 'IA e nuove tecnologie' ),
		'romanzi'               => array( 'romanzi', 'Romanzi' ),
		'phitness'              => array( 'phitness', 'Phitness' ),
		'profilo'               => array( 'profilo', 'Profilo e contatti' ),
	);
}

/** URL di una sezione ('' = home). */
function ab_url( $slug ) {
	return '' === $slug ? home_url( '/' ) : home_url( '/' . $slug . '/' );
}

/** Profili social: [etichetta, url, icona]. */
function ab_socials() {
	return array(
		array( 'Instagram', 'https://www.instagram.com/arbisogno/', 'instagram' ),
		array( 'Facebook', 'https://www.facebook.com/bisognoarmando', 'facebook' ),
		array( 'LinkedIn', 'https://www.linkedin.com/in/armando-bisogno-1ba575111/', 'linkedin' ),
		array( 'Substack', 'https://armandobisogno.substack.com', 'substack' ),
		array( 'Spotify · Macchine Parlanti', 'https://open.spotify.com/show/7IiQKcsGREet0QlxBUgIU5', 'spotify' ),
	);
}

/** Stampa i link social come icone tonde con etichetta accessibile. */
function ab_social_links( $class = '' ) {
	$icons = array(
		'instagram' => '<rect x="3.5" y="3.5" width="17" height="17" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.2" cy="6.8" r="1.2" fill="currentColor"/>',
		'facebook'  => '<path fill="currentColor" d="M13.5 21v-7.5h2.6l.4-3.1h-3V8.5c0-.9.3-1.5 1.6-1.5h1.6V4.2c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.3H7.9v3.1h2.6V21h3z"/>',
		'linkedin'  => '<path fill="currentColor" d="M6.9 8.6H3.6V20h3.3V8.6zM5.2 3.5a1.9 1.9 0 1 0 0 3.8 1.9 1.9 0 0 0 0-3.8zM20.4 13.6c0-3.1-1.6-5.2-4.4-5.2-1.6 0-2.6.9-3.1 1.7V8.6H9.8V20h3.3v-5.9c0-1.6.6-2.8 2.1-2.8 1.5 0 1.9 1.3 1.9 2.9V20h3.3v-6.4z"/>',
		'spotify'   => '<path fill="currentColor" d="M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zm4.1 13a.6.6 0 0 1-.8.2c-2.3-1.4-5.1-1.7-8.5-.9a.6.6 0 1 1-.3-1.1c3.7-.8 6.8-.5 9.4 1a.6.6 0 0 1 .2.8zm1.1-2.5a.7.7 0 0 1-1 .2c-2.6-1.6-6.6-2.1-9.7-1.1a.7.7 0 1 1-.4-1.4c3.5-1.1 7.9-.6 10.9 1.3.3.2.4.7.2 1zm.1-2.6C14.2 9.1 9 8.9 6 9.8a.8.8 0 1 1-.5-1.6c3.5-1.1 9.2-.9 12.8 1.3a.8.8 0 0 1-.8 1.4z"/>',
		'substack'  => '<path fill="currentColor" d="M5 4h14v2.1H5zM5 8h14v2.1H5zM5 12h14v8.5l-7-3.9-7 3.9z"/>',
	);
	echo '<ul class="social ' . esc_attr( $class ) . '">';
	foreach ( ab_socials() as $s ) {
		printf(
			'<li><a href="%1$s" aria-label="%2$s" title="%2$s" rel="me noopener" target="_blank"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">%3$s</svg></a></li>',
			esc_url( $s[1] ),
			esc_attr( $s[0] ),
			$icons[ $s[2] ] // SVG statico definito qui sopra.
		);
	}
	echo '</ul>';
}

/* -------------------------------------------------------------------------
 * Setup
 * ---------------------------------------------------------------------- */

add_action(
	'after_setup_theme',
	function () {
		add_theme_support( 'title-tag' );
		add_theme_support( 'post-thumbnails' );
		add_theme_support( 'html5', array( 'search-form', 'gallery', 'caption', 'style', 'script' ) );
		add_theme_support( 'automatic-feed-links' );
	}
);

add_action(
	'wp_enqueue_scripts',
	function () {
		wp_enqueue_style( 'ab-fonts', get_template_directory_uri() . '/assets/fonts/fonts.css', array(), AB_VERSION );
		wp_enqueue_style( 'ab-style', get_stylesheet_uri(), array( 'ab-fonts' ), AB_VERSION );
	}
);

/** Icona del sito (AB): sostituisce quella impostata in WordPress. */
remove_action( 'wp_head', 'wp_site_icon', 99 );
add_action(
	'wp_head',
	function () {
		printf( '<link rel="icon" href="%s" sizes="32x32" type="image/png">' . "\n", esc_url( AB_IMG . 'favicon-32.png?v=' . AB_VERSION ) );
		printf( '<link rel="icon" href="%s" sizes="512x512" type="image/png">' . "\n", esc_url( AB_IMG . 'favicon-512.png?v=' . AB_VERSION ) );
		printf( '<link rel="apple-touch-icon" href="%s">' . "\n", esc_url( AB_IMG . 'apple-touch-icon.png?v=' . AB_VERSION ) );
	},
	2
);

/** Precarica i due caratteri principali. */
add_action(
	'wp_head',
	function () {
		$base = get_template_directory_uri() . '/assets/fonts/';
		foreach ( array( 'LibreCaslonDisplay-normal-400-latin.woff2', 'HankenGrotesk-normal-400-latin.woff2' ) as $f ) {
			printf( '<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n", esc_url( $base . $f ) );
		}
	},
	1
);

/* -------------------------------------------------------------------------
 * All'attivazione: crea le pagine delle sezioni che mancano
 * ---------------------------------------------------------------------- */

add_action(
	'after_switch_theme',
	function () {
		$all = ab_sections() + array( 'post-scriptum' => array( 'post-scriptum', 'Post Scriptum' ) );
		foreach ( $all as $s ) {
			if ( ! get_page_by_path( $s[0] ) ) {
				wp_insert_post(
					array(
						'post_type'   => 'page',
						'post_status' => 'publish',
						'post_name'   => $s[0],
						'post_title'  => $s[1],
					)
				);
			}
		}
		flush_rewrite_rules();
	}
);

/* -------------------------------------------------------------------------
 * I template del tema hanno la precedenza su quelli di Elementor
 * (le vecchie pagine costruite con Elementor hanno lo stesso slug).
 * ---------------------------------------------------------------------- */

add_filter(
	'template_include',
	function ( $template ) {
		if ( is_front_page() ) {
			return get_template_directory() . '/front-page.php';
		}
		if ( is_page() ) {
			$slug = get_post_field( 'post_name', get_queried_object_id() );
			$file = get_template_directory() . '/page-' . $slug . '.php';
			if ( file_exists( $file ) ) {
				return $file;
			}
		}
		return $template;
	},
	999
);

/*
 * Elementor Pro (Theme Builder) sostituisce header.php e footer.php con le sue
 * testate: le togliamo, così il tema usa sempre le proprie. Togliamo anche la
 * classe del "kit" Elementor dal body, che applicherebbe caratteri e colori globali.
 */
add_action(
	'template_redirect',
	function () {
		global $wp_filter;
		foreach ( array( 'get_header', 'get_footer' ) as $hook ) {
			if ( empty( $wp_filter[ $hook ] ) ) {
				continue;
			}
			foreach ( $wp_filter[ $hook ]->callbacks as $priority => $callbacks ) {
				foreach ( $callbacks as $cb ) {
					$fn = $cb['function'];
					if ( is_array( $fn ) && is_object( $fn[0] ) && false !== strpos( get_class( $fn[0] ), 'ElementorPro\\Modules\\ThemeBuilder' ) ) {
						remove_action( $hook, $fn, $priority );
					}
				}
			}
		}
	},
	9999
);

/**
 * True dove la pagina è disegnata dal tema e Elementor non serve: home, pagine
 * con template page-{slug}.php, articoli e archivi. False solo per i contenuti
 * ancora costruiti con Elementor.
 */
function ab_is_theme_page() {
	if ( is_front_page() ) {
		return true;
	}
	if ( is_page() ) {
		$slug = get_post_field( 'post_name', get_queried_object_id() );
		if ( file_exists( get_template_directory() . '/page-' . $slug . '.php' ) ) {
			return true;
		}
	}
	if ( is_singular() ) {
		return 'builder' !== get_post_meta( get_queried_object_id(), '_elementor_edit_mode', true );
	}
	return true;
}

/*
 * Sulle pagine del tema Elementor non serve: niente suoi CSS, JS e Google Fonts
 * (più leggerezza, e nessun IP dei visitatori inviato a Google).
 */
add_filter( 'elementor/frontend/print_google_fonts', fn( $print ) => ab_is_theme_page() ? false : $print );
add_filter(
	'style_loader_tag',
	function ( $tag, $handle, $href ) {
		if ( ab_is_theme_page() && ( false !== strpos( (string) $href, '/elementor' ) || false !== strpos( (string) $href, 'fonts.googleapis.com' ) ) ) {
			return '';
		}
		return $tag;
	},
	10,
	3
);
add_filter(
	'script_loader_tag',
	function ( $tag, $handle, $src ) {
		if ( ab_is_theme_page() && false !== strpos( (string) $src, '/elementor' ) ) {
			return '';
		}
		return $tag;
	},
	10,
	3
);

add_filter(
	'body_class',
	function ( $classes ) {
		return array_values( array_filter( $classes, fn( $c ) => 0 !== strpos( $c, 'elementor-kit-' ) ) );
	},
	999
);

/* -------------------------------------------------------------------------
 * Redirect permanenti dalle vecchie pagine
 * ---------------------------------------------------------------------- */

add_action(
	'template_redirect',
	function () {
		$map  = array(
			'home'                 => '',
			'ricerche'             => 'ricerca',
			'pubblicazioni_aperte' => 'ricerca',
			'open'                 => 'ricerca',
			'phitnesslab'          => 'phitness',
			'libra'                => '',
			'ats'                  => '',
			'cronache'             => '',
		);
		$path = trim( (string) wp_parse_url( isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '', PHP_URL_PATH ), '/' );
		if ( isset( $map[ $path ] ) || ( 0 === strpos( $path, 'cronache/' ) ) ) {
			$to = isset( $map[ $path ] ) ? $map[ $path ] : '';
			wp_safe_redirect( ab_url( $to ), 301 );
			exit;
		}
	},
	1
);

/* -------------------------------------------------------------------------
 * Ultime uscite: newsletter e podcast dai feed RSS di Substack
 * ---------------------------------------------------------------------- */

/** I feed di Substack si aggiornano ogni ora (il default di WordPress è 12 ore). */
add_filter(
	'wp_feed_cache_transient_lifetime',
	function ( $lifetime, $url ) {
		return false !== strpos( (string) $url, 'substack.com' ) ? HOUR_IN_SECONDS : $lifetime;
	},
	10,
	2
);

function ab_latest_feed() {
	include_once ABSPATH . WPINC . '/feed.php';
	$sources = array(
		array(
			'name' => 'Macchine Pensanti',
			'feed' => 'https://armandobisogno.substack.com/feed',
			'home' => 'https://armandobisogno.substack.com',
			'cta'  => 'Leggi la newsletter →',
		),
		array(
			'name' => 'Macchine Parlanti',
			'feed' => 'https://macchineparlanti.substack.com/feed',
			'home' => 'https://macchineparlanti.substack.com/',
			'cta'  => 'Ascolta la puntata →',
		),
	);
	echo '<div class="feed latest">';
	foreach ( $sources as $s ) {
		$title = '';
		$link  = $s['home'];
		$desc  = '';
		$date  = '';
		$rss   = fetch_feed( $s['feed'] );
		if ( ! is_wp_error( $rss ) && $rss->get_item_quantity( 1 ) ) {
			$item  = $rss->get_item( 0 );
			$title = $item->get_title();
			$link  = $item->get_permalink();
			$desc  = wp_strip_all_tags( (string) $item->get_description() );
			$date  = mb_strtolower( date_i18n( 'j F Y', $item->get_date( 'U' ) ) );
		}
		echo '<article>';
		printf( '<span class="eyebrow">%s%s</span>', esc_html( $s['name'] ), $date ? ' · ' . esc_html( $date ) : '' );
		if ( $title ) {
			printf( '<h3><a href="%s">%s</a></h3>', esc_url( $link ), esc_html( $title ) );
			if ( $desc ) {
				printf( '<p>%s</p>', esc_html( wp_trim_words( $desc, 28 ) ) );
			}
		} else {
			printf( '<h3><a href="%s">%s</a></h3>', esc_url( $link ), esc_html( $s['name'] ) );
		}
		printf( '<a class="more" href="%s">%s</a>', esc_url( $link ), esc_html( $s['cta'] ) );
		echo '</article>';
	}
	echo '</div>';
}

/* -------------------------------------------------------------------------
 * Una intelligenza fantastica: versioni dal Foglio Google «Versioni UIF»
 * (colonne: Versione, Data di pubblicazione, Note). Letto dal server, in cache 1 ora.
 * ---------------------------------------------------------------------- */

define( 'AB_UIF_SHEET', '12f38iYsgQVB2XtuGujufpiqvnF_wdbu9ubbc1sro9RA' );

function ab_uif_versions() {
	$cached = get_transient( 'ab_uif_versions' );
	if ( is_array( $cached ) ) {
		return $cached;
	}
	$res = wp_remote_get( 'https://docs.google.com/spreadsheets/d/' . AB_UIF_SHEET . '/export?format=csv', array( 'timeout' => 8 ) );
	if ( is_wp_error( $res ) || 200 !== wp_remote_retrieve_response_code( $res ) ) {
		$old = get_option( 'ab_uif_versions_last', array() );
		set_transient( 'ab_uif_versions', $old, 10 * MINUTE_IN_SECONDS );
		return $old;
	}
	$rows = array_map( 'str_getcsv', preg_split( '/\r\n|\n|\r/', trim( (string) wp_remote_retrieve_body( $res ) ) ) );
	array_shift( $rows ); // Intestazioni.
	$out = array();
	foreach ( $rows as $r ) {
		if ( empty( $r[0] ) ) {
			continue;
		}
		$out[] = array(
			'versione' => trim( $r[0] ),
			'data'     => isset( $r[1] ) ? trim( $r[1] ) : '',
			'note'     => isset( $r[2] ) ? trim( $r[2] ) : '',
		);
	}
	set_transient( 'ab_uif_versions', $out, HOUR_IN_SECONDS );
	update_option( 'ab_uif_versions_last', $out, false );
	return $out;
}

/* -------------------------------------------------------------------------
 * Phitness: ipotesi di lezione (carosello). Per aggiungerne una basta un elemento.
 * ---------------------------------------------------------------------- */

function ab_lessons() {
	return array(
		array(
			'titolo'    => 'So di (non) sapere',
			'img'       => 'lez-socrate.jpg',
			'opera'     => 'Jacques-Louis David, <em>La morte di Socrate</em>, 1787 · Metropolitan Museum of Art, New York',
			'fonte'     => 'The Met Open Access, CC0',
			'fonte_url' => 'https://commons.wikimedia.org/wiki/File:The_Death_of_Socrates_MET_DP-13139-001.jpg',
			'testo'     => 'Una riflessione sul significato di parole come ‘conoscenza’, ‘competenza’, ‘saperi’, partendo dalla prospettiva socratica del ‘so di non sapere’ fino all\'illusione contemporanea di sapere tutto solo perché si è capaci di interrogare un oracolo artificiale.',
		),
		array(
			'titolo'    => 'Che tempo fa?',
			'img'       => 'lez-dali.jpg',
			'opera'     => 'Salvador Dalí, <em>La persistenza della memoria</em>, 1931 · Museum of Modern Art, New York',
			'fonte'     => '© Salvador Dalí, Fundació Gala-Salvador Dalí, by SIAE 2026',
			'fonte_url' => 'https://www.moma.org/collection/works/79018',
			'testo'     => 'Agostino spiega nelle <em>Confessioni</em> che il tempo esiste solo perché lo misuriamo: la memoria è la misura del passato, il desiderio è la misura del futuro mentre l\'attenzione misura il presente. Che cosa significa ‘misurare il tempo’ in un mondo nel quale tutto viene vissuto in modo asincrono?',
		),
		array(
			'titolo'    => 'Fidarsi è bene?',
			'img'       => 'lez-tommaso.jpg',
			'opera'     => 'Caravaggio, <em>L\'incredulità di san Tommaso</em>, 1601-1602 · Bildergalerie, Potsdam',
			'fonte'     => 'Wikimedia Commons, pubblico dominio',
			'fonte_url' => 'https://commons.wikimedia.org/wiki/File:The_Incredulity_of_Saint_Thomas-Caravaggio_(1601-2).jpg',
			'testo'     => 'Avere fede è credere che una notizia sia vera e agire di conseguenza. Questo vale se la notizia è contenuta in un libro sacro ma anche nel caso del racconto di un amico che ci chiede di credergli. Oggi più che mai è importante ragionare sul modo con il quale validiamo le fonti e verifichiamo se e quanto una notizia sia affidabile, cioè degna di fede.',
		),
		array(
			'titolo'    => 'Fragile. Maneggiare con cura',
			'img'       => 'lez-cioccolataia.jpg',
			'opera'     => 'Jean-Étienne Liotard, <em>La bella cioccolataia</em>, 1744 circa · Gemäldegalerie Alte Meister, Dresda',
			'fonte'     => 'Wikimedia Commons, pubblico dominio',
			'fonte_url' => 'https://commons.wikimedia.org/wiki/File:Jean-Etienne_Liotard_-_The_Chocolate_Girl_-_Google_Art_Project.jpg',
			'testo'     => 'Siamo abituati a raccontarci attraverso i successi: obiettivi, risultati, prestazioni. Ma un gruppo diventa davvero una comunità quando sa accogliere i limiti di ciascuno. Che cosa cambia se usiamo un linguaggio che non nasconde la fragilità ma la espone? Una riflessione sul tono di voce con cui parliamo e scriviamo agli altri: inclusivo, attento, mai tossico.',
		),
		array(
			'titolo'    => 'Punti di vista',
			'img'       => 'lez-vermeer.jpg',
			'opera'     => 'Johannes Vermeer, <em>L\'arte della pittura</em>, 1666-1668 · Kunsthistorisches Museum, Vienna',
			'fonte'     => 'Wikimedia Commons, pubblico dominio',
			'fonte_url' => 'https://commons.wikimedia.org/wiki/File:Jan_Vermeer_-_The_Art_of_Painting_-_Google_Art_Project.jpg',
			'testo'     => 'Chi ha scritto questo testo? Una persona, una macchina, tutte e due? Chiederselo rischia di diventare una caccia al colpevole. Più utile è domandarsi da quale punto di vista un testo è stato scritto: chi lo firma deve saper dire come lo ha costruito, che cosa ha scelto e di che cosa si assume la responsabilità. Scrivere, con o senza macchine, è sempre prendere posizione.',
		),
		array(
			'titolo'    => 'Vuoto a perdere',
			'img'       => 'lez-vuoto.jpg',
			'opera'     => 'Vilhelm Hammershøi, <em>Polvere che danza nei raggi di sole</em>, 1900 · Ordrupgaard, Copenaghen',
			'fonte'     => 'Wikimedia Commons, pubblico dominio',
			'fonte_url' => 'https://commons.wikimedia.org/wiki/File:Hammersh%C3%B8i_Dust_motes_dancing.jpg',
			'testo'     => 'Centinaia di foto che non guardiamo, promemoria che ci ricordano dov\'eravamo anni fa, notifiche che non lasciano mai un momento di silenzio. Non sappiamo più sopportare il vuoto, fino a immaginare app che fanno parlare chi non c\'è più. Eppure il vuoto è lo spazio nel quale possiamo costruire, dopo ogni perdita, un racconto nuovo. Che cosa succede se smettiamo di riempirlo?',
		),
	);
}

function ab_lessons_carousel() {
	$allowed = array( 'em' => array() );
	?>
	<div class="lessons" data-carousel>
		<div class="lessons-head">
			<div class="head" style="margin:0"><span class="eyebrow">Ipotesi di lezione</span><h2>Per esempio?</h2></div>
			<div class="lessons-nav">
				<button type="button" class="lessons-btn" data-dir="-1" aria-label="Lezione precedente">←</button>
				<button type="button" class="lessons-btn" data-dir="1" aria-label="Lezione successiva">→</button>
			</div>
		</div>
		<ul class="lessons-track" tabindex="0" aria-label="Ipotesi di lezione">
			<?php foreach ( ab_lessons() as $l ) : ?>
				<li class="lesson">
					<h3><?php echo esc_html( $l['titolo'] ); ?></h3>
					<figure>
						<img src="<?php echo esc_url( AB_IMG . $l['img'] ); ?>" alt="" loading="lazy" width="800" height="600">
						<figcaption><?php echo wp_kses( $l['opera'], $allowed ); ?><br><span class="src">Immagine: <a href="<?php echo esc_url( $l['fonte_url'] ); ?>" rel="noopener" target="_blank"><?php echo esc_html( $l['fonte'] ); ?></a></span></figcaption>
					</figure>
					<p><?php echo wp_kses( $l['testo'], $allowed ); ?></p>
				</li>
			<?php endforeach; ?>
		</ul>
	</div>
	<?php
}

/** Il segno Φ di Phitness (stesso disegno di phitness.it). */
function ab_phitness_mark( $size = 28 ) {
	return sprintf( '<svg class="phit-mark" viewBox="0 0 48 48" width="%1$d" height="%1$d" aria-hidden="true"><circle cx="24" cy="24" r="13.5" fill="none" stroke="#4F7CB6" stroke-width="4"/><path d="M24 3.5v41" stroke="#152238" stroke-width="3.6" stroke-linecap="round"/><circle cx="24" cy="3.6" r="2.6" fill="#F2B35E"/></svg>', (int) $size );
}

/* -------------------------------------------------------------------------
 * Anteprime di condivisione (WhatsApp, Facebook, LinkedIn, Telegram) e titoli.
 * Le scrive il tema; quelle automatiche di Yoast restano spente.
 * ---------------------------------------------------------------------- */

/** Titolo, descrizione e immagine della pagina corrente. */
function ab_meta() {
	$site = 'Armando Bisogno';
	$map  = array(
		''                           => array( $site . ' · Usare la filosofia per capire il presente', 'Insegno Storia della filosofia medievale all\'Università di Salerno. Ricerca su Agostino e il Medioevo, intelligenza artificiale, romanzi e Phitness, filosofia per aziende e comunità.', 'og-home.jpg' ),
		'ricerca'                    => array( 'Ricerca · ' . $site, 'Leggere il Medioevo, ripensare le Humanities: cinque libri su Agostino e l\'alto Medioevo, pubblicazioni aperte e il manifesto Ermenetica.', 'og-ricerca.jpg' ),
		'ia-e-nuove-tecnologie'      => array( 'IA e nuove tecnologie · ' . $site, 'Le macchine, lette da un umanista: la newsletter Macchine Pensanti, il podcast Macchine Parlanti e il libro aperto Una intelligenza fantastica.', 'og-home.jpg' ),
		'romanzi'                    => array( 'Romanzi · ' . $site, 'Terapie e Mosaici, i gialli del commissario Malversi, ambientati a Fossa Etrusca. Pubblicati da De Tomi.', 'og-romanzi.jpg' ),
		'phitness'                   => array( 'Phitness · Filosofia per aziende e comunità', 'Un laboratorio di filosofia per allenarsi a concentrarsi, leggere con attenzione e scrivere dopo aver pensato. Incontri singoli o percorsi, con restituzioni personali e anonime.', 'og-phitness.jpg' ),
		'profilo'                    => array( 'Profilo e contatti · ' . $site, 'Studioso, docente, life addicted. Storia della filosofia medievale all\'Università di Salerno. Inviti, conferenze, collaborazioni.', 'og-home.jpg' ),
		'una-intelligenza-fantastica' => array( 'Una intelligenza fantastica · ' . $site, 'Otto riflessioni aperte sull\'intelligenza artificiale, lette con gli occhi di uno studioso di filosofia. Gratuite in PDF ed ePub.', 'og-uif.jpg' ),
		'post-scriptum'              => array( 'Post Scriptum · ' . $site, 'Appunti, riflessioni e materiali scritti nel tempo.', 'og-home.jpg' ),
	);
	$key = null;
	if ( is_front_page() ) {
		$key = '';
	} elseif ( is_page() ) {
		$slug = get_post_field( 'post_name', get_queried_object_id() );
		$key  = isset( $map[ $slug ] ) ? $slug : null;
	}
	if ( null !== $key ) {
		list( $t, $d, $i ) = $map[ $key ];
		return array( 'title' => $t, 'desc' => $d, 'image' => AB_IMG . $i, 'type' => 'website' );
	}
	if ( is_singular() ) {
		$id    = get_queried_object_id();
		$desc  = has_excerpt( $id ) ? get_the_excerpt( $id ) : wp_trim_words( wp_strip_all_tags( strip_shortcodes( get_post_field( 'post_content', $id ) ) ), 30, '…' );
		$thumb = get_the_post_thumbnail_url( $id, 'large' );
		return array( 'title' => get_the_title( $id ) . ' · ' . $site, 'desc' => $desc, 'image' => $thumb ? $thumb : AB_IMG . 'og-home.jpg', 'type' => is_single() ? 'article' : 'website' );
	}
	return array( 'title' => wp_strip_all_tags( get_the_archive_title() ) . ' · ' . $site, 'desc' => $map[''][1], 'image' => AB_IMG . 'og-home.jpg', 'type' => 'website' );
}

// Yoast: niente anteprime automatiche; titolo e descrizione dal tema.
add_filter(
	'option_wpseo_social',
	function ( $o ) {
		$o              = is_array( $o ) ? $o : array();
		$o['opengraph'] = false;
		$o['twitter']   = false;
		return $o;
	}
);
add_filter( 'wpseo_title', fn() => ab_meta()['title'], 99 );
add_filter( 'pre_get_document_title', fn() => ab_meta()['title'], 99 );
add_filter( 'wpseo_metadesc', fn() => ab_meta()['desc'], 99 );

add_action(
	'wp_head',
	function () {
		$m   = ab_meta();
		$url = is_front_page() ? home_url( '/' ) : ( is_singular() ? get_permalink() : home_url( add_query_arg( array() ) ) );
		$tags = array(
			'og:locale'      => 'it_IT',
			'og:type'        => $m['type'],
			'og:site_name'   => 'Armando Bisogno',
			'og:title'       => $m['title'],
			'og:description' => $m['desc'],
			'og:url'         => $url,
			'og:image'       => $m['image'],
		);
		foreach ( $tags as $k => $v ) {
			printf( '<meta property="%s" content="%s">' . "\n", esc_attr( $k ), esc_attr( $v ) );
		}
		if ( false !== strpos( $m['image'], '/og-' ) ) {
			echo '<meta property="og:image:width" content="1200">' . "\n" . '<meta property="og:image:height" content="630">' . "\n";
		}
		printf( '<meta name="twitter:card" content="summary_large_image">' . "\n" . '<meta name="twitter:title" content="%s">' . "\n" . '<meta name="twitter:description" content="%s">' . "\n" . '<meta name="twitter:image" content="%s">' . "\n", esc_attr( $m['title'] ), esc_attr( $m['desc'] ), esc_url( $m['image'] ) );
		if ( ! defined( 'WPSEO_VERSION' ) ) {
			printf( '<meta name="description" content="%s">' . "\n", esc_attr( $m['desc'] ) );
		}
	},
	5
);

/* -------------------------------------------------------------------------
 * Modulo di contatto (Phitness e Profilo) → mail a AB_EMAIL
 * ---------------------------------------------------------------------- */

/** Opzioni del modulo Phitness. */
function ab_phit_interessi() {
	return array(
		'azienda'  => 'Phitness nella mia azienda',
		'comunita' => 'Phitness nella mia comunità',
		'info'     => 'Vorrei saperne di più',
	);
}

function ab_contact_form( $tipo ) {
	$esito = isset( $_GET['inviato'] ) ? sanitize_key( wp_unslash( $_GET['inviato'] ) ) : '';
	$ok    = ( 'ok-' . $tipo ) === $esito;
	$ko    = ( 'ko-' . $tipo ) === $esito;
	if ( $ok ) {
		echo '<p class="form-ok">Grazie, il messaggio è arrivato. Ti rispondo di persona.</p>';
		return;
	}
	if ( $ko ) {
		echo '<p class="form-ko">Il messaggio non è partito. Controlla nome, email e testo, poi riprova.</p>';
	}
	$is_phit = ( 'phitness' === $tipo );
	?>
	<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
		<input type="hidden" name="action" value="ab_contatto">
		<input type="hidden" name="tipo" value="<?php echo esc_attr( $tipo ); ?>">
		<input type="hidden" name="t" value="<?php echo esc_attr( time() ); ?>">
		<?php wp_nonce_field( 'ab_contatto', 'ab_nonce' ); ?>
		<p class="hp" aria-hidden="true"><label>Non compilare<input type="text" name="sito_web" tabindex="-1" autocomplete="off"></label></p>
		<div class="fgrid">
			<label for="f-nome-<?php echo esc_attr( $tipo ); ?>">Nome e cognome<input id="f-nome-<?php echo esc_attr( $tipo ); ?>" name="nome" required autocomplete="name"></label>
			<label for="f-mail-<?php echo esc_attr( $tipo ); ?>">Email<input id="f-mail-<?php echo esc_attr( $tipo ); ?>" name="email" type="email" required autocomplete="email"></label>
		</div>
		<?php if ( $is_phit ) : ?>
			<fieldset class="choice">
				<legend>Mi interessa</legend>
				<?php
				foreach ( ab_phit_interessi() as $k => $label ) {
					printf( '<label class="opt"><input type="radio" name="interesse" value="%1$s"%3$s required><span>%2$s</span></label>', esc_attr( $k ), esc_html( $label ), 'azienda' === $k ? ' checked' : '' );
				}
				?>
			</fieldset>
			<label for="f-org"><span>Azienda o comunità <em class="opt-note">(facoltativo)</em></span><input id="f-org" name="org"></label>
		<?php endif; ?>
		<label for="f-msg-<?php echo esc_attr( $tipo ); ?>"><span><?php echo $is_phit ? 'Vuoi aggiungere qualcosa? <em class="opt-note">(facoltativo)</em>' : 'Messaggio'; ?></span><textarea id="f-msg-<?php echo esc_attr( $tipo ); ?>" name="messaggio"<?php echo $is_phit ? '' : ' required'; ?> placeholder="<?php echo $is_phit ? esc_attr( 'Quante persone, che lavoro fanno, che cosa vi incuriosisce.' ) : ''; ?>"></textarea></label>
		<button class="btn btn-primary" type="submit"><?php echo $is_phit ? 'Lascia il contatto' : 'Invia'; ?></button>
		<p class="note"><?php echo $is_phit ? 'Userò il tuo indirizzo solo per ricontattarti.' : 'I dati servono solo a risponderti e non vengono conservati sul sito.'; ?></p>
	</form>
	<?php
}

function ab_handle_contact() {
	$tipo = isset( $_POST['tipo'] ) && 'phitness' === $_POST['tipo'] ? 'phitness' : 'contatti';
	$back = ab_url( 'phitness' === $tipo ? 'phitness' : 'profilo' );
	$fail = function () use ( $back, $tipo ) {
		wp_safe_redirect( add_query_arg( 'inviato', 'ko-' . $tipo, $back ) . ( 'phitness' === $tipo ? '#richiesta' : '#contatti' ) );
		exit;
	};
	if ( ! isset( $_POST['ab_nonce'] ) || ! wp_verify_nonce( sanitize_text_field( wp_unslash( $_POST['ab_nonce'] ) ), 'ab_contatto' ) ) {
		$fail();
	}
	// Trappole per i bot: campo nascosto compilato o invio in meno di 3 secondi.
	$t = isset( $_POST['t'] ) ? (int) $_POST['t'] : 0;
	if ( ! empty( $_POST['sito_web'] ) || ( time() - $t ) < 3 ) {
		wp_safe_redirect( add_query_arg( 'inviato', 'ok-' . $tipo, $back ) );
		exit;
	}
	$nome  = sanitize_text_field( wp_unslash( $_POST['nome'] ?? '' ) );
	$email = sanitize_email( wp_unslash( $_POST['email'] ?? '' ) );
	$msg   = sanitize_textarea_field( wp_unslash( $_POST['messaggio'] ?? '' ) );
	$interessi = ab_phit_interessi();
	$interesse = sanitize_key( wp_unslash( $_POST['interesse'] ?? '' ) );
	if ( '' === $nome || ! is_email( $email ) || ( 'contatti' === $tipo && '' === $msg ) || ( 'phitness' === $tipo && ! isset( $interessi[ $interesse ] ) ) ) {
		$fail();
	}
	$lines = array( 'Nome: ' . $nome, 'Email: ' . $email );
	if ( 'phitness' === $tipo ) {
		$lines[] = 'Interesse: ' . $interessi[ $interesse ];
		$lines[] = 'Azienda o comunità: ' . sanitize_text_field( wp_unslash( $_POST['org'] ?? '' ) );
	}
	$lines[] = '';
	$lines[] = '' !== $msg ? $msg : '(nessun messaggio)';
	$subject = 'phitness' === $tipo ? '[Sito] Phitness · ' . $interessi[ $interesse ] . ' · ' . $nome : '[Sito] Messaggio da ' . $nome;
	$sent    = wp_mail( AB_EMAIL, $subject, implode( "\n", $lines ), array( 'Reply-To: ' . $nome . ' <' . $email . '>' ) );
	if ( ! $sent ) {
		$fail();
	}
	wp_safe_redirect( add_query_arg( 'inviato', 'ok-' . $tipo, $back ) . ( 'phitness' === $tipo ? '#richiesta' : '#contatti' ) );
	exit;
}
add_action( 'admin_post_nopriv_ab_contatto', 'ab_handle_contact' );
add_action( 'admin_post_ab_contatto', 'ab_handle_contact' );

/* -------------------------------------------------------------------------
 * Pulizia
 * ---------------------------------------------------------------------- */

remove_action( 'wp_head', 'print_emoji_detection_script', 7 );
remove_action( 'wp_print_styles', 'print_emoji_styles' );
add_filter( 'excerpt_length', fn() => 32 );
add_filter( 'excerpt_more', fn() => '…' );
