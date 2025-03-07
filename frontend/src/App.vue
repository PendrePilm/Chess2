<template>
  <div id="app">
    <header>
      <img src="@/img/logo.png" alt="Logo" class="logo" />
      <span v-if="userPseudo" class="user-pseudo">{{ userPseudo }}</span>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      userPseudo: localStorage.getItem('userPseudo'),
    };
  },
  watch: {
    // Observe les changements de route pour mettre à jour le pseudo
    '$route'() {
      this.userPseudo = localStorage.getItem('userPseudo');
    },
  },
};
</script>

<style>
body {
  background-color: #121212;
  color: #e0e0e0;
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}

header {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background-color: #1f1f1f;
  border-bottom: 1px solid #333;
}

header .logo {
  height: 40px;
  margin-right: 10px;
}

header h1 {
  color: #e0e0e0;
  margin: 0;
}

.user-pseudo {
  font-weight: bold;
  color: #e0e0e0;
}

main {
  padding: 20px;
}

a {
  color: #bb86fc;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
