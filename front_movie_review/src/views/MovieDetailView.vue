<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMoviesStore } from '@/stores/movies'
import EditableText from '@/components/EditableText.vue'
import ActorListItem from '@/components/ActorListItem.vue'

const route = useRoute()
const router = useRouter()
const moviesStore = useMoviesStore()

const movieId = computed(() => Number(route.params.id))
const movie = computed(() => moviesStore.currentMovie)

onMounted(() => {
  moviesStore.fetchMovie(movieId.value)
})

function fieldErrorMessage(error, field) {
  return error.response?.data?.[field]?.[0] ?? `Failed to save ${field}.`
}

// Title
const titleSaving = ref(false)
const titleError = ref('')

async function saveTitle(value) {
  titleSaving.value = true
  titleError.value = ''
  try {
    await moviesStore.updateMovie(movieId.value, { title: value })
  } catch (error) {
    titleError.value = fieldErrorMessage(error, 'title')
  } finally {
    titleSaving.value = false
  }
}

// Description
const descriptionSaving = ref(false)
const descriptionError = ref('')

async function saveDescription(value) {
  descriptionSaving.value = true
  descriptionError.value = ''
  try {
    await moviesStore.updateMovie(movieId.value, { description: value })
  } catch (error) {
    descriptionError.value = fieldErrorMessage(error, 'description')
  } finally {
    descriptionSaving.value = false
  }
}

// Delete movie
const deleteDialog = ref(false)
const deletingMovie = ref(false)

async function confirmDeleteMovie() {
  deletingMovie.value = true
  try {
    await moviesStore.deleteMovie(movieId.value)
    router.push({ name: 'movie-list' })
  } catch {
    deletingMovie.value = false
    deleteDialog.value = false
  }
}

// Existing actors
const actorSaving = reactive({})
const actorErrors = reactive({})
const actorDeleting = reactive({})

async function saveActor(actor, data) {
  actorSaving[actor.id] = true
  actorErrors[actor.id] = ''
  try {
    await moviesStore.updateActor(movieId.value, actor.id, data)
  } catch {
    actorErrors[actor.id] = 'Failed to save actor.'
  } finally {
    actorSaving[actor.id] = false
  }
}

async function deleteActor(actor) {
  actorDeleting[actor.id] = true
  try {
    await moviesStore.deleteActor(movieId.value, actor.id)
  } catch {
    actorDeleting[actor.id] = false
  }
}

// New actor
const addingActor = ref(false)
const newActorFirstName = ref('')
const newActorLastName = ref('')
const addActorSaving = ref(false)
const addActorError = ref('')

function startAddingActor() {
  newActorFirstName.value = ''
  newActorLastName.value = ''
  addActorError.value = ''
  addingActor.value = true
}

function cancelAddingActor() {
  addingActor.value = false
}

async function submitNewActor() {
  addActorSaving.value = true
  addActorError.value = ''
  try {
    await moviesStore.addActor(movieId.value, {
      first_name: newActorFirstName.value,
      last_name: newActorLastName.value,
    })
    addingActor.value = false
  } catch {
    addActorError.value = 'Failed to add actor.'
  } finally {
    addActorSaving.value = false
  }
}

// Review
const reviewGrade = ref(0)
const reviewSubmitting = ref(false)
const reviewError = ref('')
const reviewSuccess = ref(false)

async function submitReview() {
  if (!reviewGrade.value) {
    reviewError.value = 'Please select a rating.'
    return
  }
  reviewSubmitting.value = true
  reviewError.value = ''
  reviewSuccess.value = false
  try {
    await moviesStore.addReview(movieId.value, reviewGrade.value)
    reviewSuccess.value = true
    reviewGrade.value = 0
  } catch {
    reviewError.value = 'Failed to submit review.'
  } finally {
    reviewSubmitting.value = false
  }
}
</script>

