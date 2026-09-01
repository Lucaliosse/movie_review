<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  actor: { type: Object, required: true },
  saving: { type: Boolean, default: false },
  deleting: { type: Boolean, default: false },
  errorMessage: { type: String, default: '' },
})

const emit = defineEmits(['save', 'delete'])

const editing = ref(false)
const firstName = ref(props.actor.first_name)
const lastName = ref(props.actor.last_name)

watch(
  () => props.actor,
  (actor) => {
    if (!editing.value) {
      firstName.value = actor.first_name
      lastName.value = actor.last_name
    }
  },
)

watch(
  () => props.saving,
  (saving, wasSaving) => {
    if (wasSaving && !saving && !props.errorMessage) editing.value = false
  },
)

function startEditing() {
  firstName.value = props.actor.first_name
  lastName.value = props.actor.last_name
  editing.value = true
}

function cancel() {
  editing.value = false
  firstName.value = props.actor.first_name
  lastName.value = props.actor.last_name
}

function save() {
  emit('save', { first_name: firstName.value, last_name: lastName.value })
}
</script>

<template>
  <v-list-item>
    <div v-if="!editing" class="d-flex align-center justify-space-between">
      <span>{{ actor.first_name }} {{ actor.last_name }}</span>
      <div>
        <v-btn
          icon="mdi-pencil"
          size="x-small"
          variant="text"
          aria-label="Edit actor"
          @click="startEditing"
        />
        <v-btn
          icon="mdi-delete"
          size="x-small"
          variant="text"
          color="error"
          :loading="deleting"
          aria-label="Delete actor"
          @click="emit('delete')"
        />
      </div>
    </div>
    <div v-else>
      <div class="d-flex align-center flex-wrap" style="gap: 8px">
        <v-text-field
          v-model="firstName"
          label="First name"
          density="compact"
          hide-details
          style="max-width: 160px"
          autofocus
        />
        <v-text-field
          v-model="lastName"
          label="Last name"
          density="compact"
          hide-details
          style="max-width: 160px"
        />
        <v-btn
          icon="mdi-check"
          size="small"
          color="primary"
          :loading="saving"
          aria-label="Save actor"
          @click="save"
        />
        <v-btn
          icon="mdi-close"
          size="small"
          variant="text"
          :disabled="saving"
          aria-label="Cancel"
          @click="cancel"
        />
      </div>
      <div v-if="errorMessage" class="text-error text-caption mt-1">{{ errorMessage }}</div>
    </div>
  </v-list-item>
</template>
