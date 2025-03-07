<template>
    <div class="game-container">
      <aside class="sidebar">
        <nav>
          <ul>
            <li><router-link to="/menu">Accueil</router-link></li>
            <li><router-link to="/parametres">Paramètres</router-link></li>
            <li><a href="#" @click.prevent="logout">Déconnexion</a></li>
          </ul>
        </nav>
      </aside>
  
      <div class="board-container">
        <h2>Partie d'Échecs</h2>
        <p>Code de la partie : {{ gameCode }}</p>
        <p>Vous jouez les : {{ playerColor === 'w' ? 'Blancs' : 'Noirs' }}</p>
        <p>Tour actuel : {{ turn === 'w' ? 'Blancs' : 'Noirs' }}</p>
  
        <div id="chessboard" class="chessboard">
          <div 
            v-for="(piece, index) in board" 
            :key="index" 
            class="square" 
            :class="getSquareClass(index)" 
            @click="handleSquareClick(index)"
          >
            <img v-if="piece" :src="pieceImages[piece]" class="piece" />
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: "GameBoard",
    props: ['gameCode', 'playerColor'],
    data() {
      return {
        board: [],
        selectedSquare: null,
        turn: "w", // "w" = blanc, "b" = noir
        pieceImages: {
          wp: require('@/img/pions/w/pawn.png'),
          bp: require('@/img/pions/b/pawn.png'),
          wr: require('@/img/pions/w/rook.png'),
          br: require('@/img/pions/b/rook.png'),
          wn: require('@/img/pions/w/knight.png'),
          bn: require('@/img/pions/b/knight.png'),
          wb: require('@/img/pions/w/bishop.png'),
          bb: require('@/img/pions/b/bishop.png'),
          wq: require('@/img/pions/w/queen.png'),
          bq: require('@/img/pions/b/queen.png'),
          wk: require('@/img/pions/w/king.png'),
          bk: require('@/img/pions/b/king.png'),
        }
      };
    },
    created() {
      this.board = this.initializeBoard();
    },
    methods: {
      // Initialiser le plateau de jeu avec les positions des pièces
      initializeBoard() {
        if (this.playerColor === 'b') {
          // Si le joueur joue avec les noirs, on inverse les positions des pièces
          return [
            "wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr",
            "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp",
            "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "",
            "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp",
            "br", "bn", "bb", "bq", "bk", "bb", "bn", "br"
          ];
        } else {
          // Sinon, si le joueur joue avec les blancs, on garde l'ordre par défaut
          return [
            "br", "bn", "bb", "bq", "bk", "bb", "bn", "br",
            "bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp",
            "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "",
            "wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp",
            "wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"
          ];
        }
      },
  
      // Gérer le clic sur une case du plateau
      handleSquareClick(index) {
        if (this.selectedSquare === null) {
          // Sélectionner une pièce si elle appartient au joueur
          if (this.board[index] && this.board[index][0] === this.turn) {
            this.selectedSquare = index; // Sélectionner la pièce
          }
        } else {
          // Si une pièce est sélectionnée, tenter de déplacer
          const validMove = this.isValidMove(this.selectedSquare, index);
          if (validMove) {
            // Déplacer la pièce sur l'échiquier
            this.board[index] = this.board[this.selectedSquare];  // Déplacer la pièce
            this.board[this.selectedSquare] = "";  // Vider l'ancienne case
            this.selectedSquare = null;  // Désélectionner la pièce
            this.turn = this.turn === "w" ? "b" : "w"; // Changer de tour
          } else {
            // Si le mouvement n'est pas valide, désélectionner la pièce
            this.selectedSquare = null;
          }
        }
      },
  
      // Vérifier si le mouvement est valide en fonction du type de pièce
      isValidMove(from, to) {
        const piece = this.board[from];
        const targetPiece = this.board[to];
  
        // Vérifier qu'une pièce est sélectionnée
        if (!piece) return false;
  
        const pieceType = piece[1]; // Le type de la pièce (p, r, n, b, q, k)
        const pieceColor = piece[0]; // La couleur de la pièce (w pour blanc, b pour noir)
  
        // Si la pièce et la cible sont de la même couleur, c'est un mouvement invalide
        if (targetPiece && targetPiece[0] === pieceColor) {
          return false;
        }
  
        // Pion (déplacement d'une case vers l'avant, capture en diagonale)
        if (pieceType === 'p') {
          return this.isValidPawnMove(from, to, pieceColor);
        }
  
        // Tour (déplacement horizontal ou vertical)
        if (pieceType === 'r') {
          return this.isValidRookMove(from, to);
        }
  
        // Cavalier (déplacement en L)
        if (pieceType === 'n') {
          return this.isValidKnightMove(from, to);
        }
  
        // Fou (déplacement en diagonale)
        if (pieceType === 'b') {
          return this.isValidBishopMove(from, to);
        }
  
        // Reine (combinaison de la tour et du fou)
        if (pieceType === 'q') {
          return this.isValidQueenMove(from, to);
        }
  
        // Roi (déplacement d'une case dans toutes les directions)
        if (pieceType === 'k') {
          return this.isValidKingMove(from, to);
        }
  
        return false;
      },
  
      // Vérifier si un mouvement de pion est valide
      isValidPawnMove(from, to, color) {
        const direction = color === 'w' ? -1 : 1;
        const row = Math.floor(from / 8);
        const col = from % 8;
        const targetRow = Math.floor(to / 8);
        const targetCol = to % 8;
  
        // Déplacement d'une case en avant
        if (col === targetCol && targetRow === row + direction && this.board[to] === "") {
          return true;
        }
  
        // Déplacement de deux cases en avant (seulement pour le premier mouvement)
        if (col === targetCol && targetRow === row + 2 * direction && row === (color === 'w' ? 6 : 1) && this.board[to] === "" && this.board[from + direction * 8] === "") {
          return true;
        }
  
        // Capture en diagonale
        if (Math.abs(col - targetCol) === 1 && targetRow === row + direction && this.board[to] !== "" && this.board[to][0] !== color) {
          return true;
        }
  
        return false;
      },
  
      // Vérifier si un mouvement de tour est valide
      isValidRookMove(from, to) {
        const row1 = Math.floor(from / 8);
        const col1 = from % 8;
        const row2 = Math.floor(to / 8);
        const col2 = to % 8;
  
        // Déplacement horizontal ou vertical
        if (row1 === row2) {
          // Déplacement horizontal
          const start = Math.min(col1, col2) + 1;
          const end = Math.max(col1, col2);
          for (let i = start; i < end; i++) {
            if (this.board[row1 * 8 + i] !== "") {
              return false;  // Il y a une pièce dans le chemin
            }
          }
          return true;
        } else if (col1 === col2) {
          // Déplacement vertical
          const start = Math.min(row1, row2) + 1;
          const end = Math.max(row1, row2);
          for (let i = start; i < end; i++) {
            if (this.board[i * 8 + col1] !== "") {
              return false;  // Il y a une pièce dans le chemin
            }
          }
          return true;
        }
  
        return false;
      },
  
      // Vérifier si un mouvement de cavalier est valide
      isValidKnightMove(from, to) {
        const row1 = Math.floor(from / 8);
        const col1 = from % 8;
        const row2 = Math.floor(to / 8);
        const col2 = to % 8;
  
        const rowDiff = Math.abs(row1 - row2);
        const colDiff = Math.abs(col1 - col2);
  
        return (rowDiff === 2 && colDiff === 1) || (rowDiff === 1 && colDiff === 2);
      },
  
      // Vérifier si un mouvement de fou est valide
      isValidBishopMove(from, to) {
        const row1 = Math.floor(from / 8);
        const col1 = from % 8;
        const row2 = Math.floor(to / 8);
        const col2 = to % 8;
  
        return Math.abs(row1 - row2) === Math.abs(col1 - col2);
      },
  
      // Vérifier si un mouvement de reine est valide
      isValidQueenMove(from, to) {
        return this.isValidRookMove(from, to) || this.isValidBishopMove(from, to);
      },
  
      // Vérifier si un mouvement de roi est valide
      isValidKingMove(from, to) {
        const row1 = Math.floor(from / 8);
        const col1 = from % 8;
        const row2 = Math.floor(to / 8);
        const col2 = to % 8;
  
        return Math.abs(row1 - row2) <= 1 && Math.abs(col1 - col2) <= 1;
      },
  
      // Récupérer la classe CSS pour une case (pour les couleurs beige ou marron)
      getSquareClass(index) {
        const row = Math.floor(index / 8);
        const col = index % 8;
        return (row + col) % 2 === 0 ? 'beige' : 'brown';
      },
  
      // Se déconnecter de la session
      async logout() {
        try {
          await axios.post('http://localhost:8000/logout/');
          localStorage.removeItem('userPseudo');
          localStorage.removeItem('userEmail');
          localStorage.removeItem('userNom');
          localStorage.removeItem('userPrenom');
          this.$router.push('/login');
        } catch (error) {
          console.error("Erreur lors de la déconnexion :", error.response ? error.response.data : error.message);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .game-container {
    display: flex;
  }
  
  .sidebar {
    width: 200px;
    background-color: #1f1f1f;
    padding: 20px;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.5);
  }
  
  .sidebar nav ul {
    list-style-type: none;
    padding: 0;
  }
  
  .sidebar nav ul li {
    margin: 15px 0;
  }
  
  .sidebar nav ul li a {
    color: #e0e0e0;
    text-decoration: none;
  }
  
  .sidebar nav ul li a:hover {
    text-decoration: underline;
  }
  
  .board-container {
    flex-grow: 1;
    padding: 20px;
    text-align: center;
  }
  
  .chessboard {
    display: grid;
    grid-template-columns: repeat(8, 80px);
    grid-template-rows: repeat(8, 80px);
    border: 2px solid #333;
    width: 640px;
    height: 640px;
    margin: 20px auto;
  }
  
  .square {
    width: 80px;
    height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    border: 1px solid black;
    position: relative;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .square:hover {
    background-color: rgba(0, 0, 0, 0.1);
  }
  
  .square.beige {
    background-color: #f5f5dc;
  }
  
  .square.brown {
    background-color: #8b4513;
  }
  
  .square.selected {
    border: 3px solid #f39c12;
  }
  
  .piece {
    width: 60%;
    height: 60%;
    object-fit: contain;
    pointer-events: none;
  }
  </style>
  