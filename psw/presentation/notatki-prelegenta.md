# Feedback — notatki prelegenta


Wersja marketingowa, bez części technologicznej. 9 slajdów, około 5 minut. Czasy są propozycją tempa wystąpienia. Schematy i hasła są redakcyjnym opracowaniem dokumentacji; nie przedstawiają działającego prototypu.


## 1. Feedback

[0:00–0:30] Feedback opiera się na prostym pomyśle: siła przeciwnika może stać się naszym następnym ruchem. Parowanie pozwala odbijać pociski, pokonywać przeszkody i rozwiązywać zagadki. Przedstawiamy koncepcję gry na podstawie dokumentów projektu.
Ilustracja jest schematem koncepcyjnym przygotowanym do prezentacji, a nie zrzutem gry. Hasło jest propozycją redakcyjną.
Źródło: feedback/deadline_3/specyfikacja/specyfikacja.tex, Wprowadzenie i Opis gry.
Grafika postaci/przeciwnika pochodzi z dostarczonego Figma Make (CharacterShowcase.tsx / PixelEnemy.tsx). Statyczne klatki SVG; schematy interakcji są opracowaniem do prezentacji. Jednego wzoru przeciwnika użyto ilustracyjnie, bez ustalania wyglądu poszczególnych typów.



## 2. Każdy atak to okazja.

[0:30–1:10] Jedna mechanika ma trzy zastosowania. Możemy oddać przeciwnikowi jego pocisk, przejąć pęd ataku fizycznego i użyć odbitego pocisku do uruchomienia elementu otoczenia. Przeciwnik jest zarówno zagrożeniem, jak i częścią rozwiązania. To opis projektowanej mechaniki, nie deklaracja ukończonej implementacji.
Źródło: specyfikacja.tex, trzy filary; req.tex, WF-03–WF-05 i WF-13.
Grafika postaci/przeciwnika pochodzi z dostarczonego Figma Make (CharacterShowcase.tsx / PixelEnemy.tsx). Statyczne klatki SVG; schematy interakcji są opracowaniem do prezentacji. Jednego wzoru przeciwnika użyto ilustracyjnie, bez ustalania wyglądu poszczególnych typów.



## 3. Zagrożenie staje się rozwiązaniem.

[1:10–1:55] Oto schemat jednej interakcji, a nie gotowy projekt poziomu. Po lewej przeciwnik wysyła pocisk w stronę gracza. W środku gracz paruje i odwraca jego kierunek. Po prawej odbity pocisk trafia przełącznik, który otwiera drzwi. Przełącznik reaguje na pocisk po odbiciu. Pozostaje przejść dalej. Ten przykład pokazuje połączenie obserwacji, timingu i zagadki.
Schemat nie ustala finalnego układu poziomów ani oprawy. Źródło: req.tex, WF-04 i WF-13.
Grafika postaci/przeciwnika pochodzi z dostarczonego Figma Make (CharacterShowcase.tsx / PixelEnemy.tsx). Statyczne klatki SVG; schematy interakcji są opracowaniem do prezentacji. Jednego wzoru przeciwnika użyto ilustracyjnie, bez ustalania wyglądu poszczególnych typów.



## 4. Sparuj. Wykorzystaj pęd.

[1:55–2:30] Drugie zastosowanie parowania to ruch. Udane sparowanie ataku fizycznego może nadać postaci pęd i pozwolić dotrzeć na wyższą lub dalszą platformę. Gracz musi więc zaplanować nie tylko moment parowania, lecz także to, gdzie chce się znaleźć po nim.
Strzałki ilustrują ideę transferu pędu; nie przedstawiają pomiaru trajektorii ani ustalonego modelu fizyki. Źródło: req.tex, WF-05; specyfikacja.tex, Manipulacja fizyką i momentum.
Grafika postaci/przeciwnika pochodzi z dostarczonego Figma Make (CharacterShowcase.tsx / PixelEnemy.tsx). Statyczne klatki SVG; schematy interakcji są opracowaniem do prezentacji. Jednego wzoru przeciwnika użyto ilustracyjnie, bez ustalania wyglądu poszczególnych typów.



