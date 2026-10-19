# Feedback — otwarty przegląd technologii

Stan: 19.10.2026. **Brak rekomendacji końcowej i brak wybranego silnika.** Ten dokument zastępuje wcześniejszą roboczą hipotezę wyboru Godota. Kolejnym krokiem jest [kwestionariusz zespołu](kwestionariusz-wyboru-silnika.md).

Zespół zna dobrze C# i Rust; część osób pracowała z Unreal Engine, a część zrobiła małe gry w Bevy około rok temu. To oznacza, że Bevy i Unreal mają rzeczywiste atuty wynikające z doświadczenia, a Unity i Godot C# mogą wykorzystać znany język. Nie znamy jeszcze rozkładu kompetencji, aktualnych wymagań ani preferencji autorów poziomów.

## Dokumenty i ich znaczenie

Przejrzano 9 PDF-ów, źródła LaTeX, Business Model Canvas oraz teksty arkusza XLSX. Harmonogram odczytano z eksportu PDF; nie parsowano osobno binarnego MPP. Dostarczony plik `.make` przeanalizowano jako archiwum.

| Materiały | Co wnoszą do rozmowy |
|---|---|
| Karta projektu, VPC, BMC | Parowanie i zagadki; zespół 6 osób; budżet pieniężny 0 zł. Starsze określenie roguelike. |
| WBS i harmonogram | Podział prac; zapis o kreatorze poziomów; planowane terminy. |
| Prezentacja inwestorska i starszy Beamer | Istniejący pitch, ale także niepotwierdzone twierdzenia marketingowe i stare role. |
| Specyfikacja i wymagania | Platformówka 2D; 3 poziomy, 2 typy przeciwników; Windows 10/11; 60 FPS, wejście do 50 ms, reset do 1 s; determinizm. Aktualność trzeba potwierdzić. |
| Ludzie i komunikacja | Role, kanały, przeglądy. Macierz umiejętności nie daje pełnego obrazu kompetencji silnikowych. |
| Plan i rejestr ryzyk | Ryzyka balansu, silnika, wydajności i dostępności zespołu; zapis o wczesnej próbie technicznej. |
| Figma Make | Odzyskany obraz menu 2560 × 2160 i fragmenty TSX; referencja wizualna, bez potwierdzenia istnienia kompletnej gry. |

## Czterej kandydaci do omówienia

Kolejność nie jest rankingiem. Koszty organizacyjne to kwestie do sprawdzenia w tym zespole, nie benchmarki.

| Silnik | Co zespół może wykorzystać | Narzędzia i możliwości | Co trzeba sprawdzić |
|---|---|---|---|
| Unity | Znajomość C# | Edytor, sprite'y, tilemapy, animacje, fizyka 2D, UI | Czy ktoś zna workflow Unity; czas nauki, pakiety, współpraca na scenach |
| Bevy | Znajomość Rust i wcześniejsze małe gry | ECS, 2D/3D, modularne pluginy; workflow oparty na kodzie | Wersje starych projektów, zgodność pluginów, autorstwo poziomów, UI, eksport i kompilacja |
| Unreal | Faktyczne doświadczenie części osób | Blueprints/C++, Paper 2D; sceny i narzędzia 3D/2.5D | Zakres doświadczenia, pipeline 2D, praca na zasobach i docelowy sprzęt |
| Godot | Możliwość użycia C# | Węzły 2D, edytor scen, TileMapLayer, Resources, UI | Doświadczenie w silniku, workflow .NET i eksporty; nauka modelu scen |

