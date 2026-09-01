import { defineStore } from 'pinia'
import api from '@/services/api'

export const useMoviesStore = defineStore('movies', {
  state: () => ({
    movies: [],
    moviesCount: 0,
    pageSize: 5,
    currentPage: 1,
    loading: false,
    error: null,
    currentMovie: null,
    currentMovieLoading: false,
    currentMovieError: null,
  }),
  actions: {
    async fetchMovies(page = 1) {
      this.loading = true
      this.error = null
      try {
        const response = await api.get('/movies/', { params: { page } })
        this.movies = response.data.results
        this.moviesCount = response.data.count
        this.currentPage = page
      } catch (error) {
        this.error = 'Failed to load movies.'
        throw error
      } finally {
        this.loading = false
      }
    },

    async fetchMovie(id) {
      this.currentMovieLoading = true
      this.currentMovieError = null
      try {
        const response = await api.get(`/movies/${id}/`)
        this.currentMovie = response.data
      } catch (error) {
        this.currentMovieError = 'Failed to load movie.'
        throw error
      } finally {
        this.currentMovieLoading = false
      }
    },

    async createMovie(data) {
      const response = await api.post('/movies/', data)
      return response.data
    },

    async updateMovie(id, data) {
      await api.patch(`/movies/${id}/`, data)
      await this.fetchMovie(id)
    },

    async deleteMovie(id) {
      await api.delete(`/movies/${id}/`)
      this.currentMovie = null
    },

    async addActor(movieId, data) {
      await api.post('/actors/', { ...data, movie_id: movieId })
      await this.fetchMovie(movieId)
    },

    async updateActor(movieId, actorId, data) {
      await api.put(`/actors/${actorId}/`, data)
      await this.fetchMovie(movieId)
    },

    async deleteActor(movieId, actorId) {
      await api.delete(`/actors/${actorId}/`)
      await this.fetchMovie(movieId)
    },

    async addReview(movieId, grade) {
      await api.post('/reviews/', { grade, movie: movieId })
      await this.fetchMovie(movieId)
    },
  },
})
