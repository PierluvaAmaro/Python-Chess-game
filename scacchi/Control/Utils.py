from ..Entity.Alfiere import Alfiere
from ..Entity.Cavallo import Cavallo
from ..Entity.Coordinata import Coordinata
from ..Entity.Pedone import Pedone
from ..Entity.Re import Re
from ..Entity.Regina import Regina
from ..Entity.Torre import Torre


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
        case "♙":
            return Pedone("♙", id, colore)
        
        case "♟":
            return Pedone("♟", id, colore)
        
        case "♖":
            return Torre("♖", id, colore)

        case "♜":
            return Torre("♜", id, colore)

        case "♘":
            return Cavallo("♘", id, colore)

        case "♞":
            return Cavallo("♞", id, colore)

        case "♔":
            return Re("♔", id, colore)

        case "♚":
            return Re("♚", id, colore)

        case "♕":
            return Regina("♕", id, colore)
        
        case "♛":
            return Regina("♛", id, colore)

        case "♗":
            return Alfiere("♗", id, colore)
        
        case "♝":
            return Alfiere("♝", id, colore)
        
        case _:
            raise ValueError(f"Pezzo non conosciuto: {simbolo}")


def leggi_scacchiera(file="scacchiera.txt"):
    """Legge la disposizione della scacchiera da un file di testo.

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

    # Usa la funzione leggi_file per leggere il contenuto del file
    contenuto = leggi_file(file)

    # Suddivide il contenuto in righe e rimuove eventuali righe vuote
    righe = [line.strip() for line in contenuto.splitlines() if line.strip()]

    if len(righe) != 8:
        raise ValueError(f"File non valido: le righe devono essere 8 ma sono: "
                         f"{len(righe)}"
                        )
    
    for y_riga, riga in enumerate(righe):
        y = 8 - y_riga

        if len(riga) != 8:
            raise ValueError(f"File non valido: le colonne devono essere 8 ma sono: " 
                             f"{len(riga)}"
                            )

        for x_col, simbolo in enumerate(riga):
            if simbolo != ".":
                x = x_col + 1

                # Determina il colore del pezzo in base alla posizione
                if y == 2 or y == 1:
                    colore = True
                elif y == 7 or y == 8:
                    colore = False
                else:
                    continue  # nessun pezzo previsto in quella casa.
                
                coord = Coordinata(x, y)
                pezzo = crea_pezzo(simbolo, coord, colore)
                scacchiera[coord] = pezzo

    return scacchiera


def leggi_file(percorso: str | None = None) -> str:
    """Legge il contenuto di un file di testo e lo restituisce come stringa.

    Args:
        percorso (str): Percorso del file da leggere.

    Returns:
        str: Contenuto del file come stringa.

    Raises:
        ValueError: Se non viene fornito alcun percorso.
        FileNotFoundError: Se il file non esiste.
        PermissionError: Se non si hanno i permessi per leggerlo.
        OSError: Per altri errori legati al file system.

    """
    if not percorso or not percorso.strip():
        raise ValueError("Nessun percorso file fornito.")

    percorso = percorso.strip()

    try:
        with open(percorso, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Errore: {e}.") from e
    
    except PermissionError as e:
        raise PermissionError(f"Errore {e}.") from e
    
    except OSError as e:
        raise OSError(f"Errore: {e}.") from e