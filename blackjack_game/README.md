# BlackJack Game

Un semplice gioco di BlackJack implementato in Python usando Pygame.

## Requisiti
- Python 3.7+
- Pygame 2.5.2

## Installazione

1. Crea un ambiente virtuale (opzionale ma consigliato):
```bash
python -m venv venv
source venv/bin/activate  # Per Linux/Mac
venv\Scripts\activate     # Per Windows
```

2. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

## Come Giocare

Esegui il gioco con:
```bash
python main.py
```

### Controlli
- `H` - Chiedi una carta (Hit)
- `S` - Stai (Stand)
- `R` - Ricomincia la partita (quando il gioco è finito)
- `ESC` o click sulla X - Chiudi il gioco

### Regole
- L'obiettivo è battere il dealer ottenendo un punteggio più alto senza superare 21
- Le carte numeriche valgono il loro valore
- Le figure (J, Q, K) valgono 10
- L'Asso vale 11, ma se il totale supera 21, il suo valore diventa 1
- Il dealer deve pescare carte finché non raggiunge almeno 17

## Funzionalità da implementare
- Raddoppio
- Split
- Assicurazione
- Immagini reali delle carte
- Interfaccia grafica migliorata con pulsanti
- Suoni ed effetti

## Note
Questo è un progetto in sviluppo. Nuove funzionalità verranno aggiunte nelle prossime versioni. 