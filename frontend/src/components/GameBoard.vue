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

      <p v-if="check">Échec!</p>
      <p v-if="checkmate">Échec et mat!</p>
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
      check: false,
      checkmate: false,
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
        if (this.board[index] && this.board[index][0] === this.turn) {
          this.selectedSquare = index;
        }
      } else {
        const validMove = this.isValidMove(this.selectedSquare, index);
        if (validMove) {
          this.board[index] = this.board[this.selectedSquare];
          this.board[this.selectedSquare] = "";
          this.selectedSquare = null;
          this.turn = this.turn === "w" ? "b" : "w";

          // Vérifier l'échec et l'échec et mat après le mouvement
          this.check = this.isKingInCheck(this.board, this.turn);
          this.checkmate = this.isCheckmate(this.board, this.turn);
        } else {
          this.selectedSquare = null;
        }
      }
    },

    // Vérifier si le mouvement est valide en fonction du type de pièce
    isValidMove(from, to) {
      const piece = this.board[from];
      const targetPiece = this.board[to];

      if (!piece) return false;

      const pieceType = piece[1];
      const pieceColor = piece[0];

      if (targetPiece && targetPiece[0] === pieceColor) {
        return false;
      }

      if (pieceType === 'p') {
        return this.isValidPawnMove(from, to, pieceColor);
      }

      if (pieceType === 'r') {
        return this.isValidRookMove(from, to);
      }

      if (pieceType === 'n') {
        return this.isValidKnightMove(from, to);
      }

      if (pieceType === 'b') {
        return this.isValidBishopMove(from, to);
      }

      if (pieceType === 'q') {
        return this.isValidQueenMove(from, to);
      }

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

      if (row1 === row2) {
        const start = Math.min(col1, col2) + 1;
        const end = Math.max(col1, col2);
        for (let i = start; i < end; i++) {
          if (this.board[row1 * 8 + i] !== "") {
            return false;
          }
        }
        return true;
      } else if (col1 === col2) {
        const start = Math.min(row1, row2) + 1;
        const end = Math.max(row1, row2);
        for (let i = start; i < end; i++) {
          if (this.board[i * 8 + col1] !== "") {
            return false;
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

    // Vérifier si le roi est en échec
    isKingInCheck(board, color) {
      const kingPosition = this.findKingPosition(board, color);
      return this.isSquareUnderAttack(board, kingPosition, color);
    },

    // Trouver la position du roi
    findKingPosition(board, color) {
      for (let i = 0; i < board.length; i++) {
        if (board[i] === `${color}k`) {
          return i;
        }
      }
      return -1;
    },

    // Vérifier si une case est sous attaque
    isSquareUnderAttack(board, squareIndex, color) {
      const opponentColor = color === 'w' ? 'b' : 'w';
      const pawnAttacks = this.getPawnAttacks(squareIndex, opponentColor);
      for (const attack of pawnAttacks) {
        if (board[attack] === `${opponentColor}p`) {
          return true;
        }
      }

      const knightAttacks = this.getKnightAttacks(squareIndex);
      for (const attack of knightAttacks) {
        if (board[attack] === `${opponentColor}n`) {
          return true;
        }
      }

      const straightAttacks = this.getStraightAttacks(squareIndex);
      const diagonalAttacks = this.getDiagonalAttacks(squareIndex);

      for (const attack of straightAttacks) {
        if (board[attack] === `${opponentColor}r` || board[attack] === `${opponentColor}q`) {
          return true;
        }
      }

      for (const attack of diagonalAttacks) {
        if (board[attack] === `${opponentColor}b` || board[attack] === `${opponentColor}q`) {
          return true;
        }
      }

      return false;
    },

    // Vérifier si c'est un échec et mat
    isCheckmate(board, color) {
      if (!this.isKingInCheck(board, color)) {
        return false;
      }

      const possibleMoves = this.generateAllMoves(board, color);

      for (const move of possibleMoves) {
        const newBoard = this.applyMove(board, move);
        if (!this.isKingInCheck(newBoard, color)) {
          return false;
        }
      }

      return true;
    },

    // Générer tous les mouvements possibles
    generateAllMoves(board, color) {
      const moves = [];
      for (let i = 0; i < board.length; i++) {
        if (board[i] && board[i][0] === color) {
          const pieceType = board[i][1];
          if (pieceType === 'p') {
            moves.push(...this.generatePawnMoves(i, color));
          } else if (pieceType === 'r') {
            moves.push(...this.generateRookMoves(i));
          } else if (pieceType === 'n') {
            moves.push(...this.generateKnightMoves(i));
          } else if (pieceType === 'b') {
            moves.push(...this.generateBishopMoves(i));
          } else if (pieceType === 'q') {
            moves.push(...this.generateQueenMoves(i));
          } else if (pieceType === 'k') {
            moves.push(...this.generateKingMoves(i));
          }
        }
      }
      return moves;
    },

    // Appliquer un mouvement à l'échiquier
    applyMove(board, move) {
      const newBoard = board.slice();
      newBoard[move.to] = newBoard[move.from];
      newBoard[move.from] = "";
      return newBoard;
    },

    // Calculer les cases attaquées par un pion
    getPawnAttacks(squareIndex, color) {
      const direction = color === 'w' ? -1 : 1;
      const col = squareIndex % 8;
      const attacks = [];

      if (col > 0) attacks.push(squareIndex - 1 + direction * 8);
      if (col < 7) attacks.push(squareIndex + 1 + direction * 8);

      return attacks;
    },

    // Calculer les cases attaquées par un cavalier
    getKnightAttacks(squareIndex) {
      const row = Math.floor(squareIndex / 8);
      const col = squareIndex % 8;
      const attacks = [];

      const moves = [
        [-2, -1], [-2, 1], [-1, -2], [-1, 2],
        [1, -2], [1, 2], [2, -1], [2, 1]
      ];

      for (const [dRow, dCol] of moves) {
        const newRow = row + dRow;
        const newCol = col + dCol;
        if (newRow >= 0 && newRow < 8 && newCol >= 0 && newCol < 8) {
          attacks.push(newRow * 8 + newCol);
        }
      }

      return attacks;
    },

    // Calculer les cases attaquées en ligne droite
    getStraightAttacks(squareIndex) {
      const row = Math.floor(squareIndex / 8);
      const col = squareIndex % 8;
      const attacks = [];

      // Attaques horizontales
      for (let c = 0; c < 8; c++) {
        if (c !== col) attacks.push(row * 8 + c);
      }

      // Attaques verticales
      for (let r = 0; r < 8; r++) {
        if (r !== row) attacks.push(r * 8 + col);
      }

      return attacks;
    },

    // Calculer les cases attaquées en diagonale
    getDiagonalAttacks(squareIndex) {
      const row = Math.floor(squareIndex / 8);
      const col = squareIndex % 8;
      const attacks = [];

      // Attaques diagonales
      for (let r = 0; r < 8; r++) {
        for (let c = 0; c < 8; c++) {
          if (Math.abs(r - row) === Math.abs(c - col)) {
            if (r !== row || c !== col) attacks.push(r * 8 + c);
          }
        }
      }

      return attacks;
    },

    // Générer tous les mouvements possibles pour un pion
    generatePawnMoves(index, color) {
      const direction = color === 'w' ? -1 : 1;
      const row = Math.floor(index / 8);
      const col = index % 8;
      const moves = [];

      // Déplacement d'une case en avant
      const targetRow = row + direction;
      if (targetRow >= 0 && targetRow < 8) {
        const targetIndex = targetRow * 8 + col;
        if (this.board[targetIndex] === "") {
          moves.push({ from: index, to: targetIndex });
        }
      }

      // Déplacement de deux cases en avant (seulement pour le premier mouvement)
      if ((color === 'w' && row === 6) || (color === 'b' && row === 1)) {
        const targetRow = row + 2 * direction;
        if (targetRow >= 0 && targetRow < 8) {
          const targetIndex = targetRow * 8 + col;
          if (this.board[targetIndex] === "" && this.board[targetRow * 8 + col - direction * 8] === "") {
            moves.push({ from: index, to: targetIndex });
          }
        }
      }

      // Capture en diagonale
      for (const offset of [-1, 1]) {
        const targetCol = col + offset;
        if (targetCol >= 0 && targetCol < 8) {
          const targetIndex = (row + direction) * 8 + targetCol;
          if (this.board[targetIndex] !== "" && this.board[targetIndex][0] !== color) {
            moves.push({ from: index, to: targetIndex });
          }
        }
      }

      return moves;
    },

    // Générer tous les mouvements possibles pour une tour
    generateRookMoves(index) {
      const row = Math.floor(index / 8);
      const col = index % 8;
      const moves = [];

      // Mouvements horizontaux
      for (let c = 0; c < 8; c++) {
        if (c !== col) {
          const targetIndex = row * 8 + c;
          if (this.board[targetIndex] === "" || this.board[targetIndex][0] !== this.board[index][0]) {
            moves.push({ from: index, to: targetIndex });
          }
        }
      }

      // Mouvements verticaux
      for (let r = 0; r < 8; r++) {
        if (r !== row) {
          const targetIndex = r * 8 + col;
          if (this.board[targetIndex] === "" || this.board[targetIndex][0] !== this.board[index][0]) {
            moves.push({ from: index, to: targetIndex });
          }
        }
      }

      return moves;
    },

    // Générer tous les mouvements possibles pour un cavalier
    generateKnightMoves(index) {
      const row = Math.floor(index / 8);
      const col = index % 8;
      const moves = [];

      const movesOffsets = [
        [-2, -1], [-2, 1], [-1, -2], [-1, 2],
        [1, -2], [1, 2], [2, -1], [2, 1]
      ];

      for (const [dRow, dCol] of movesOffsets) {
        const targetRow = row + dRow;
        const targetCol = col + dCol;
        if (targetRow >= 0 && targetRow < 8 && targetCol >= 0 && targetCol < 8) {
          const targetIndex = targetRow * 8 + targetCol;
          if (this.board[targetIndex] === "" || this.board[targetIndex][0] !== this.board[index][0]) {
            moves.push({ from: index, to: targetIndex });
          }
        }
      }

      return moves;
    },

    // Générer tous les mouvements possibles pour un fou
    generateBishopMoves(index) {
      const row = Math.floor(index / 8);
      const col = index % 8;
      const moves = [];

      // Mouvements diagonaux
      for (let r = 0; r < 8; r++) {
        for (let c = 0; c < 8; c++) {
          if (Math.abs(r - row) === Math.abs(c - col)) {
            const targetIndex = r * 8 + c;
            if (targetIndex !== index && (this.board[targetIndex] === "" || this.board[targetIndex][0] !== this.board[index][0])) {
              moves.push({ from: index, to: targetIndex });
            }
          }
        }
      }

      return moves;
    },

    // Générer tous les mouvements possibles pour une reine
    generateQueenMoves(index) {
      return [...this.generateRookMoves(index), ...this.generateBishopMoves(index)];
    },

    // Générer tous les mouvements possibles pour un roi
    generateKingMoves(index) {
      const row = Math.floor(index / 8);
      const col = index % 8;
      const moves = [];

      const movesOffsets = [
        [-1, -1], [-1, 0], [-1, 1],
        [0, -1],         [0, 1],
        [1, -1], [1, 0], [1, 1]
      ];

      for (const [dRow, dCol] of movesOffsets) {
        const targetRow = row + dRow;
        const targetCol = col + dCol;
        if (targetRow >= 0 && targetRow < 8 && targetCol >= 0 && targetCol < 8) {
          const targetIndex = targetRow * 8 + targetCol;
          if (this.board[targetIndex] === "" || this.board[targetIndex][0] !== this.board[index][0]) {
            moves.push({ from: index, to: targetIndex });
          }
        }
      }

      return moves;
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
