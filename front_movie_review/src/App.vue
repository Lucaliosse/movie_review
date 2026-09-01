<script setup></script>

<template>
  <v-app>
    <v-app-bar title="Movie Review" />
    <v-main>
      <router-view :key="$route.fullPath" />
    </v-main>
  </v-app>
</template>
