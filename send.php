<?php
// Wysyłka formularza kontaktowego Detal Studio (zgodne ze starszymi wersjami PHP)
const RECIPIENT = 'marcin@detalstudio.pl';
const SENDER    = 'marcin@detalstudio.pl';

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

function out($code, $ok) {
    http_response_code($code);
    echo json_encode(array('ok' => $ok));
    exit;
}
function field($key, $max) {
    $v = isset($_POST[$key]) && is_string($_POST[$key]) ? trim($_POST[$key]) : '';
    return function_exists('mb_substr') ? mb_substr($v, 0, $max, 'UTF-8') : substr($v, 0, $max);
}
function oneLine($v) {
    return trim(preg_replace('/[\r\n\t]+/', ' ', $v));
}

if (!isset($_SERVER['REQUEST_METHOD']) || $_SERVER['REQUEST_METHOD'] !== 'POST') out(405, false);

// pole-pułapka: wypełniają je tylko boty; udajemy sukces
if (field('website', 200) !== '') out(200, true);

$name    = oneLine(field('name', 120));
$email   = oneLine(field('email', 200));
$company = oneLine(field('company', 160));
$topic   = oneLine(field('topic', 200));
$message = field('message', 5000);
$lang    = field('lang', 2) === 'en' ? 'EN' : 'PL';

if ($name === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) out(422, false);

$body = "Imię i nazwisko: $name\n"
      . "E-mail: $email\n"
      . 'Firma: ' . ($company !== '' ? $company : '–') . "\n"
      . 'Temat: ' . ($topic !== '' ? $topic : '–') . "\n"
      . "Język strony: $lang\n\n"
      . ($message !== '' ? $message : '(bez wiadomości)') . "\n";

$subject = '=?UTF-8?B?' . base64_encode("Zapytanie ze strony: $name") . '?=';
$headers = implode("\r\n", array(
    'From: Detal Studio <' . SENDER . '>',
    'Reply-To: ' . $email,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
));

$sent = @mail(RECIPIENT, $subject, $body, $headers);
out($sent ? 200 : 500, $sent);
