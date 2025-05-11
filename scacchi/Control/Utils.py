from Entity.Coordinata import Coordinata
from Entity.Pedone import Pedone


def crea_pezzo(simbolo: str, id: Coordinata, colore: bool):
    """Crea un oggetto Pezzo corrispondente al simbolo e al colore specificato.

    Args:
        simbolo (str): Simbolo del pezzo da creare.
        id (Coordinata): Coordinata iniziale del pezzo.
        colore (int): Colore del pezzo da creare (0 = nero, 1 = bianco).
    
    Returns:
        Pezzo: Oggetto derivato dalla classe Pezzo (es. Pedone).

    Raises:
        ValueError: Se il simbolo non corrisponde a un pezzo riconosciuto.

    """
    match simbolo:
        case "♟":
            return Pedone("♟", id, colore)

        case _:
            raise ValueError(f"Pezzo non conosciuto: {simbolo}")

def leggi_scacchiera(file="scacchiera.txt"):
    """Legge la disposizione della tastiera da un file di testo.

    Il file deve contenere 8 righe da 8 caratteri ciascuna, dove ogni simbolo 
    rappresenta un pezzo. I punti (.) indicano caselle vuote. I pezzi vengono associati 
    a un colore in base alla riga.

    Args:
        file (str): Percorso del file da cui leggere la disposizione.
    
    Returns:
        dict[Coordinata, Pezzo]: Dizionario che associa una Coordinata a un Pezzo.

    Raises:
        ValueError: Se il file non contiene esattamente 8 righe o se una riga non 
        contiene 8 colonne.
    
    """
    scacchiera = {}

    with open(file) as f:
        righe = [line.strip() for line in f.readlines() if line.strip()]

    if len(righe) != 8:
        raise ValueError(f"File non valido: le righe devono essere 8 ma sono: "
                         f"{len.righe}"
                        )
    
    for y_riga, riga in enumerate(righe):
        y = 8 - y_riga

        if len(riga) != 8:
            raise ValueError(f"File non valido: le colonne devono essere 8 ma sono"
                             f"{len(riga)}"
                            )

        for x_col, simbolo in enumerate(riga):
            if simbolo != ".":
                x = x_col + 1

                # determina il colore del pezzo in base alla posizione
                if y == 2 or y == 1:
                    colore = True # colore bianco
                elif y == 7 or y == 8:
                    colore = False # colore nero
                else:
                    continue # nessun pezzo previsto in quella casa.
                
                coord = Coordinata(x, y)
                pezzo = crea_pezzo(simbolo, coord, colore)
                scacchiera[coord] = pezzo

    return scacchiera
