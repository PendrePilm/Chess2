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
    </div>
    <div class="parameters-container">
      <h2>Paramètres</h2>
      <div class="user-info">
        <p><strong>Email :</strong> {{ userEmail }}</p>
        <p><strong>Pseudo :</strong> {{ userPseudo }}</p>
        <p><strong>Nom :</strong> {{ userNom }}</p>
        <p><strong>Prénom :</strong> {{ userPrenom }}</p>
      </div>
      <div class="change-password">
        <h3>Changer le mot de passe</h3>
        <form @submit.prevent="changePassword">
          <div class="form-group">
            <label for="newPassword">Nouveau mot de passe :</label>
            <input type="password" id="newPassword" v-model="newPassword" required />
          </div>
          <button type="submit">Changer le mot de passe</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: "ParametersChess",
    data() {
      return {
        userEmail: localStorage.getItem('userEmail'),
        userPseudo: localStorage.getItem('userPseudo'),
        userNom: localStorage.getItem('userNom'),
        userPrenom: localStorage.getItem('userPrenom'),
        newPassword: "",
      };
    },
    methods: {
      async changePassword() {
        try {
          const response = await axios.post('http://localhost:8000/change_password/', {
            email: this.userEmail,
            newPassword: this.newPassword,
          });
          alert(response.data.message);
        } catch (error) {
          console.error("Erreur lors du changement de mot de passe :", error.response ? error.response.data : error.message);
          alert("Erreur lors du changement de mot de passe. Veuillez réessayer.");
        }
      },
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
  .parameters-container {
    padding: 20px;
    max-width: 600px;
    margin: auto;
    flex-grow: 1;
    text-align: center;
  }
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
  
  .user-info {
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    margin-bottom: 5px;
    display: block;
  }
  
  input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
  }
  
  button {
    padding: 10px 15px;
    background-color: #00ff00;
    color: #121212;
    border: none;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #00cc00;
  }
  </style>
  