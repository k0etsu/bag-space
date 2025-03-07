<script setup lang="ts">
import { onMounted, ref, unref, toRaw } from 'vue'
import ItemRow from './ItemRow.vue'

const rows = ref([])
const categories = ref(new Set())
const editItem = ref({})
const newItem = ref({
  name: '',
  category: '',
  stock: 0,
  notes: '',
})

async function getItems() {
  try {
    const response = await fetch('http://localhost:5000/get_items')
    if (!response.ok) {
      throw new Error(`Reponse status: ${response.status}`)
    }
    rows.value = await response.json();
    categories.value = new Set();
    for (const row of rows.value) {
      // categories.value.push(row.category)
      categories.value.add(row.category);
    };
    console.log(categories.value);
    // console.log(rows.value);
  } catch (e) {
    console.error('Error fetching data:', e)
    console.log(e)
  }
}

function handleUpdateItem(id: number) {
  console.log('handleUpdateItem: ', id)
  for (const row of rows.value) {
    if (row.id === id) {
      console.log(row)
      editItem.value = structuredClone(toRaw(row))
    }
  }
  let modalEl = document.getElementById('updateItemModal')
  let modal = bootstrap.Modal.getOrCreateInstance(modalEl)
  modal.show()
}

async function updateItem() {
  const obj = unref(editItem)
  console.log('updateItem: ', obj)
  try {
    const params = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: obj.id,
        type: 'update',
        name: obj.name,
        category: obj.category,
        stock: obj.stock,
        notes: obj.notes,
      }),
    }
    const response = await fetch('http://localhost:5000/update_item', params)
    if (!response.ok) {
      throw new Error(`Reponse status: ${response.status}`)
    }
    let modalEl = document.getElementById('updateItemModal')
    let modal = bootstrap.Modal.getOrCreateInstance(modalEl)
    modal.hide()
    getItems()
  } catch (e) {
    console.error(`Error updating ${obj.name}:`, e)
    console.log(e)
  }
}

function handleAddItem() {
  console.log('handleAddItem: ')
  let modalEl = document.getElementById('addItemModal')
  let modal = bootstrap.Modal.getOrCreateInstance(modalEl)
  modal.show()
}

async function addItem() {
  const obj = unref(newItem)
  console.log('addItem: ', obj)
  for (const row of rows.value) {
    if (row.name.toLowerCase() === obj.name.toLowerCase()) {
      alert('Item already exists.')
      return
    }
  }
  try {
    const params = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: obj.name,
        category: obj.category,
        stock: obj.stock,
        notes: obj.notes,
      }),
    }
    const response = await fetch('http://localhost:5000/add_item', params)
    if (!response.ok) {
      throw new Error(`Reponse status: ${response.status}`)
    }
    newItem.value = {
      name: '',
      category: '',
      stock: 0,
      notes: '',
    }
    let modalEl = document.getElementById('addItemModal')
    let modal = bootstrap.Modal.getOrCreateInstance(modalEl)
    modal.hide()
    getItems()
  } catch (e) {
    console.error(`Error adding ${obj.name}:`, e)
    console.log(e)
  }
}

async function deleteItem() {
  const obj = unref(editItem)
  console.log('deleteItem: ', obj.id)
  try {
    const params = {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        id: obj.id,
      }),
    }
    const response = await fetch('http://localhost:5000/delete_item', params)
    if (!response.ok) {
      throw new Error(`Reponse status: ${response.status}`)
    }
    getItems()
  } catch (e) {
    console.error(`Error deleting ${obj.name}:`, e)
    console.log(e)
  }
}

onMounted(() => {
  console.log('ItemTable mounted')
  getItems()
  let addForm = document.querySelector('#addItemForm')
  addForm.addEventListener('submit', (event) => {
    event.preventDefault()
    let submitter = event.submitter
    let handler = submitter.id
    if (handler) {
      addItem()
    } else {
      alert('Please validate inputs.')
    }
  })
  let updateForm = document.querySelector('#updateItemForm')
  updateForm.addEventListener('submit', (event) => {
    event.preventDefault()
    let submitter = event.submitter
    let handler = submitter.id
    console.log(handler)
    if (handler) {
      updateItem()
    } else {
      alert('Please validate inputs.')
    }
  })
  let modalEl = document.getElementById('addItemModal')
  modalEl.addEventListener('hidden.bs.modal', (event) => {
    newItem.value = {
      name: '',
      category: '',
      stock: 0,
      notes: '',
    }
  })
})
</script>

