import numpy as np

class Node:
    """
        Node jest to klasa A*
        rodzic jest rodzicem bieżącego węzła
        pozycja to bieżąca pozycja węzła w labiryncie
        g to koszt od początku do bieżącego węzła
        h jest szacowanym kosztem heurystycznym bieżącego węzła do końca węzła
        f to całkowity koszt węzła  f = g + h
    """
    def __init__(self, rodzic=None, pozycja=None):
        self.rodzic = rodzic
        self.pozycja = pozycja

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, inna):
        return self.pozycja == inna.pozycja

# Ta funkcja zwraca ścieżkę wyszukiwania
def zwroc_sciezke(obecny_node, labirynt):
    sciezka = []
    no_rows, no_columns = np.shape(labirynt)
    #tutaj tworzymy zainicjowany labirynt wynikowy z -1 w każdej pozycji
    wynik = [[-1 for i in range(no_columns)] for j in range(no_rows)]
    current = obecny_node
    while current is not None:
        sciezka.append(current.pozycja)
        current = current.rodzic
    # Zwracamy tutaj odwróconą ścieżkę, ponieważ musimy pokazywać ścieżkę od początku do końca
    sciezka = sciezka[::-1]
    start_value = 0
    # aktualizujemy ścieżkę od początku do końca znalezioną przez wyszukiwanie A* z każdym krokiem o 1
    for i in range(len(sciezka)):
        wynik[sciezka[i][0]][sciezka[i][1]] = start_value
        start_value += 1
    return wynik