<template>
  <v-container v-if="moviesStore.currentMovieLoading">
    <div class="d-flex justify-center py-8">
      <v-progress-circular indeterminate color="primary" />
    </div>
  </v-container>

  <v-alert v-else-if="moviesStore.currentMovieError" type="error" class="ma-4">
    {{ moviesStore.currentMovieError }}
  </v-alert>

  <v-container v-else-if="movie">
    <div class="d-flex align-start justify-space-between">
      <EditableText
        :model-value="movie.title"
        label="Title"
        heading
        :saving="titleSaving"
        :error-message="titleError"
        class="flex-grow-1"
        @save="saveTitle"
      />
      <v-btn
        icon="mdi-delete"
        color="error"
        variant="tonal"
        class="ml-2 mt-1"
        aria-label="Delete movie"
        @click="deleteDialog = true"
      />
    </div>

    <div class="d-flex align-center mb-6 mt-1">
      <template v-if="movie.average_review !== null">
        <v-rating
          :model-value="movie.average_review"
          readonly
          half-increments
          density="compact"
          color="amber"
        />
        <span class="ml-2 text-body-2">
          {{ movie.average_review.toFixed(1) }} / 5 ({{ movie.review_count }} review{{
            movie.review_count === 1 ? '' : 's'
          }})
        </span>
      </template>
      <span v-else class="text-body-2 text-medium-emphasis">No reviews yet</span>
    </div>

    <h2 class="text-h6 mb-1">Description</h2>
    <EditableText
      :model-value="movie.description"
      label="Description"
      textarea
      :saving="descriptionSaving"
      :error-message="descriptionError"
      class="mb-6"
      @save="saveDescription"
    />

    <h2 class="text-h6 mb-1">Actors</h2>
    <v-list class="mb-2">
      <ActorListItem
        v-for="actor in movie.actors"
        :key="actor.id"
        :actor="actor"
        :saving="!!actorSaving[actor.id]"
        :deleting="!!actorDeleting[actor.id]"
        :error-message="actorErrors[actor.id] || ''"
        @save="(data) => saveActor(actor, data)"
        @delete="() => deleteActor(actor)"
      />
    </v-list>

    <v-btn
      v-if="!addingActor"
      icon="mdi-plus"
      color="success"
      size="small"
      aria-label="Add actor"
      @click="startAddingActor"
    />
    <div v-else>
      <div class="d-flex align-center flex-wrap" style="gap: 8px">
        <v-text-field
          v-model="newActorFirstName"
          label="First name"
          density="compact"
          hide-details
          style="max-width: 160px"
          autofocus
        />
        <v-text-field
          v-model="newActorLastName"
          label="Last name"
          density="compact"
          hide-details
          style="max-width: 160px"
        />
        <v-btn
          icon="mdi-check"
          size="small"
          color="primary"
          :loading="addActorSaving"
          aria-label="Save new actor"
          @click="submitNewActor"
        />
        <v-btn
          icon="mdi-close"
          size="small"
          variant="text"
          :disabled="addActorSaving"
          aria-label="Cancel"
          @click="cancelAddingActor"
        />
      </div>
      <div v-if="addActorError" class="text-error text-caption mt-1">{{ addActorError }}</div>
    </div>

    <h2 class="text-h6 mt-8 mb-1">Leave a review</h2>
    <div class="d-flex align-center flex-wrap" style="gap: 8px">
      <v-rating v-model="reviewGrade" hover length="5" color="amber" />
      <v-btn color="primary" :loading="reviewSubmitting" @click="submitReview">Submit</v-btn>
    </div>
    <v-alert v-if="reviewError" type="error" density="compact" class="mt-2" max-width="400">
      {{ reviewError }}
    </v-alert>
    <v-alert v-if="reviewSuccess" type="success" density="compact" class="mt-2" max-width="400">
      Review submitted!
    </v-alert>

    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Delete movie?</v-card-title>
        <v-card-text>
          This will permanently delete "{{ movie.title }}" and all its reviews. Its actors will
          not be deleted.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" :loading="deletingMovie" @click="confirmDeleteMovie">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>
