<?php
/**
 * La Folie Boulart — réception des demandes de réservation.
 *
 * Reçoit le JSON envoyé par assets/js/reservation.js et transmet la demande
 * par courriel. À activer en renseignant l'attribut data-endpoint du module :
 *
 *     <div class="resa" data-resa data-endpoint="reservation.php" ...>
 *
 * (voir build/pages_resa.py). Ce fichier n'a d'effet que sur un hébergement
 * PHP : sur GitHub Pages, le module bascule sur un envoi par messagerie.
 */

declare(strict_types=1);

const DESTINATAIRE = 'contact@lafolieboulart.com';
const EXPEDITEUR   = 'site@lafolieboulart.com';   // doit appartenir au domaine
const SUJET        = 'Demande de réservation — La Folie Boulart';

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Méthode non autorisée']);
    exit;
}

$brut = file_get_contents('php://input');
$data = json_decode($brut, true);

if (!is_array($data)) {
    http_response_code(400);
    echo json_encode(['error' => 'Requête illisible']);
    exit;
}

/** Nettoie une valeur : chaîne courte, sans retour chariot parasite. */
function propre($valeur, int $max = 500): string
{
    $v = is_scalar($valeur) ? (string) $valeur : '';
    $v = str_replace(["\r", "\0"], '', trim($v));
    return mb_substr($v, 0, $max);
}

$champs = [
    'arrivee'   => propre($data['arrivee']   ?? '', 10),
    'depart'    => propre($data['depart']    ?? '', 10),
    'nuits'     => propre($data['nuits']     ?? '', 4),
    'adultes'   => propre($data['adultes']   ?? '', 3),
    'enfants'   => propre($data['enfants']   ?? '', 3),
    'occasion'  => propre($data['occasion']  ?? '', 80),
    'prenom'    => propre($data['prenom']    ?? '', 80),
    'nom'       => propre($data['nom']       ?? '', 80),
    'email'     => propre($data['email']     ?? '', 120),
    'telephone' => propre($data['telephone'] ?? '', 40),
    'message'   => propre($data['message']   ?? '', 4000),
];

// Contrôles minimaux, identiques à ceux du formulaire.
$manquants = [];
foreach (['arrivee', 'depart', 'prenom', 'nom', 'email'] as $requis) {
    if ($champs[$requis] === '') {
        $manquants[] = $requis;
    }
}
if (!filter_var($champs['email'], FILTER_VALIDATE_EMAIL)) {
    $manquants[] = 'email';
}
if ($manquants) {
    http_response_code(422);
    echo json_encode(['error' => 'Champs manquants', 'champs' => array_values(array_unique($manquants))]);
    exit;
}

$corps = <<<TEXTE
Nouvelle demande de réservation reçue depuis le site.

SÉJOUR
  Arrivée   : {$champs['arrivee']}
  Départ    : {$champs['depart']}
  Durée     : {$champs['nuits']} nuit(s)
  Voyageurs : {$champs['adultes']} adulte(s), {$champs['enfants']} enfant(s)
  Occasion  : {$champs['occasion']}

DEMANDEUR
  Nom       : {$champs['prenom']} {$champs['nom']}
  E-mail    : {$champs['email']}
  Téléphone : {$champs['telephone']}

MESSAGE
{$champs['message']}

--
Envoyé le {$_SERVER['REQUEST_TIME']} depuis lafolieboulart.com
TEXTE;

// L'expéditeur reste le domaine (SPF/DKIM) ; le client est en Reply-To.
$entetes = [
    'From: La Folie Boulart <' . EXPEDITEUR . '>',
    'Reply-To: ' . $champs['prenom'] . ' ' . $champs['nom'] . ' <' . $champs['email'] . '>',
    'Content-Type: text/plain; charset=UTF-8',
    'X-Mailer: PHP/' . PHP_VERSION,
];

$envoye = mail(
    DESTINATAIRE,
    '=?UTF-8?B?' . base64_encode(SUJET) . '?=',
    $corps,
    implode("\r\n", $entetes)
);

if (!$envoye) {
    http_response_code(500);
    echo json_encode(['error' => 'L’envoi a échoué']);
    exit;
}

echo json_encode(['ok' => true]);
