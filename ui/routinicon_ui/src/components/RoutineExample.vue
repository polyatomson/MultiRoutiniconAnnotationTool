<template>
    <Card :pt="{ 
    header: { class: 'bg-primary border-round-lg' }, 
    title: {class: 'flex justify-content-center'},
    content: { class: 'flex justify-content-center' }, 
    footer: { class: 'flex justify-content-center'} 
    }">
        <template #title>
            Examples
        </template>
        <template #header>
            <div style="height: 1rem;"></div>
        </template>
        <template #content>
            <AutoComplete inputId="routine_example" v-model="pickedRoutines" multiple dropdown
                        :suggestions="filteredRSuggestions"
                        optionLabel = "r"
                        @complete="searchR"
                        @change="saveExamples">
                <template #option="slotProps">
                    <div class="flex flex-row gap-2">
                        <div class="flex align-items-center"><Tag :value="slotProps.option.lang" severity="secondary"/></div>
                        <div class="flex align-items-center">{{ slotProps.option.r }}</div>
                        <div class="flex flex-grow-1"></div>
                        <div class="flex align-items-center">
                            <i :class="['pi', {'pi-lock-open': slotProps.option.vacant, 'pi-lock': !slotProps.option.vacant}]"></i>
                        </div>
                    </div>
                </template>
            </AutoComplete>
        </template>
    </Card>
</template>

<script setup>

import { onMounted } from 'vue';
import { ref } from 'vue';
import { store } from '../store.js'
import AutoComplete from 'primevue/autocomplete';

// const routines = ref([
//     {'lang': 'si', 'r': 'kdo je', 'r_id':1}, {'lang': 'si', 'r': 'marš', 'r_id':2}, 
//     {'lang': 'si', 'r':'na', 'r_id':3}, {'lang': 'si', 'r':'evo ga', 'r_id':4}])
const filteredRSuggestions =ref([])
const pickedRoutines = ref([])

const searchR = (event) => {
    console.log('query', event.query)
    if (event.query === '') {
        filteredRSuggestions.value = store.frameAnnotation.routines.filter((rut) => !pickedRoutines.value.filter((pr) => pr.r_id == rut.r_id).length)
        return false
    }
    
    filteredRSuggestions.value = store.frameAnnotation.routines.filter((rut) => rut.r.startsWith(event.query) && !pickedRoutines.value.filter((pr) => pr.r_id == rut.r_id).length)
    
}

const saveExamples = () => {
    store.userFrame.fullFrame.examples = pickedRoutines.value
}


</script>