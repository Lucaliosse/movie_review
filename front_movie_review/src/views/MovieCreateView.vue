<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMoviesStore } from '@/stores/movies'

const router = useRouter()
const moviesStore = useMoviesStore()

const title = ref('')
const description = ref('')
const titleError = ref('')
const submitting = ref(false)

async function submit() {
  submitting.value = true
  titleError.value = ''
  try {
    const movie = await moviesStore.createMovie({
      title: title.value,
      description: description.value,
    })
    router.push({ name: 'movie-detail', params: { id: movie.id } })
  } catch (error) {
    titleError.value = error.response?.data?.title?.[0] ?? 'Failed to create movie.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <v-container>
    <v-btn :to="{ name: 'movie-list' }" prepend-icon="mdi-arrow-left" variant="text" class="mb-2">
      Back to movies
    </v-btn>

    <h1 class="text-h4 mb-4">Create movie</h1>

    <v-form style="max-width: 480px" @submit.prevent="submit">
      <v-text-field
        v-model="title"
        label="Title"
        :error-messages="titleError"
        required
        class="mb-2"
      />
      <v-textarea v-model="description" label="Description" auto-grow class="mb-2" />
      <v-btn type="submit" color="primary" :loading="submitting">Create</v-btn>
    </v-form>
  </v-container>
</template>
