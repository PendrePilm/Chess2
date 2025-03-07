<template>
  <div class="menu-container">
    <aside class="sidebar">
      <nav>
        <ul>
          <li><router-link to="/menu">Accueil</router-link></li>
          <li><router-link to="/parametres">Paramètres</router-link></li>
          <li><a href="#" @click.prevent="logout">Déconnexion</a></li>
        </ul>
      </nav>
    </aside>
    <div class="content">
      <h1>Menu Principal</h1>
      <p>Bienvenue dans le menu principal de votre application Chess !</p>
      <button><router-link to="/play">Jouer</router-link></button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "MenuChess",
  methods: {
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
    },
  },
};
</script>

<style scoped>
.menu-container {
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

.content {
  flex-grow: 1;
  padding: 20px;
  text-align: center;
}

button {
  padding: 10px 20px;
  background-color: #00ff00;
  color: #121212;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-top: 20px;
}

button:hover {
  background-color: #00cc00;
}
</style>