Źródła: [Unity 2D](https://docs.unity3d.com/Manual/Unity2D.html), [Bevy Introduction](https://bevy.org/learn/quick-start/introduction/), [stan rozwoju Bevy](https://bevy.org/news/bevys-sixth-birthday/), [Paper 2D](https://dev.epicgames.com/documentation/unreal-engine/paper-2d-in-unreal-engine?application_version=5.2), [Godot CharacterBody2D](https://docs.godotengine.org/en/stable/classes/class_characterbody2d.html), [TileMapLayer](https://docs.godotengine.org/en/stable/classes/class_tilemaplayer.html).

Porównanie konkretnych gier 2D z parowaniem, odbijaniem pocisków i zagadkami oraz ich silników opisuje osobny [przegląd gier rynkowych](porownanie-gier-rynkowych.md). Najbliższe potwierdzone przykłady wskazują Unity (*Nine Sols*, *Blasphemous 2*) i GameMaker (*Katana ZERO*); przykłady Bevy są mniej zbliżone do gatunku, ale potwierdzają wydawanie gier z walką i poziomami na Steamie. Wniosek zawęża sensowną próbę do Unity i Bevy, nie wybiera silnika.

**Unreal i 2D:** tak, jest to obsługiwany scenariusz. Trzeba ocenić, czy doświadczenie zespołu i potrzebne narzędzia równoważą koszty konkretnego workflow. Sam wymiar gry nie wyklucza silnika.

**Bevy i doświadczenie sprzed roku:** to wartościowy punkt startowy. Nie zakładamy konieczności migracji. Najpierw ustalamy wersję, potrzebne funkcje, kompatybilny zestaw dodatków oraz możliwość wykorzystania istniejącej wiedzy. Oficjalny edytor jest rozwijany; alternatywą do tworzenia poziomów może być np. LDtk z importerem. [Bevy Setup](https://bevy.org/learn/quick-start/getting-started/setup/), [bevy_ecs_ldtk](https://github.com/Trouv/bevy_ecs_ldtk).

## Inne technologie dostępne na rynku

| Technologia | Charakter | Potencjalna zaleta | Koszt do uwzględnienia |
|---|---|---|---|
| GameMaker | Silnik/edytor 2D, GML | Zintegrowana produkcja 2D | Nauka GML; licencja komercyjna, jeśli potrzebna |
| Defold | Silnik i edytor, Lua | Workflow 2D i bezpłatny runtime | Nauka Lua i modelu silnika |
| Phaser | Framework JS/TS | Gry przeglądarkowe i znany workflow webowy | Edycja poziomów i opakowanie desktopu wymagają decyzji |
| GDevelop | Edytor z systemem zdarzeń | Prototypowanie wizualne | Sprawdzenie precyzyjnego ruchu i aktualnych limitów usług |
| Construct 3 | Edytor przeglądarkowy, zdarzenia/JS | Szybka praca wizualna | Ograniczenia darmowej wersji; koszt pełnego planu |
| MonoGame | Framework C# | Znany język i duża kontrola | Własna organizacja poziomów, narzędzi i pipeline'u |
| LÖVE | Framework Lua | Mały zestaw narzędzi do 2D | Dobór narzędzi i więcej własnej infrastruktury |
| Własny silnik / SDL | Biblioteki niskiego poziomu | Pełna kontrola i walor dydaktyczny | Duży zakres infrastruktury do utrzymania |

Te opcje nie są odrzucone. W kwestionariuszu skupiamy się na czterech wskazanych wyżej, ponieważ odpowiadają aktualnej rozmowie o kompetencjach i kandydatach.

Źródła: [GameMaker FAQ](https://gamemaker.io/en/help/articles/gamemaker-faq), [Defold FAQ](https://defold.com/faq/faq/), [Phaser](https://docs.phaser.io/phaser/getting-started/what-is-phaser), [GDevelop](https://gdevelop.io/pricing), [Construct](https://www.construct.net/en/make-games/buy-construct), [MonoGame](https://monogame.net/), [LÖVE](https://love2d.org/).

## Licencje bez wybierania modelu biznesowego

| Silnik | Zasady istotne do sprawdzenia |
|---|---|
| Godot | MIT; wymagane informacje licencyjne przy dystrybucji silnika |
| Bevy | Do wyboru MIT lub Apache 2.0; osobno licencje zależności |
| Unity | Personal przy spełnieniu warunków, w tym progu 200 tys. USD przychodu i finansowania w poprzednich 12 miesiącach; Runtime Fee anulowano |
| Unreal | Standardowe tantiemy dla gier: 5% od kwalifikującego się przychodu ponad pierwszy 1 mln USD przychodu produktu; wyłączenia i programy mogą zmieniać rozliczenie |

Źródła: [Godot](https://godotengine.org/license/), [Bevy](https://github.com/bevyengine/bevy), [Unity plany](https://unity.com/products), [Unity Runtime Fee](https://unity.com/products/pricing-updates), [Unreal](https://www.unrealengine.com/license). Te informacje nie zakładają, że gra będzie sprzedawana.

## Ryzyka wspólne dla kandydatów

- **Parry:** potrzebuje zdefiniowanego okna czasowego, kolejności rozstrzygnięcia trafień i cooldownu; nie ustalamy teraz liczby ticków ani długości okna.
- **Pęd:** trzeba pogodzić zatrzymanie zwykłego ruchu po puszczeniu klawisza z zachowaniem impulsu po parry. Ustalić wpływ grawitacji i sterowania w powietrzu.
- **Odbicia:** odwrócenie kierunku pocisku i odbicie według normalnej powierzchni to różne reguły. Specyfikacja używa obu w różnych sytuacjach.
- **Determinizm:** stały tick, Rust czy ECS nie stanowią automatycznej gwarancji. Najpierw trzeba ustalić znaczenie wymagania i test. Godot wprost ostrzega o niedeterministyczności fizyki. [Godot physics](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.html).
- **Szybkie pociski:** końcowy overlap może ominąć hitbox; sposób sprawdzania całej drogi pocisku zależy od warstwy kolizji.
- **Reset:** musi przywracać cały stan poziomu, nie tylko pozycję gracza.
- **Pomiar wejścia:** profiler nie mierzy sam fizycznego naciśnięcia → widocznej reakcji. Procedura musi odpowiadać wymaganiu.
- **Tworzenie treści:** osoba odpowiedzialna za poziomy i balans powinna sprawdzić cały workflow, nie tylko obejrzeć demo programisty.

## Niespójności do potwierdzenia przed prezentacją

1. Starsze materiały mówią roguelike, nowsza specyfikacja opisuje platformówkę z projektowanymi poziomami.
2. Karta i wcześniejszy pitch podają 180 roboczogodzin; BMC i harmonogram 450 h pracy. Harmonogram rozróżnia też czas trwania 240 h.
3. Karta przewiduje finalizację w styczniu 2027, szczegółowy harmonogram kończy projekt 2 marca 2027. Dokumenty komunikacji dodatkowo nie są spójne co do semestru implementacji.
4. Starsze slajdy przypisują rolę Głównego Użytkownika Aleksandrze Sobótce, nowsze materiały Tomaszowi Hermanowi.
5. Zapis o własnym kreatorze poziomów może oznaczać osobny produkt albo tylko potrzebę edycji map — trzeba to wyjaśnić.
6. W pliku Figma odzyskano obraz menu oraz fragmenty kodu, w tym skróty `... existing code ...`; nie potwierdzono kompletnej aplikacji do uruchomienia offline. React/TSX nie przenosi automatycznie mechanik do żadnego z czterech silników.
7. Nie ma podstaw, by przedstawiać jako wyniki badań twierdzenia o nasyceniu rynku, gotowym modelu biznesowym czy gwarancji sukcesu.

Przygotowano osobny pitch marketingowy (`feedback-pitch.pdf` / `feedback-pitch.pptx`) na podstawie dokumentów i mockupu. Część technologiczna pozostaje otwarta; kwestionariusz służy do ustalenia wyboru przed jej dodaniem.
