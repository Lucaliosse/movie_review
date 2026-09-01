import { defineStore } from 'pinia'
import api from '@/services/api'

export const useMoviesStore = defineStore('movies', {
  state: () => ({
    movies: [],
    loading: false,
    error: null,
  }),
  actions: {
    async fetchMovies() {
      this.loading = true
      this.error = null
      try {
        const response = await api.get('/movies/')
        this.movies = response.data
      } catch (error) {
        this.error = 'Failed to load movies.'
        throw error
      } finally {
        this.loading = false
      }
    },
  },
})
