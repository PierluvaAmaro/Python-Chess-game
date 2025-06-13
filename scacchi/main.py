from .Control.Partita import Partita


def main():
    """Avvia il gioco degli scacchi e attiva il workflow GH."""
    partita = Partita()

    while True:
        try:
            partita.verifica()
        except Exception as e:
            print(f"Errore: {e} Riprova.")
        
if __name__ == "__main__":
    main()