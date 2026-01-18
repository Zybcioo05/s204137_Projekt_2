Autor: Jakub Zybert <br>

Project title: Projekt 2 informatyka <br>

1. Zasada Działania Systemu (Logika Wodna)
•	Ciągły Przepływ (Rzeka): Woda nie czeka, aż zbiornik się napełni. Jeśli wlewasz wodę do Z1, ona natychmiast przelatuje do Z2, potem do Z3 itd., o ile pozwalają na to poziomy rur i zawory.
•	Równoległość: Wszystkie rury działają jednocześnie. Możesz mieć sytuację, w której woda jednocześnie wpada do Z2 i z niego wypada.
•	Brak mieszania temperatur: Temperatura wody w zbiorniku zależy wyłącznie od Twojego ustawienia suwaka (nie zmienia się przez dolanie zimnej wody z innego zbiornika).
2. Poziomy Rur (Geometria)
1.	Z1 ➔ Z2: Rura jest na dnie (0%). Woda spływa do ostatniej kropli.
2.	Z2 ➔ Z3: Rura jest zamontowana na wysokości 10%.
o	Jeśli poziom wody spadnie poniżej 10%, przepływ ustaje (tzw. "martwa strefa" na dnie).
3.	Z3 ➔ Z4 (Przelew): Rura jest zamontowana wysoko, na 70%.
o	Zbiornik Z3 działa jak bufor. Woda zaczyna lecieć do Z4 dopiero, gdy Z3 napełni się w ponad 70%.
4.	Z4 ➔ Z1 (Pompa): Rura ssąca na dnie (0%).
3. Instrukcja Obsługi Interfejsu
A. Zawory (Interaktywne)
•	Na rurach widoczne są symbole zaworów (kokardki).
•	Kliknij myszką na zawór, aby go przełączyć.
•	Zielony: Otwarty (woda płynie).
•	Czerwony: Zamknięty (blokada przepływu, nawet jeśli pompa działa).
B. Suwaki Poziomu (Górny suwak pod każdym zbiornikiem)
•	Pozwalają ręcznie ustawić ilość wody w zbiorniku (0% - 100%).
•	Suwaki te "żyją" – jeśli woda przepływa automatycznie, suwaki same się przesuwają, pokazując aktualny stan.
C. Suwaki Temperatury (Dolny suwak pod każdym zbiornikiem)
•	Ustawiają kolor wody w danym zbiorniku i w rurze, która z niego wychodzi.
•	Lewo (20°C): Kolor niebieski.
•	Prawo (100°C): Kolor czerwony.
•	Wpływają też na to, czy grzałka wewnątrz zbiornika (przerywana linia) zmieni kolor na czerwony (aktywna > 50°C).
D. Przycisk START / STOP
•	Włącza lub zamraża czas w symulacji.
4. Pompa (Automatyka)
Pompa przy zbiorniku Z4 (Odbiór) działa w trybie automatycznym z histerezą:
•	Włącza się sama, gdy w Z4 jest > 50 litrów.
•	Wyłącza się sama, gdy w Z4 zostanie < 5 litrów.
•	Uwaga: Nawet jeśli pompa pracuje (kręci się na zielono), woda nie popłynie, jeśli zamkniesz ręcznie zawór V4 na rurze powrotnej.
5. Logi (Zakładka po prawej)
Rejestrują kluczowe zdarzenia:
•	Włączenie/Wyłączenie procesu.
•	Każde kliknięcie w zawór (Otwarcie/Zamknięcie).
•	Alarmy o przepełnieniu zbiorników.<br>

