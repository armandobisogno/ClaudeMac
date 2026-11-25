"""Riconduzione dei definienda (forma del testo) al lemma: passaggio separato e dichiarato, sopra i dati della codifica.
Uscita: _dati/lemmi_definienda.tsv (forma, lemma, tipo). Tipi: identico | flessione | verbo | sintagma | rinvio."""
import os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__))
forme = [l.split("\t")[1] for l in open(os.path.join(HERE, "../_dati/forme_definienda.txt"), encoding="utf-8").read().splitlines()]

# flessione nominale/aggettivale → nominativo singolare (o forma di citazione)
N = {
 "Aeternae legis":"Aeterna lex","Aequales":"Aequalis","Aequalia":"Aequalis","Aequales pedes":"Aequalis pes","Aequalitatem numerosam":"Aequalitas numerosa",
 "Altitudinem":"Altitudo","Animae":"Anima","Animam":"Anima","Animam humanam":"Anima humana","Humana anima":"Anima humana","Animos":"Animus","Animum":"Animus",
 "Arte":"Ars","Artem":"Ars","Artes":"Ars","Artis":"Ars","Aspectum":"Aspectus","Beatam vitam":"Beata vita","Vita beata":"Beata vita","Beati":"Beatus","Beatos":"Beatus",
 "Beatum":"Beatus","Beatum hominem":"Beatus homo","Barbarismum":"Barbarismus","Bestiae":"Bestia","Bestias":"Bestia","Bona voluntate":"Bona voluntas","Bonam voluntatem":"Bona voluntas",
 "Bonam":"Bonus","Breves":"Brevis","Breve":"Brevis","Caducarii":"Caducarius","Cantu":"Cantus","Casum":"Casus","Chirurgiam":"Chirurgia","Circuitum":"Circuitus",
 "Coloratum":"Coloratus","Colorem":"Color","Comparationem":"Comparatio","Corpora":"Corpus","Corpori":"Corpus","Corporibus":"Corpus","Corporales":"Corporalis","Corporalia":"Corporalis",
 "Corporea":"Corporeus","Cupiditatem":"Cupiditas","Dei Filium":"Dei Filius","Filium Dei":"Dei Filius","Dei Virtutem atque Sapientiam":"Dei Virtus et Sapientia","Dei Virtutem et Dei Sapientiam":"Dei Virtus et Sapientia",
 "Deo":"Deus","Deum":"Deus","Dialecticam":"Dialectica","Disciplinae huius":"Disciplina","Disciplinam":"Disciplina","Disciplinas":"Disciplina","Egestati":"Egestas","Egestatis nomen":"Egestas",
 "Epulis":"Epulae","Errorem":"Error","Erroris":"Error","Falsa":"Falsum","Falsam":"Falsum","Falsas":"Falsum","Falsarum opinionum":"Falsa opinio","Falsitatem":"Falsitas","Falsitatis":"Falsitas",
 "Figuram":"Figura","Figurarum":"Figura","Figuras":"Figura","Finem":"Finis","Fortem":"Fortis","Fortitudinis":"Fortitudo","Frugalitatem":"Frugalitas","Frugem":"Frux","Geometriam":"Geometria",
 "Homine":"Homo","Hominem":"Homo","Hominem ordinatissimum":"Homo ordinatissimus","Ordinatus homo":"Homo ordinatus","Perfectum hominem":"Homo perfectus","Humanam sapientiam":"Humana sapientia","Humanam scientiam":"Humana scientia",
 "Humanarum rerum scientia":"Rerum humanarum scientia","Res humanas":"Res humanae","Humanae res":"Res humanae","Res divinas":"Res divinae","Iambos pedes":"Iambus","Imaginem scientiae":"Imago scientiae",
 "Intellectum":"Intellectus","Intellegentiam":"Intellegentia","Intentione digiti":"Intentio digiti","Iudicialium":"Iudicialis","Iudiciales":"Iudicialis","Iustitiae":"Iustitia","Iustitiam":"Iustitia",
 "Iustitiam Dei":"Iustitia Dei","Latitudinem":"Latitudo","Legem":"Lex","Legem istam":"Lex","Legis":"Lex","Libidine":"Libido","Libidinem":"Libido","Lineam":"Linea","Litterationem":"Litteratio",
 "Locutione":"Locutio","Locutionem":"Locutio","Longa":"Longus","Longam":"Longus","Longae syllabae":"Longa syllaba","Longitudinem":"Longitudo","Lumine":"Lumen","Magistros":"Magister",
 "Magnitudine":"Magnitudo","Malefacta":"Malefactum","Memoriam":"Memoria","Mendaces":"Mendax","Membra":"Membrum","Mentem":"Mens","Metris":"Metrum","Metrorum":"Metrum","Minimum metrum":"Metrum minimum",
 "Miseriam":"Miseria","Miserum":"Miser","Modulatione":"Modulatio","Modulationem":"Modulatio","Modum":"Modus","Montem":"Mons","Morbos":"Morbus","Mortuum":"Mortuus","Motum":"Motus","Multitudinem":"Multitudo",
 "Mundos":"Mundus","Mundum":"Mundus","Mundum (sensibilem)":"Mundus sensibilis","Musas":"Musa","Musicae":"Musica","Musicam":"Musica","Mutas":"Muta","Naturam":"Natura","Nequitiam":"Nequitia",
 "Nomina":"Nomen","Hoc nomen":"Nomen","Hoc nomine":"Nomen","Numeri":"Numerus","Numero":"Numerus","Numerum":"Numerus","Hi numeri":"Numerus","Ordine":"Ordo","Ordinem":"Ordo","Ordini":"Ordo","Ordinis":"Ordo",
 "Ordinem rerum":"Ordo rerum","Opulentiam":"Opulentia","Parem":"Par","Paris numeri":"Par numerus","Partibus orationis":"Partes orationis","Partitionem":"Partitio","Pedem":"Pes","Pedes":"Pes",
 "Peccata":"Peccatum","Perceptionem":"Perceptio","Phantasiam":"Phantasia","Phantasmata":"Phantasma","Philosophum":"Philosophus","Plenitudine":"Plenitudo","Probabili":"Probabile","Probabilitate":"Probabilitas",
 "Probabilia vel verisimilia":"Probabile vel verisimile","Proceleumaticum":"Proceleumaticus","Pronomina":"Pronomen","Proportione":"Proportio","Proportionem":"Proportio","Prudentiam":"Prudentia",
 "Pulchra":"Pulchrum","Pulchritudinis":"Pulchritudo","Puncto":"Punctum","Rationem":"Ratio","Rationabiles":"Rationabilis","Ratiocinationem":"Ratiocinatio","Recordabiles":"Recordabilis",
 "Rhetoricam":"Rhetorica","Rhythmi":"Rhythmus","Rhythmis":"Rhythmus","Rhythmum":"Rhythmus","Sapiente":"Sapiens","Sapientem":"Sapiens","Sapientes":"Sapiens","Sapienti":"Sapiens","Sapientis":"Sapiens",
 "Sapientiae":"Sapientia","Sapientiam":"Sapientia","Sapientiae studiosum":"Studiosus sapientiae","Studioso sapientiae":"Studiosus sapientiae","Studioso":"Studiosus sapientiae","Scientiae":"Scientia","Scientiam":"Scientia",
 "Scientiam modulandi":"Scientia modulandi","Sensum":"Sensus","Sententiam":"Sententia","Signa":"Signum","Ea signa":"Signum","Signo":"Signum","Significationem":"Significatio","Sono":"Sonus","Sonum":"Sonus",
 "Sphaeram":"Sphaera","Spiritus immundus":"Spiritus immundus","Stultitiae":"Stultitia","Stultitiam":"Stultitia","Stultum":"Stultus","Suavitatis":"Suavitas","Substantiam":"Substantia","Syllabam brevem":"Brevis syllaba",
 "Syllabis":"Syllaba","Temperantiam":"Temperantia","Temporalem":"Temporalis","Temporali":"Temporalis","Ternario numero":"Ternarius numerus","Umbrae":"Umbra","Uno":"Unum","Ventum":"Ventus",
 "Verba":"Verbum","Verbis":"Verbum","Hoc verbo":"Verbum","Verborum quaestione":"Verborum quaestio","Veritatem":"Veritas","Veritatis":"Veritas","Veri simile":"Verisimile","Verisimilia":"Verisimile",
 "Versibus":"Versus","Versui":"Versus","Versum":"Versus","Versum heroicum":"Versus heroicus","Virtute":"Virtus","Virtutem":"Virtus","Visionem":"Visio","Vocabula":"Vocabulum","Vocabulis":"Vocabulum",
 "Voluptatem":"Voluptas","Errat":"Errare","Erroris":"Error","Esca":"Esca","Ferae":"Fera","Fallax":"Fallax","Mutas":"Muta","Connumeratos":"Connumeratus","Dinumeratos":"Dinumeratus","surdi":"Surdus","Muti":"Mutus",
 "Sesquati":"Sesquatus","Semipedes":"Semipes","Semivocales":"Semivocalis","Sonantes":"Sonans","Vocales":"Vocalis","Mobilia":"Mobilis","Immobilia":"Immobilis","Sensibilia":"Sensibilis","Intellegibilia":"Intellegibilis",
 "Visibilia":"Visibilis","Visibile":"Visibilis","Audibilia":"Audibilis","Significabilia":"Significabilis","Spiritalia":"Spiritalis","Carnalia":"Carnalis","Necessaria":"Necessarius","Necessarium":"Necessarius",
 "Supervacanea":"Supervacaneus","Superiora":"Superior","Rationabile":"Rationabilis","Rationale":"Rationalis","Irrationabiles":"Irrationabilis","Sensuales":"Sensualis","Monstruosa":"Monstruosus","Voluntaria":"Voluntarius",
 "Vanitantes":"Vanitans","Progressores":"Progressor","Occursores":"Occursor","Complicati":"Complicatus","Eruditi":"Eruditus","Homicidae":"Homicida","Aegrotationes":"Aegrotatio","Cubiculis":"Cubiculum",
 "Imagines":"Imago","Imagines corporum":"Imago corporum","Imaginationes":"Imaginatio","Oculi":"Oculus","Vires":"Vis","Pedes et accentus":"Pes et accentus","Principia":"Principium","Malorum ordo":"Ordo malorum",
 "Silentiorum spatia":"Silentii spatium","Spatia":"Spatium","Epitriti":"Epitritus","Paeones":"Paeon","Iudiciale nescio quid":"Iudicialis","Insignem finem versus heroici":"Finis versus heroici",
 "Ipsius sensus numerum":"Numerus sensus","Numeros qui sunt in ipsa passione aurium":"Numerus in passione aurium","Numeros qui sunt in ipso sono":"Numerus in sono","Loquendi causas":"Loquendi causa",
 "Quantitatem animi":"Quantitas animi","Vim verbi":"Vis verbi","Prosperam fortunam":"Prospera fortuna","Sabbato":"Sabbatum","Rhythmum facere":"Rhythmum facere","Mensuram et modum":"Mensura et modus",
 "Cupiditatem":"Cupiditas","Partes pedum":"Pars pedis","Pars":"Pars","Malefaciendi genere":"Malefaciendi genus","Facto malo":"Malum factum","Egestati contrarium":"Egestati contrarium",
 "Magnum vel ingentem animum":"Magnus animus", "Arborem":"Arbor","Bimembrem":"Bimembris","Imparem":"Impar","Nivem":"Nix","Quadrimembrem":"Quadrimembris","Trimembrem":"Trimembris","Summum hominis verum bonum":"Summum hominis bonum","Beatum hominis":"Beatum hominis",
}
# forme verbali → infinito
V = {"Accuset":"Accusare","Ambulat":"Ambulare","Amatur":"Amare","Credimus":"Credere","Credo":"Credere","Discit":"Discere","Discunt":"Discere","Docet":"Docere","Egeant":"Egere","Egeat":"Egere","Egens":"Egere",
 "Errat":"Errare","Fallitur":"Falli","Festinat":"Festinare","Intellego":"Intellegere","Loquimur":"Loqui","Loquitur":"Loqui","Mentitur":"Mentiri","Mentientes":"Mentiri","Novimus":"Nosse","Peccat":"Peccare",
 "Scimus":"Scire","Scit":"Scire","Scitur":"Scire","Sentimus":"Sentire","Sentiendo":"Sentire","Videat":"Videre","Videmus":"Videre","Videtur":"Videre","Vivit":"Vivere","Gignendo":"Gignere","Operando":"Operari",
 "Ratiocinando":"Ratiocinari","Resultando":"Resultare","Tangendo sentire":"Tangere","Videndo sentit":"Videre","Habet egestatem":"Habere egestatem","Cum Deo est":"Esse cum Deo","Cum Deo":"Esse cum Deo",
 "Scit se vivere":"Scire se vivere","Non latet":"Non latere","Inanescere":"Inanescere","Est":"Esse","Ambulare":"Ambulare","Dicimus":"Dicere","Tenet ordinem":"Tenere ordinem","Discernendum":"Discernere",
 "Connectendum":"Connectere","Sine Deo esse":"Esse sine Deo","Non esse sine Deo":"Esse sine Deo"}
