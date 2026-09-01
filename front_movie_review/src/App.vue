<script setup></script>

<template>
  <v-app>
    <v-app-bar>
      <v-toolbar-title>
        <router-link
          :to="{ name: 'movie-list' }"
          class="text-decoration-none"
          style="color: inherit"
        >
          Movie Review
        </router-link>
      </v-toolbar-title>
    </v-app-bar>
    <v-main>
      <router-view :key="$route.fullPath" />
    </v-main>
  </v-app>
</template>
