<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: { type: String, required: true },
  label: { type: String, default: '' },
  textarea: { type: Boolean, default: false },
  heading: { type: Boolean, default: false },
  saving: { type: Boolean, default: false },
  errorMessage: { type: String, default: '' },
})

const emit = defineEmits(['save'])

const editing = ref(false)
const draft = ref(props.modelValue)

watch(
  () => props.modelValue,
  (value) => {
    if (!editing.value) draft.value = value
  },
)

watch(
  () => props.saving,
  (saving, wasSaving) => {
    if (wasSaving && !saving && !props.errorMessage) editing.value = false
  },
)

function startEditing() {
  draft.value = props.modelValue
  editing.value = true
}

function cancel() {
  editing.value = false
  draft.value = props.modelValue
}

function save() {
  emit('save', draft.value)
}
</script>

<template>
  <div>
    <div v-if="!editing" class="d-flex align-start" style="gap: 4px">
      <component :is="heading ? 'h1' : 'p'" :class="heading ? 'text-h4' : 'text-body-1'" class="mb-0">
        {{ modelValue }}
      </component>
      <v-btn
        icon="mdi-pencil"
        size="x-small"
        variant="text"
        :aria-label="`Edit ${label}`"
        @click="startEditing"
      />
    </div>
    <div v-else class="d-flex align-start flex-wrap" style="gap: 8px">
      <v-textarea
        v-if="textarea"
        v-model="draft"
        :label="label"
        :error-messages="errorMessage"
        auto-grow
        density="compact"
        class="flex-grow-1"
        style="min-width: 240px"
        autofocus
      />
      <v-text-field
        v-else
        v-model="draft"
        :label="label"
        :error-messages="errorMessage"
        density="compact"
        class="flex-grow-1"
        style="min-width: 200px"
        autofocus
        @keyup.enter="save"
      />
      <v-btn
        icon="mdi-check"
        size="small"
        color="primary"
        :loading="saving"
        aria-label="Save"
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
  </div>
</template>