# rinvii (pronomi, deittici): il termine non è nella frase; se c'è un'indicazione tra parentesi si usa quella
R = {"Aliquid","Eam","Ego","Eius","Eum","Haec","Hi","Hoc","Id","Illa","Illam","Illi","Ipsa","Ipso","Is","Ista","Nos","Nostra","Nostrum","Totum","Unum","Esse","Res","Haec actio","Ea quae scribuntur",
     "Illud quod vident","Quod sonat","Quod in audiente contingit","Quintum genus","Aliud genus","Hoc genus (in operatione animi)","Hoc numerorum genus","Ista nomina","Iudicialis"}
rows = []
for f in forme:
    m = re.match(r"^(.+?)\s*\((.+)\)$", f)
    if f in V: rows.append((f, V[f], "verbo"))
    elif f in N: rows.append((f, N[f], "flessione" if " " not in f else "sintagma"))
    elif m and m.group(1).strip() in R | {"Hoc","Haec","Hos","Ipsi","Huius","Illud","Eos"}: rows.append((f, m.group(2).strip().capitalize(), "rinvio"))
    elif f in R: rows.append((f, f, "rinvio"))
    else: rows.append((f, f, "identico"))
out = os.path.join(HERE, "../_dati/lemmi_definienda.tsv")
with open(out, "w", encoding="utf-8") as fh:
    fh.write("forma\tlemma\ttipo\n"); [fh.write("\t".join(r) + "\n") for r in rows]
c = collections.Counter(t for _, _, t in rows); print(len(rows), "forme →", len({l for _, l, _ in rows}), "lemmi;", dict(c))