def search(labirynt, koszt, start, koniec):
    """
        Zwraca listę krotek jako ścieżkę od podanego początku do podanego końca w danym labiryncie
        :param labirynt:
        :param koszt
        :param start:
        :param koniec:
        :return:
    """

    # Tworzymy węzeł początkowy i końcowy z zainicjowanymi wartościami dla g, h i f
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    koniec_node = Node(None, tuple(koniec))
    koniec_node.g = koniec_node.h = koniec_node.f = 0

    # Inicjuję listę do odwiedzenia oraz listę, która została odwiedzona
    # na tej liście umieszczam wszystkie węzły nie_odziwiedzona_lista do eksploracji.
    # Tutaj znajdziemy węzeł o najniższym koszcie, który należy rozwinąć w następnej kolejności
    nie_odziwiedzona_lista = []
    # na tej liście umieszczam wszystkie węzły już zbadane, zeby nie eksplorować go ponownie
    odwiedzona_lista = []

    # Dodaje węzeł początkowy
    nie_odziwiedzona_lista.append(start_node)

    # Dodaje warunke zatrzymania. Uniknięcie nieskończonej pętli i zatrzymanie.
    outer_iteracja = 0
    max_iteracja = (len(labirynt) // 2) ** 10

    # Szukamy po kwadratach. Zaczynam wyszukiwania w kolejności lewy-prawy-górny-dolny
    # (4 ruchy) z kazdej pozycji

    idz = [[-1, 0],  # gora
            [0, -1],  # lewa
            [1, 0],  # dol
            [0, 1]]  # prawa

    """
        1) Najpierw uzyskuje bieżący węzeł, porównując wszystkie koszty f i wybierając węzeł o najniższym koszcie do dalszej rozbudowy.
        2) Sprawdzam, czy osiągnięto maksymalną iterację, czy nie. Ustawiam wiadomość i zatrzymanie wykonywania.
        3) Usuwam wybrany węzeł z listy nie odwiedzonej i dodaje ten węzeł do listy odwiedzanych
        4) Testuje i zwracam ścieżkę i potem robie poniższe kroki
        5) Dla wybranego węzła znajduje wszystkie children (użyj idz, aby znaleźć child)
            5.1) pobierz bieżącą pozycję dla wybranego noda (staje się on węzłem nadrzędnym dla children)
            5.2) jeśli jakikolwiek węzeł jest ścianą, zignoruj go
            5.3 dodaj do prawidłowej listy węzłów potomnych  wybranego rodzica

            Dla węzłów potomnych
            1) jeśli dziecko na liście odwiedzanych, zignoruj ​​je i spróbuj następnego węzła
            2) oblicz wartości g, h i f węzła potomnego
            3) Jeśli child jest na liście yet_to_visit list zignoguj to
            4) w przeciwnym razie przenies child na liste yet_to_visit 
    """
    # sprawdz ile labirynt ma  wierszy i kolumn
    no_rows, no_columns = np.shape(labirynt)

    # sprawdzam do konca

    while len(nie_odziwiedzona_lista) > 0:

        # Za każdym razem, gdy dowolny węzeł jest odsyłany z listy yet_to_visit, zwiększana jest operacja
        outer_iteracja += 1

        # pobierama bierzący węzeł
        obecny_node = nie_odziwiedzona_lista[0]
        obecny_index = 0
        for index, item in enumerate(nie_odziwiedzona_lista):
            if item.f < obecny_node.f:
                obecny_node = item
                obecny_index = index

        # jeśli osiągniemy punkt, zwróć ścieżkę, ponieważ może to nie być rozwiązanie
        # lub koszt obliczeń jest zbyt wysoki
        if outer_iteracja > max_iteracja:
            print("giving up on pathfinding too many iterations")
            return zwroc_sciezke(obecny_node, labirynt)

        # Usuń bieżący węzeł z listy yet_to_visit, dodaj do listy odwiedzanych
        nie_odziwiedzona_lista.pop(obecny_index)
        odwiedzona_lista.append(obecny_node)

        # sprawdź, czy cel został osiągnięty, czy nie, jeśli tak, zwróć ścieżkę
        if obecny_node == koniec_node:
            return zwroc_sciezke(obecny_node, labirynt)

        # Generuje children ze wszystkich sąsiednich kwadratów.
        children = []

        for nowa_pozycja in idz:

            # pobieram pozycje noda
            node_pozycja = (obecny_node.pozycja[0] + nowa_pozycja[0], obecny_node.pozycja[1] + nowa_pozycja[1])

            # Sprawdzam zasięg (czy mieści sie w granicach labiryntu)
            if (node_pozycja[0] > (no_rows - 1) or
                    node_pozycja[0] < 0 or
                    node_pozycja[1] > (no_columns - 1) or
                    node_pozycja[1] < 0):
                continue

            # sprawdzam czy moge chodzic po tym terenie
            if labirynt[node_pozycja[0]][node_pozycja[1]] != 0:
                continue

            # tworze nowy node
            nowy_node = Node(obecny_node, node_pozycja)

            children.append(nowy_node)

        for child in children:

            # Jeśli child jest na liście odwiedzanych przeszukuje cala liste od poczatktu odwiedzona_lista
            if len([visited_child for visited_child in odwiedzona_lista if visited_child == child]) > 0:
                continue

            # tworze wartosci f, g, h
            child.g = obecny_node.g + koszt
            # Obliczam koszty heurestyczne (odlegosc eukledyjska)
            child.h = (((child.pozycja[0] - koniec_node.pozycja[0]) ** 2) +
                       ((child.pozycja[1] - koniec_node.pozycja[1]) ** 2))

            child.f = child.g + child.h

            # child jest już na liście yet_to_visit, a koszt g jest już niższy
            if len([i for i in nie_odziwiedzona_lista if child == i and child.g > i.g]) > 0:
                continue

            # dodaje dziecko do listy nie_odziwiedzona_lista
            nie_odziwiedzona_lista.append(child)


if __name__ == '__main__':
    labirynt = [[0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 1, 0]]

    start = [0, 0]
    koniec = [4, 5]
    koszt = 1

    sciezka = search(labirynt, koszt, start, koniec)
    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in sciezka]))
    print("\n")

   # print(sciezka)