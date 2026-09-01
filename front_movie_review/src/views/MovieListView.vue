<script setup>
import { onMounted } from 'vue'
import { useMoviesStore } from '@/stores/movies'

const moviesStore = useMoviesStore()

onMounted(() => {
  moviesStore.fetchMovies()
})
</script>

<template>
  <v-container>
    <h1 class="text-h4 mb-4">Movies</h1>

    <v-alert v-if="moviesStore.error" type="error" class="mb-4">
      {{ moviesStore.error }}
    </v-alert>

    <div v-if="moviesStore.loading" class="d-flex justify-center py-8">
      <v-progress-circular indeterminate color="primary" />
    </div>

    <v-row v-else>
      <v-col v-for="movie in moviesStore.movies" :key="movie.id" cols="12" sm="6" md="4">
        <v-card>
          <v-card-title>{{ movie.title }}</v-card-title>
          <v-card-text>
            <p>{{ movie.description }}</p>
            <div class="mt-2">
              <v-chip
                v-for="actor in movie.actors"
                :key="actor.id"
                size="small"
                class="mr-1 mb-1"
              >
                {{ actor.first_name }} {{ actor.last_name }}
              </v-chip>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
