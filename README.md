# 🎰 Python BlackJack

Un gioco di BlackJack completo implementato in Python usando Pygame. Include tutte le funzionalità classiche del BlackJack da casinò come split, double down e assicurazione.

![BlackJack Game Screenshot](screenshots/game.png) *(Screenshot da aggiungere)*

## ✨ Caratteristiche

- 🎮 Interfaccia grafica intuitiva
- 💰 Sistema di puntate e gestione del denaro
- 🃏 Funzionalità complete di BlackJack:
  - Split (divisione delle coppie)
  - Double Down (raddoppio)
  - Insurance (assicurazione)
- 🎯 Regole standard da casinò
- 🔄 Gestione automatica del valore degli Assi (1/11)

## 🚀 Installazione

### Prerequisiti

- Python 3.7 o superiore
- pip (Python package installer)

### Passaggi per l'installazione

1. Clona il repository:
```bash
git clone https://github.com/tuousername/blackjack-game.git
cd blackjack-game
```

2. (Opzionale ma consigliato) Crea un ambiente virtuale:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Installa le dipendenze:
```bash
pip install -r requirements.txt
```

## 🎮 Come Giocare

1. Avvia il gioco:
```bash
python main.py
```

2. Controlli:
- `H` - Hit (Chiedi una carta)
- `S` - Stand (Stai)
- `D` - Double Down (Raddoppia)
- `P` - Split (Dividi le carte, disponibile solo con coppie)
- `I` - Insurance (Assicurazione, disponibile solo quando il dealer mostra un Asso)
- `R` - Restart (Ricomincia la partita)
- `ESC` o `X` - Chiudi il gioco

### Regole del Gioco

- 🎯 L'obiettivo è battere il dealer ottenendo un punteggio più alto senza superare 21
- 🔢 Le carte dal 2 al 10 valgono il loro valore nominale
- 👑 Le figure (J, Q, K) valgono 10
- 🎭 L'Asso vale 11 o 1 (il gioco gestisce automaticamente il valore ottimale)
- 🎲 Il dealer deve pescare su 16 e stare su 17

### Funzionalità Speciali

#### Double Down (Raddoppio)
- Disponibile solo sulla mano iniziale
- Raddoppia la puntata
- Ricevi una sola carta aggiuntiva

#### Split (Divisione)
- Disponibile quando hai una coppia
- Crea due mani separate
- Richiede una puntata aggiuntiva uguale alla puntata iniziale
- Ogni mano riceve una nuova carta e può essere giocata indipendentemente

#### Insurance (Assicurazione)
- Disponibile quando il dealer mostra un Asso
- Costa la metà della puntata iniziale
- Paga 2:1 se il dealer ha BlackJack

## 🛠️ Sviluppo

### Struttura del Progetto
```
blackjack-game/
│
├── main.py           # File principale del gioco
├── requirements.txt  # Dipendenze Python
└── README.md        # Questo file
```

### Tecnologie Utilizzate
- 🐍 Python 3.7+
- 🎮 Pygame 2.5.2

## 📝 Note di Sviluppo

Il gioco è stato sviluppato con un focus su:
- Codice pulito e ben organizzato
- Gestione corretta delle regole del BlackJack
- Interfaccia utente intuitiva
- Facilità di installazione e utilizzo

## 🤝 Contribuire

Sentiti libero di:
1. Fare un fork del progetto
2. Creare un branch per le tue modifiche (`git checkout -b feature/AmazingFeature`)
3. Committare le modifiche (`git commit -m 'Add some AmazingFeature'`)
4. Pushare sul branch (`git push origin feature/AmazingFeature`)
5. Aprire una Pull Request

## 📜 Licenza

Distribuito sotto la Licenza MIT. Vedi `LICENSE` per maggiori informazioni.

## 🙏 Riconoscimenti

- [Pygame](https://www.pygame.org/)
- [Python](https://www.python.org/)
- Tutti i contributori che hanno aiutato a migliorare questo progetto