## 5. Zobacz. Zaplanuj. Wykonaj.

[2:30–3:05] Chcemy, żeby każdy poziom zaczynał się od zrozumienia sytuacji, a kończył płynnym wykonaniem. Pomyłka prowadzi do szybkiej kolejnej próby. Postęp wynika z poznania zasad, rozpoznawania ataków i doskonalenia własnego timingu. Nie pokazujemy tu obiecanego czasu przejścia ani wyników playtestów.
Źródło: specyfikacja.tex, Gameplay loop i Progression loop; req.tex, WF-11.



## 6. Refleks spotyka łamigłówkę.

[3:05–3:40] Projekt kierujemy do osób, które lubią wyzwania zręcznościowe i jednocześnie szukają logicznej satysfakcji ze zrozumienia poziomu. Punkt wspólny to frajda z opanowania jednej mechaniki i odkrywania jej kolejnych zastosowań. To grupa docelowa opisana w materiałach, a nie wynik przeprowadzonych badań rynku.
Źródło: specyfikacja.tex, Użytkownicy; deadline_1/value proposition canvas.pdf.



## 7. Pierwszy obraz świata Feedback.

[3:40–4:10] To jest istniejący mockup menu oraz oryginalna postać z dostarczonego pliku Figma Make. Po prawej widzimy neutralną pozę oraz klatkę animacji parowania mieczem. To statyczne kadry odzyskanych komponentów SVG, nie przerysowane postacie. Traktujemy go jako kierunek do dalszej rozmowy, nie jako zatwierdzoną oprawę całej gry. Etykieta wersji w obrazie należy do makiety i nie oznacza wydanej wersji gry.
Źródło grafiki: Feedback mockup.make, images/00131dcf29b7204da054f6a204fc6d419a773f8a. Oryginalny obraz menu, bez zmiany treści, zachowane proporcje. Postać: CharacterShowcase.tsx, neutralna poza i pierwszy utrzymany klucz parry. Źródła SVG zapisano w assets/figma-characters/.
Grafika postaci/przeciwnika pochodzi z dostarczonego Figma Make (CharacterShowcase.tsx / PixelEnemy.tsx). Statyczne klatki SVG; schematy interakcji są opracowaniem do prezentacji. Jednego wzoru przeciwnika użyto ilustracyjnie, bez ustalania wyglądu poszczególnych typów.



## 8. Jedna mechanika. Różne wyzwania.

[4:10–4:45] Zapisany w specyfikacji zakres prototypu obejmuje co najmniej trzy poziomy, dwa typy przeciwników oraz trzy podstawowe akcje: ruch, skok i parowanie. To zakres planowany. Nie przedstawiamy tych liczb jako stanu ukończenia. Celem jest sprawdzenie, czy różne zastosowania parowania tworzą przyjemną grę.
Źródło: specyfikacja.tex, Cel projektu; req.tex, WF-01–WF-03, WF-07–WF-08 i WF-12. Aktualność zakresu pozostaje do potwierdzenia przez zespół, zgodnie z kwestionariuszem.



## 9. Feedback

[4:45–5:05] Kończymy pytaniem o najważniejszą obietnicę gry: jak wykorzystasz następny atak? Zapraszamy do pytań o koncepcję i uwag do proponowanych zastosowań parowania. Część technologiczna nie jest elementem tej wersji prezentacji. Hasło jest propozycją redakcyjną.
Zespół według dokumentów: Aleksander Bielicki, Radosław Głasek, Jakub Pączka, Michał Popkowicz, Filip Shramko, Kacper Trzciński.
Źródło koncepcji: specyfikacja.tex i req.tex. Brak deklaracji daty premiery, ceny, stanu ukończenia lub wyników testów.
Grafika postaci/przeciwnika pochodzi z dostarczonego Figma Make (CharacterShowcase.tsx / PixelEnemy.tsx). Statyczne klatki SVG; schematy interakcji są opracowaniem do prezentacji. Jednego wzoru przeciwnika użyto ilustracyjnie, bez ustalania wyglądu poszczególnych typów.

