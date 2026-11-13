# Strona Detal Studio – instrukcja wdrożenia

## Co to jest

Jednostronicowa strona Detal Studio (butikowe studio kreatywne: strategia, marka, komunikacja). Cała strona to jeden plik `index.html` – zatwierdzony prototyp. Zadanie: wdrożyć go na produkcję bez zmiany wyglądu, treści i animacji, chyba że Marcin poprosi inaczej.

## Jak działa strona

- Ciemne tło, różowy akcent `#e2337f`, logo DS (inline SVG w nagłówku).
- Scena 3D na `<canvas id="stage">`, rysowana w three.js r128 (ładowane z cdnjs). Różowa linia prowadzi przez przestrzeń, kamera leci za nią przy scrollu.
- 9 scen = 9 sekcji `<section data-scene>`. Pozycja scrolla przelicza się na numer sceny (funkcja `target()`).
  1. Start – różowy punkt („Różnicę robi detal.”)
  2. Zrozumienie – chmura punktów
  3. Wzór – punkty układają się w siatkę
  4. „Z jednej myśli powstaje całość” – napis na środku
  5. Strategia – zagnieżdżone wielościany
  6. Marka – skręcona kolumna z ramek
  7. Komunikacja – fale z jednego punktu
  8. Zespół – orbity z bryłami
  9. Kontakt – chmura cząstek („materia”) i formularz
- Położenie obiektów i kamery: tablice `ST` (stacje), `MID` (zakręty linii), `OFF` (kamera), `SHIFT` (gdzie obiekt ląduje na ekranie).
- Teksty PL i EN są w obiekcie `dict` w skrypcie. Domyślny język: polski. Przełącznik zapisuje wybór w `localStorage`.
- Funkcja `nb()` wiąże w polskich tekstach jedno- i dwuliterowe słowa z następnym wyrazem. Zostawić.
- Telefon (poniżej 860 px): animacja u góry, tekst pod nią.
- `prefers-reduced-motion` wyłącza ruch otoczenia. Bez WebGL strona pokazuje same teksty.

## Zasady

- Narracja w pierwszej osobie liczby mnogiej („my”, studio).
- Język prosty, bez marketingowych ozdobników.
- Nie pokazujemy klientów ani portfolio.
- Bez WordPressa i bez frameworków. Czysty HTML, CSS i JS.
- W stopce tylko „Detal Studio · 2026” oraz to, co wymienione niżej.

## Do zrobienia

1. **Repozytorium i hosting.** Wrzucić do nowego repo na GitHubie i włączyć GitHub Pages (albo inny hosting wskazany przez Marcina). Podpiąć domenę, jeśli Marcin ją poda.
2. **Formularz.** Teraz niczego nie wysyła – po kliknięciu pokazuje tylko podziękowanie z dopiskiem „Prototyp”. Podłączyć realną wysyłkę na adres Marcina (usługa formularzy albo własny endpoint – zapytać Marcina), dodać stan błędu wysyłki i usunąć dopisek `doneNote`.
3. **Zgoda i polityka prywatności.** Dodać pod formularzem informację o przetwarzaniu danych oraz link do polityki prywatności w stopce. Treść polityki dostarczy Marcin.
4. **Meta.** Dodać opis strony, favicon z logo DS, obrazek i tagi do udostępniania (Open Graph), `hreflang` nie jest potrzebny (jedna strona, przełącznik języka w skrypcie).
5. **Czcionki i biblioteka.** Google Fonts (Instrument Serif, Geist, Geist Mono) i three.js r128 ładują się z zewnątrz. Można je zostawić albo przenieść do repo.
6. **Test na prawdziwych urządzeniach.** Płynność animacji nie była mierzona na sprzęcie z kartą graficzną. Sprawdzić na telefonie (iOS i Android) i laptopie. Jeśli przycina: zmniejszyć liczbę cząstek w finale (`MN`, teraz 14000) i limit `setPixelRatio` (teraz 2).

## Do decyzji Marcina

- Zdanie „Odpowiadamy w ciągu jednego dnia roboczego” – zostaje?
- Bryła przy „Marce” na wąskim ekranie – czy jej zarys jest w porządku.
- W scenie „Z jednej myśli…” linia przecina nagłówek, a przy „Marce” przechodzi tuż pod akapitem – zostawić czy odsunąć.
- Link „Umów 30 minut” prowadzi do Calendly: https://calendly.com/marcinraczynski/30-minutowe-spotkanie-1-na-1
