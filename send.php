<?php
// Wysyłka formularza kontaktowego Detal Studio
declare(strict_types=1);

const RECIPIENT = 'marcin@detalstudio.pl';
const SENDER    = 'marcin@detalstudio.pl';

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

function out(int $code, bool $ok): void {
    http_response_code($code);
    echo json_encode(['ok' => $ok]);
    exit;
}
function field(string $key, int $max): string {
    $v = isset($_POST[$key]) && is_string($_POST[$key]) ? trim($_POST[$key]) : '';
    return mb_substr($v, 0, $max);
}
function oneLine(string $v): string {
    return trim(preg_replace('/[\r\n\t]+/', ' ', $v));
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') out(405, false);

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
$headers = implode("\r\n", [
    'From: Detal Studio <' . SENDER . '>',
    'Reply-To: ' . $email,
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
]);

$sent = @mail(RECIPIENT, $subject, $body, $headers);
out($sent ? 200 : 500, $sent);
