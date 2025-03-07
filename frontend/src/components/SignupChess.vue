<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Inscription</h2>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="email">Email :</label>
          <input type="email" id="email" v-model="email" required />
        </div>
        <div class="form-group">
          <label for="pseudo">Pseudo :</label>
          <input type="text" id="pseudo" v-model="pseudo" required />
        </div>
        <div class="form-group">
          <label for="nom">Nom :</label>
          <input type="text" id="nom" v-model="nom" required />
        </div>
        <div class="form-group">
          <label for="prenom">Prénom :</label>
          <input type="text" id="prenom" v-model="prenom" required />
        </div>
        <div class="form-group">
          <label for="password">Mot de passe :</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit">S'inscrire</button>
      </form>
      <p>
        Déjà un compte ? <router-link to="/login">Se connecter</router-link>
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: "",
      pseudo: "",
      nom: "",
      prenom: "",
      password: "",
    };
  },
  methods: {
  async register() {
    try {
      const dataToSend = {
        email: this.email,
        pseudo: this.pseudo,
        nom: this.nom,
        prenom: this.prenom,
        password: this.password,
      };
      console.log("Données d'inscription envoyées :", dataToSend);

      const response = await axios.post('http://localhost:8000/register/', dataToSend);
      alert(response.data.message);
    } catch (error) {
      console.error("Erreur d'inscription :", error.response ? error.response.data : error.message);
      alert("Erreur lors de l'inscription. Veuillez réessayer.");
    }
  },
},
};
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-image: url('@/img/fondSite.jpg');
  background-size: cover;
  background-position: center;
}

.auth-card {
  background-color: rgba(0, 0, 0, 1); 
  border: 2px solid #00ff00; 
  box-shadow: 0 0 15px #00ff00, 0 0 30px #00ff00; 
  padding: 20px;
  border-radius: 8px;
  width: 300px;
}

.auth-card h2 {
  text-align: center;
  color: #e0e0e0;
}

form {
  display: flex;
  flex-direction: column;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 15px;
}

label {
  margin-bottom: 5px;
  color: #e0e0e0;
}

input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #1f1f1f; /* Fond des inputs pour les rendre visibles */
  color: #e0e0e0; /* Couleur du texte dans les inputs */
}

button {
  padding: 10px;
  background-color: #00ff00;
  color: #121212;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #00cc00;
}

a {
  color: #bb86fc;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>

