<script setup lang="ts">
// import { idText } from 'typescript';
import { defineEmits, onMounted } from 'vue'

const props = defineProps(['id', 'name', 'category', 'stock', 'notes'])

const emit = defineEmits(['getItems', 'updateItem'])

async function deleteItem() {
  console.log('deleteItem: ', props.id)
  try {
    const params = {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: props.id,
      }),
    }
    const response = await fetch('http://localhost:5000/delete_item', params)
    if (!response.ok) {
      throw new Error(`Reponse status: ${response.status}`)
    }
    emit('getItems')
  } catch (e) {
    console.error(`Error deleting ${props.name}:`, e)
    console.log(e)
  }
}

onMounted(() => {
  console.log('ItemRow mounted')
  console.log(props)
})
</script>

<template>
  <tr>
    <th>
      {{ name }}
    </th>
    <td>{{ category }}</td>
    <td>
      <div class="input-group" style="width: 5em">
        <input
          id="stock"
          class="form-control"
          style="text-align: center"
          :placeholder="stock"
          disabled
          readonly
        />
      </div>
    </td>
    <td>{{ notes }}</td>
    <td>
      <button type="button" class="btn btn-outline-info btn-sm" @click="$emit('updateItem', id)">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          fill="currentColor"
          class="bi bi-pencil-square"
          viewBox="0 0 16 16"
          style="display: inline-block; vertical-align: -0.125em"
        >
          <path
            d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"
          />
          <path
            fill-rule="evenodd"
            d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"
          />
        </svg>
      </button>
    </td>
  </tr>
</template>
