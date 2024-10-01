<template>
    <Card :pt="{ 
    header: { class: 'bg-primary border-round-lg' }, 
    title: {class: 'flex justify-content-center'},
    content: { class: 'flex justify-content-center' }, 
    footer: { class: 'flex justify-content-center'} 
    }">
        <template #title>
            Situation tags
        </template>
        <template #header>
            <div style="height: 1rem;"></div>
        </template>
        <template #content>
            <AutoComplete inputId="tags" v-model="pickedTags" multiple dropdown
                        :suggestions="filteredTagSuggestions"
                        optionGroupLabel="group" optionGroupChildren="tags"
                        @complete="searchTag"
                        @change="saveTags">
            </AutoComplete>
        </template>
    </Card>
</template>

<script setup>

import { onMounted } from 'vue';
import { ref } from 'vue';
import { store } from '../store.js'
import AutoComplete from 'primevue/autocomplete';

const filteredTagSuggestions =ref([])
const pickedTags = ref([])

const searchTag = (event) => {
    console.log('query', event.query)
    if (event.query === '') {
        console.log('gets here')
        filteredTagSuggestions.value = [{'group': 'Tags', 'tags': store.frameAnnotation.stags.filter((t) => !pickedTags.value.includes(t))}]
        return false
    }
    
    const filteredSuggestions = store.frameAnnotation.stags.filter((t) => t.startsWith(event.query) && !pickedTags.value.includes(t))
    const exactOccurence = filteredSuggestions.filter((t) => t == event.query)
    console.log('filteredSuggestions',filteredSuggestions)
    if (filteredSuggestions.length > 0) {    
        if (exactOccurence.length === 0) {
            filteredTagSuggestions.value = [{'group': 'Add?', 'tags': [event.query]}, {'group':'All', 'tags':filteredSuggestions}]
        }
        else {
            filteredTagSuggestions.value = [{'group': 'All', 'tags': filteredSuggestions}]
        }
    }
    else {
        filteredTagSuggestions.value = [{'group': 'Add?', 'tags': [event.query]}]
    }
}

const saveTags = () => {
    store.userFrame.fullFrame.tags = pickedTags.value
}

defineExpose({pickedTags})

onMounted (() => {
    if (store.userFrame.reusing || store.userFrame.editing) {
        pickedTags.value = store.userFrame.fullFrame.tags
    }
})

</script>