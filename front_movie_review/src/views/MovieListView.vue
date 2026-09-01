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
    <div class="d-flex align-center justify-space-between mb-4">
      <h1 class="text-h4">Movies</h1>
      <v-btn :to="{ name: 'movie-create' }" color="primary" prepend-icon="mdi-plus">
        Create movie
      </v-btn>
    </div>

    <v-alert v-if="moviesStore.error" type="error" class="mb-4">
      {{ moviesStore.error }}
    </v-alert>

    <div v-if="moviesStore.loading" class="d-flex justify-center py-8">
      <v-progress-circular indeterminate color="primary" />
    </div>

    <v-row v-else>
      <v-col v-for="movie in moviesStore.movies" :key="movie.id" cols="12" sm="6" md="4">
        <v-card
          :title="movie.title"
          :to="{ name: 'movie-detail', params: { id: movie.id } }"
        >
          <v-card-text>
            <div class="d-flex align-center mb-2">
              <template v-if="movie.average_review !== null">
                <v-rating
                  :model-value="movie.average_review"
                  readonly
                  half-increments
                  density="compact"
                  size="small"
                  color="amber"
                />
                <span class="ml-2 text-body-2">{{ movie.average_review.toFixed(1) }}</span>
              </template>
              <span v-else class="text-body-2 text-medium-emphasis">No reviews yet</span>
            </div>
            <div class="text-body-2 text-medium-emphasis">
              <v-icon icon="mdi-account-multiple" size="small" class="mr-1" />
              {{ movie.actor_count }} actor{{ movie.actor_count === 1 ? '' : 's' }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
