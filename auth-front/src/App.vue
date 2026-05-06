<template>
  <div style="background: grey; padding: 50px;">
    <h1>AUTH-API</h1>
    <router-link to="/auth/registration">Registrarse</router-link> | 
    <router-link to="/login">Ir a Login</router-link>
    
    <hr />
    
    <router-view v-slot="{ Component }">
      <component :is="Component" />
    </router-view>
  </div>
</template>