<template>
  <div class="container">
    <div class="row justify-content-end">
      <div class="col-1 gx-0">
        <button class="btn btn-outline-success" style="float: right" @click="handleAddItem">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-plus-lg"
            viewBox="0 0 16 16"
            style="display: inline-block; vertical-align: -0.125em"
          >
            <path
              fill-rule="evenodd"
              d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
  <table class="table table-dark table-striped">
    <thead>
      <tr>
        <th scope="col">Name</th>
        <th scope="col">Category</th>
        <th scope="col">Stock</th>
        <th scope="col">Notes</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <ItemRow
        v-for="row in rows"
        :key="row.id"
        :id="row.id"
        :name="row.name"
        :category="row.category"
        :stock="row.stock"
        :notes="row.notes"
        @get-items="getItems"
        @update-item="handleUpdateItem"
      />
    </tbody>
  </table>

  <datalist id="categories-list">
    <option 
      v-for="category in Array.from(categories).sort(function(a, b) {
        return a.toLowerCase().localeCompare(b.toLowerCase());
      })"
      :value="category"
    ></option>
  </datalist>

  <!-- Update Item Modal -->
  <div
    class="modal fade"
    id="updateItemModal"
    tabindex="-1"
    aria-labelledby="updateItemModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content bg-dark">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="updateItemModalLabel">Update Item</h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <form id="updateItemForm" style="color: black">
          <div class="modal-body">
            <div class="row">
              <div class="form-floating mb-3 col-5">
                <input
                  type="text"
                  class="form-control"
                  id="updateItemName"
                  placeholder="Item"
                  v-model="editItem.name"
                  required
                />
                <label for="itemName">Item Name</label>
              </div>
              <div class="form-floating mb-3 col-5">
                <input
                  type="text"
                  class="form-control"
                  id="updateItemCategory"
                  placeholder="Category"
                  v-model="editItem.category"
                  list="categories-list"
                  required
                />
                <label for="itemCategory">Category</label>
              </div>
              <div class="form-floating mb-3 col-2">
                <input
                  type="number"
                  class="form-control"
                  id="updateItemStock"
                  placeholder="0"
                  v-model="editItem.stock"
                  min="0"
                  required
                />
                <label for="itemStock">Stock</label>
              </div>
            </div>
            <div class="input-group">
              <span class="input-group-text">Notes</span>
              <textarea
                class="form-control"
                aria-labeled="updateItemNotes"
                v-model="editItem.notes"
              ></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-outline-danger"
              style="float: left"
              data-bs-dismiss="modal"
              @click="deleteItem"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                class="bi bi-trash3-fill"
                viewBox="0 0 16 16"
                style="display: inline-block; vertical-align: -0.125em"
              >
                <path
                  d="M11 1.5v1h3.5a.5.5 0 0 1 0 1h-.538l-.853 10.66A2 2 0 0 1 11.115 16h-6.23a2 2 0 0 1-1.994-1.84L2.038 3.5H1.5a.5.5 0 0 1 0-1H5v-1A1.5 1.5 0 0 1 6.5 0h3A1.5 1.5 0 0 1 11 1.5m-5 0v1h4v-1a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 0-.5.5M4.5 5.029l.5 8.5a.5.5 0 1 0 .998-.06l-.5-8.5a.5.5 0 1 0-.998.06m6.53-.528a.5.5 0 0 0-.528.47l-.5 8.5a.5.5 0 0 0 .998.058l.5-8.5a.5.5 0 0 0-.47-.528M8 4.5a.5.5 0 0 0-.5.5v8.5a.5.5 0 0 0 1 0V5a.5.5 0 0 0-.5-.5"
                />
              </svg>
            </button>
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button
              type="submit"
              id="updateItemButton"
              class="btn btn-primary"
              form="updateItemForm"
            >
              Save changes
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Add Item Modal -->
  <div
    class="modal fade"
    id="addItemModal"
    tabindex="-1"
    aria-labelledby="addItemModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-lg modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content bg-dark">
        <div class="modal-header">
          <h1 class="modal-title fs-5" id="addItemModalLabel">Add Item</h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <form id="addItemForm" style="color: black">
          <div class="modal-body">
            <div class="row">
              <div class="form-floating mb-3 col-5">
                <input
                  type="text"
                  class="form-control"
                  id="itemName"
                  :value="newItem.name"
                  @input="(event) => (newItem.name = event.target.value)"
                  required
                />
                <label for="itemName">Item Name</label>
                <div class="invalid-feedback">Please provide a valid name.</div>
              </div>
              <div class="form-floating mb-3 col-5">
                <input
                  type="text"
                  class="form-control"
                  id="itemCategory"
                  :value="newItem.category"
                  @input="(event) => (newItem.category = event.target.value)"
                  list="categories-list"
                  required
                />
                <label for="itemCategory">Category</label>
                <div class="invalid-feedback">Please provide a valid category.</div>
              </div>
              <div class="form-floating mb-3 col-2">
                <input
                  type="number"
                  class="form-control"
                  id="itemStock"
                  :value="newItem.stock"
                  @input="(event) => (newItem.stock = event.target.value)"
                  min="0"
                  required
                />
                <label for="itemStock">Stock</label>
              </div>
            </div>
            <div class="input-group">
              <span class="input-group-text">Notes</span>
              <textarea
                class="form-control"
                aria-labeled="Notes"
                :value="newItem.notes"
                @input="(event) => (newItem.notes = event.target.value)"
              ></textarea>
            </div>
            <!-- <button id="addItemButton" class="btn" type="submit" @click="addItem" style="display: none;">subby</button> -->
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="submit" id="addItemButton" class="btn btn-primary" form="addItemForm">
              Save changes
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
