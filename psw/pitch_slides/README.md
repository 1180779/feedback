# Feedback — prezentacja marketingowa

Gotowy materiał do przeglądu: **9 slajdów po polsku, około 5 minut**. Zawiera propozycję opowieści marketingowej o mechanice gry. Część technologiczna pozostaje poza tą wersją.

- [PDF do pokazania offline](feedback-pitch.pdf)
- [Edytowalny PowerPoint](feedback-pitch.pptx)
- [Podgląd wszystkich slajdów](feedback-pitch-preview.png)
- [Notatki prelegenta](notatki-prelegenta.md) — również w sekcji notatek PPTX
- [Kwestionariusz wyboru silnika](kwestionariusz-wyboru-silnika.md) — osobny materiał

## Przebieg

1. Hook: „Siła przeciwnika. Twój następny ruch”.
2. Trzy zastosowania parowania: odbicie, pęd, interakcja z otoczeniem.
3. Storyboard: sprowokuj atak → sparuj → otwórz przejście.
4. Przejęcie pędu jako narzędzie ruchu.
5. Obserwacja → plan → wykonanie → kolejna próba.
6. Odbiorca: połączenie refleksu i zagadek.
7. Istniejący mockup menu z Figma Make.
8. Planowany zakres prototypu zapisany w specyfikacji.
9. Zamknięcie i pytania.

## Na czym opiera się treść

Podstawą są `feedback/deadline_3/specyfikacja/specyfikacja.tex`, `req.tex` oraz Value Proposition Canvas. Dokładniejsze odwołania są w notatkach każdego slajdu. Nie dodano deklaracji premiery, ceny, wybranego silnika, postępu implementacji ani wyników badań rynku. Nie wykorzystano niezgodnych estymacji czasu ze starszych dokumentów.

Hasła marketingowe i układ slajdów są propozycjami redakcyjnymi. Wszystkie schematy są koncepcyjne i tak podpisane. Liczby na slajdzie 8 pochodzą ze specyfikacji i są opisane jako plan; aktualność zakresu jest do potwierdzenia przez zespół.

Obraz `assets/figma-menu.png` odzyskano z dostarczonego `Feedback mockup.make`. Zachowano jego treść i proporcje. Etykieta wersji w obrazie jest częścią makiety, a nie potwierdzeniem wydanej gry. Postać i przeciwnik na schematach pochodzą z oryginalnych komponentów Figma Make: `CharacterShowcase.tsx` i `PixelEnemy.tsx`. Użyto nieruchomych póz spoczynku i parowania, z zachowaniem geometrii i kolorów. W scenach z atakiem z lewej postać jest odbita poziomo. Strzałki, mapy i schematy pozostają ilustracją koncepcji; nie ustalają docelowej oprawy gry. Na slajdzie 7 pokazano oba kadry postaci obok menu. Historia pochodzenia znajduje się w `assets/figma-characters/PROVENANCE.md`.

## Edycja i odtworzenie

Teksty i diagramy PPTX są natywnymi elementami, które można edytować. Obraz menu oraz postacie są rastrowe; oryginalne wektory postaci zachowano w `assets/figma-characters/`. Font: Lato; w PDF font jest osadzony. Jeżeli komputer do edycji nie ma Lato, edytor może podstawić inny font i zmienić łamanie tekstu.

Odzyskanie postaci (potrzebne tylko przy ponownym tworzeniu assetów) używa standardowej biblioteki Pythona; render PNG wymaga Inkscape:

```sh
python3 presentation/src/extract_figma_characters.py
inkscape presentation/assets/figma-characters/player-idle.svg --export-type=png
inkscape presentation/assets/figma-characters/player-parry.svg --export-type=png
inkscape presentation/assets/figma-characters/enemy.svg --export-type=png
```

Generator PPTX używa wyłącznie standardowej biblioteki Pythona:

```sh
python3 presentation/src/build_marketing_deck.py
```

Eksport PDF odczytuje elementy z PPTX i renderuje je przez lokalne Pycairo:

```sh
python3 presentation/src/export_pitch_pdf.py
```

PDF sprawdzono wizualnie na wszystkich 9 stronach, a skrypt sprawdza granice tekstu i kształtów. Sprawdzono również XML, relacje i obecność notatek w pakiecie PPTX. Tutejszy LibreOffice nie uruchomił eksportu w dostępnym środowisku; wygląd PPTX po otwarciu w PowerPoint/Impress nie został osobno zweryfikowany. PDF jest sprawdzoną wersją do prezentacji.
