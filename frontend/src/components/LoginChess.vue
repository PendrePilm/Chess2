<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>Connexion</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="email">Email :</label>
          <input type="email" id="email" v-model="email" required />
        </div>
        <div class="form-group">
          <label for="password">Mot de passe :</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit">Se connecter</button>
      </form>
      <p>
        Pas encore de compte ? <router-link to="/signup">S'inscrire</router-link>
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
      password: "",
    };
  },
  methods: {
  async login() {
    try {
      const response = await axios.post('http://localhost:8000/login/', {
        email: this.email,
        password: this.password,
      });
      // Stocker toutes les informations dans le localStorage
      localStorage.setItem('userPseudo', response.data.pseudo);
      localStorage.setItem('userEmail', response.data.email);
      localStorage.setItem('userNom', response.data.nom);
      localStorage.setItem('userPrenom', response.data.prenom);
      this.$router.push('/menu');
    } catch (error) {
      console.error("Erreur de connexion :", error.response ? error.response.data : error.message);
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
  background-color: rgba(0, 0, 0, 1); /* Cadre noir avec opacité */
  border: 2px solid #00ff00; /* Bordure fluo verte */
  box-shadow: 0 0 15px #00ff00, 0 0 30px #00ff00; /* Ombre lumineuse */
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
  color: #e0e0e0; 
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
