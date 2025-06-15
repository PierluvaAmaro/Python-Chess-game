# Manuale Utente - Scacchi da Terminale

## Indice
- [Introduzione](#introduzione)
- [Regolamento](#regolamento-degli-scacchi)
- [Notazione Algebrica](#notazione-algebrica)
  - [Concetti Base](#concetti-base)
  - [Esempi di Mosse](#esempi-di-mosse)
- [Meccaniche di gioco](#meccaniche-di-gioco)
  - [Movimento dei Pezzi](#movimento-dei-pezzi)
  - [Condizioni Speciali](#condizioni-speciali)
- [Comandi e Interfaccia da Terminale](#comandi-di-gioco)
- [Requisiti di sistema](#requisiti-di-sistema)
- [Riferimenti](#riferimenti-e-crediti)

---

## Introduzione
In questa sezione si fornisce una panoramica sul gioco degli scacchi, specificando lo scopo del manuale e come utilizzare il gioco da terminale che permette a **due giocatori** di affrontarsi a turni.

![Immagine Banner](./img/BannerMilner.png)
[Torna al menu](#indice)

---

## Regolamento degli scacchi
Il regolamento degli scacchi stabilisce le basi per una partita equa e strutturata, definendo i movimenti dei pezzi, la disposizione iniziale sulla scacchiera e le regole speciali. 
Queste norme non solo garantiscono il corretto svolgimento dell'incontro, ma offrono anche un quadro che arricchisce la strategia di ogni giocatore. Per maggiori dettagli e per consultare il regolamento completo, puoi fare riferimento al seguente documento: **[Regolamento ufficiale FIDE](https://www.arbitriscacchi.com/up_file/439-Laws_of_Chess_Italiano.pdf)**.

[Torna al menu](#indice)

---

## Notazione Algebrica

### Concetti Base
La notazione algebrica è il metodo usato dalla maggior parte dei giocatori, delle organizzazioni, delle riviste e dei libri di scacchi per registrare e descrivere le partite; è l'unico sistema ammesso dalla FIDE per la registrazione delle mosse da parte dei giocatori. Viene usata anche per registrare le partite in formato elettronico, all'interno della notazione Portable Game.
Per ulteriori approfondimenti: **[Notazione algebrica](https://it.wikipedia.org/wiki/Notazione_algebrica)**

#### Lettere dei pezzi:
- R → Re 
- D → Regina 
- T → Torre 
- A → Alfiere 
- C → Cavallo 
- I pedoni hanno la lettera P assegnata di default; si identificano solo con la colonna di destinazione, ma si può comunque specificare la lettera di appartenenza.


#### Movimento e cattura:
- x → Indica una cattura.
- O-O → Arrocco corto (il re si sposta due caselle e la torre salta accanto).
- O-O-O → Arrocco lungo (il re si sposta due caselle verso il lato della regina e la torre si posiziona accanto).
#### Stato del re:
- "+" → Indica uno scacco al re (es. Qh5+ mette il re avversario sotto scacco).
- "#" → Indica scacco matto (es. Qh5# significa che la regina ha dato scacco matto).
#### Altri simboli utili:
- = → Promozione di un pedone (es. e8=Q indica che il pedone in e8 si trasforma in regina).
- e.p. → Cattura "en passant", quando un pedone cattura un altro pedone che ha appena avanzato di due caselle (es. dxe6 ep).

### Esempi di Mosse
- e4
Il pedone della colonna "e" avanza di due caselle. È una delle aperture più comuni e porta al controllo del centro della scacchiera.
<img src=./img/e4.gif width="350" alt="Descrizione dell'immagine">
- Cf3
Il cavallo si sposta nella casella f3. Questo movimento sviluppa un pezzo verso il centro, preparandosi a controllare caselle chiave.
<img src=./img/Cf3.gif width="350" alt="Descrizione dell'immagine">
- Axe5
L’alfiere cattura un pezzo posizionato sulla casella e5. La "x" indica che c’è una cattura in corso.
<img src=./img/Axe5.gif width="350" alt="Descrizione dell'immagine">
- O-O
Arrocco corto (lato re): il re si sposta di due caselle verso la torre, e la torre "salta" sul lato opposto del re.
<img src=./img/ArroccoCorto.gif width="350" alt="Descrizione dell'immagine">
- O-O-O
Arrocco lungo (lato donna): una variante dell'arrocco in cui il re si sposta di due caselle verso la torre opposta e la torre si posiziona subito accanto al re.
<img src=./img/ArroccoLungo.gif width="350" alt="Descrizione dell'immagine">
- xd4
Il pedone cattura un pezzo sulla diagonale, occupando la casella d4. La "x" denota l’azione di cattura.
<img src=./img/xd5.gif width="350" alt="Descrizione dell'immagine">
- Dh5+
La regina si sposta in h5 e, con il simbolo "+", indica che la mossa mette in scacco il re avversario.
<img src=./img/Dh5+.gif width="350" alt="Descrizione dell'immagine">

[Torna al menu](#indice)


---

## Meccaniche di gioco
### Movimento dei pezzi 
**Il movimento dei pezzi è spiegato tramite le seguenti immagini animate.**
#### Pedone (♙ / ♟)
- Movimento: in avanti di 1 casa per volta (Seconda mossa).
- Alla prima mossa può avanzare di 2 case (Prima mossa).
<img src=./img/MPedone.gif width="350" alt="Descrizione dell'immagine">

- Cattura: in diagonale di 1 casa (non in avanti).
<img src=./img/CPedone.gif width="350" alt="Descrizione dell'immagine">

#### Torre (♖ / ♜)
- Movimento: in linea retta orizzontale o verticale per quante case vuole.
<img src=./img/MRook.gif width="350" alt="Descrizione dell'immagine">

- Cattura: nella stessa direzione di movimento.
<img src=./img/MXRook.gif width="350" alt="Descrizione dell'immagine">

#### Alfiere (♗ / ♝)
- Movimento: in diagonale, per quante case vuole.
<img src=./img/MBishop.gif width="350" alt="Descrizione dell'immagine">

- Cattura: nella stessa direzione.
<img src=./img/MXBishop.gif width="350" alt="Descrizione dell'immagine">

#### Cavallo (♘ / ♞)
- Movimento: a “L”: due case in una direzione (orizzontale o verticale), poi una casa perpendicolare.

- Salta eventuali pezzi intermedi.
<img src=./img/MKnight.gif width="350" alt="Descrizione dell'immagine">

- Cattura: nella casa di arrivo.
<img src=./img/MXKnight.gif width="350" alt="Descrizione dell'immagine">


#### Regina (♕ / ♛)
- Movimento: unisce movimento di torre e alfiere: orizzontale, verticale, o diagonale per quante case vuole.
<img src=./img/MQueen.gif width="350" alt="Descrizione dell'immagine">

- Cattura: nella stessa direzione.
<img src=./img/MXQueen.gif width="350" alt="Descrizione dell'immagine">

#### Re (♔ / ♚)
- Movimento: 1 casa in qualunque direzione.
<img src=./img/MKing.gif width="350" alt="Descrizione dell'immagine">
- Cattura: nella stessa direzione
<img src=./img/ReCattura.gif width="350" alt="Descrizione dell'immagine">


### Condizioni speciali
#### Arrocco
Coinvolge re e torre.
Il re si sposta di 2 case verso una torre, e la torre salta il re posizionandosi accanto a lui.
<img src=./img/Arrocco.gif width="350" alt="Descrizione dell'immagine">

**Condizioni per arroccare:**

- Né il re né la torre devono essersi mossi prima.

- Nessun pezzo tra re e torre.

- Il re non può essere sotto scacco, né attraversare una casa sotto attacco.

#### En passant
Quando un pedone avversario avanza di 2 case dalla sua posizione iniziale e si posiziona accanto a un tuo pedone, puoi catturarlo come se avesse fatto solo 1 passo.

Valido solo al turno immediatamente successivo.
<img src=./img/EnPassant.gif width="350" alt="Descrizione dell'immagine">

#### Promozione
Quando un pedone raggiunge l’ultima traversa (8ª riga per i bianchi, 1ª per i neri), viene promosso a un altro pezzo (regina, torre, alfiere, cavallo) a scelta del giocatore — quasi sempre regina.
<img src=./img/Promozione.gif width="350" alt="Descrizione dell'immagine">

#### Scacco e scacco matto
- Scacco: il re è sotto attacco. Devi pararlo.
<img src=./img/Scacco.gif width="350" alt="Descrizione dell'immagine">

- Scacco matto: il re è sotto attacco e non c'è modo legale per salvarlo. Finisce la partita.
<img src=./img/ScaccoMatto.gif width="350" alt="Descrizione dell'immagine">

#### Stallo 
Non è scacco matto, ma il giocatore non ha mosse legali e non è sotto scacco. La partita finisce patta (pareggio).
<img src=./img/Stallo.gif width="350" alt="Descrizione dell'immagine">

#### Mossa ambigua
A volte potrebbe capitare che due pezzi uguali del giocatore possano mangiare nella stessa casa. Per risolvere l'ambiguità, basta specificare la casa di partenza del pezzo (individuata da colonna) del pezzo che si vuole muovere, e continuare normalmente la cattura in notazione algebrica.
<img src=./img/MossaAmbigua.gif width="350" alt="Descrizione dell'immagine">

[Torna al menu](#indice)

---

## Comandi di gioco
![Comandi](./img/Comandi.png)
**Con /help, --help, -h** viene mostrata una descrizione dell’applicazione seguita dall’elenco dei comandi disponibili.

- **/gioca** → Avvia una nuova partita, mostrando la scacchiera con i pezzi nella posizione iniziale e preparando la prima mossa del bianco.
<img src=./img/Gioca1.png width="350" alt="Descrizione dell'immagine">
<img src=./img/Gioca.png width="350" alt="Descrizione dell'immagine"> 

- **/scacchiera** → Mostra la disposizione attuale dei pezzi sulla scacchiera; se la partita non è iniziata, suggerisce di usare /gioca.
<img src=./img/Scacchiera1.png width="350" alt="Descrizione dell'immagine">
<img src=./img/Scacchiera2.png width="350" alt="Descrizione dell'immagine">

- **/mosse** → Mostra la cronologia delle mosse giocate nella partita corrente, utilizzando la notazione algebrica abbreviata in italiano.
<img src=./img/Mosse1.png width="350" alt="Descrizione dell'immagine">

- **/patta** → Propone la patta all’avversario; se accettata, la partita termina con un pareggio, altrimenti il gioco continua.
<img src=./img/Patta1.png width="350" alt="Descrizione dell'immagine">
<img src=./img/Patta2.png width="350" alt="Descrizione dell'immagine">

- **/abbandona** → Permette al giocatore di abbandonare la partita; richiede conferma e, in caso positivo, dichiara la vittoria dell’avversario.
<img src=./img/Abbandona.png width="350" alt="Descrizione dell'immagine">
<img src=./img/Abbandona.png width="350" alt="Descrizione dell'immagine">

- **/esci** → Permette di chiudere l’applicazione; richiede conferma e, in caso positivo, termina il gioco restituendo il controllo al sistema operativo.
<img src=./img/Esci.png width="350" alt="Descrizione dell'immagine">
<img src=./img/Esci2.png width="350" alt="Descrizione dell'immagine">

[Torna al menu](#indice)

---

## Requisiti di sistema 
1. **L'applicazione deve essere eseguita all'interno di un container Docker.** <img src="https://img.icons8.com/fluency/48/docker.png" height="20"/>
<img src=./img/ContainerDocker.png width="400" alt="Descrizione dell'immagine">

2. **L'applicazione è compatibile con i seguenti terminali:**
- <img src="https://img.icons8.com/color/48/linux.png" height="20"/> Terminal di Linux
- <img src="https://img.icons8.com/color/48/mac-os.png" height="20"/> Terminal di macOS
- <img src="https://img.icons8.com/color/48/powershell.png" height="20"/> PowerShell di Windows
- <img src="https://img.icons8.com/color/48/git.png" height="20"/> Git Bash di Windows
3. **L'applicazione utilizza i simboli UTF-8 per la rappresentazione grafica dei pezzi degli scacchi:**
♔ ♕ ♖ ♗ ♘ ♙ | ♚ ♛ ♜ ♝ ♞ ♟

[Torna al menu](#indice)

---

## Riferimenti e Crediti

### FIDE

La Federazione internazionale degli scacchi, nota con l'acronimo francese [FIDE](https://it.wikipedia.org/wiki/Federazione_Internazionale_degli_Scacchi) (Fédération internationale des échecs), è un'organizzazione internazionale che regolamenta e controlla l'attività scacchistica a livello mondiale.
![Fide](./img/Fide.jpg)

[Torna al menu](#indice)

---