<template>
        <Card :pt="{ 
    header: { class: 'bg-primary border-round-lg' }, 
    title: {class: 'flex justify-content-center'},
    content: { class: 'flex flex-column row-gap-5' }, 
    footer: { class: 'flex justify-content-center'} 
    }">
        <template #title>
            Situation structure
        </template>
        <template #header>
            <div style="height: 1rem;"></div>
        </template>
        <template #content>
            <div class="flex justify-content-center">
                <SelectButton v-model="situationStructure" 
                :options="situationStructures" @change="changeStructure"
                :allowEmpty="false"/>
            </div>
            
            <div v-if="eventFields.includes('t')" class="flex justify-content-center">
            <InputGroup style="width: 70%;">
                <InputGroupAddon>Trigger</InputGroupAddon>
                        <AutoComplete inputId="trigger"
                        v-model="pickedTriggers" multiple dropdown
                        :suggestions="filteredEventSuggestions"
                        optionGroupLabel="group" optionGroupChildren="events"
                        @complete="searchEvents($event, 't', pickedTriggers)"
                        @change="saveTriggers"
                        >
                        </AutoComplete>
            </InputGroup>
            </div>
            
            <div v-if="eventFields.includes('a')" class="flex justify-content-center">
                <InputGroup style="width: 70%;">
                    <InputGroupAddon>Action</InputGroupAddon>
                            <AutoComplete inputId="action"
                            v-model="pickedActions" multiple dropdown
                            :suggestions="filteredEventSuggestions"
                            optionGroupLabel="group" optionGroupChildren="events"
                            @complete="searchEvents($event, 'a', pickedActions)"
                            @change = "saveActions"
                            >
                            </AutoComplete>
                </InputGroup>
            </div>

            <div class="flex justify-content-center">
                <InputGroup style="width: 70%;">
                    <InputGroupAddon class="bg-primary">Pragm</InputGroupAddon>
                            <AutoComplete inputId="pragmatics"
                            v-model="pickedPragmatics" multiple dropdown
                            :suggestions="filteredPragmaticsSuggestions"
                            optionGroupLabel="group" optionGroupChildren="tags"
                            @complete="searchPragmatics"
                            @change="savePragmatics"
                            >
                            </AutoComplete>
                </InputGroup>
            </div>
            
            <div v-if="eventFields.includes('e')" class="flex justify-content-center">
                <InputGroup style="width: 70%;">
                    <InputGroupAddon>Effect</InputGroupAddon>
                            <AutoComplete inputId="effect"
                            v-model="pickedEffects" multiple dropdown
                            :suggestions="filteredEventSuggestions"
                            optionGroupLabel="group" optionGroupChildren="events"
                            @complete="searchEvents($event, 'e', pickedEffects)"
                            @change="saveEffects"
                            >
                            </AutoComplete>
                </InputGroup>
        </div>
        </template>
</Card>
</template>

<script setup>
import { ref } from 'vue'
import { onMounted } from 'vue';
import { store } from '../store.js'

const eventFields = ref(['t', 'p'])
const situationStructures = ref(['reaction', 'prompt', 'reaction + prompt', 'accompaniment'])
const situationStructure = ref('')

const pickedTriggers = ref([])
const pickedEffects = ref([])
const pickedActions = ref([])
const pickedPragmatics = ref([])
const filteredPragmaticsSuggestions = ref()
const filteredEventSuggestions = ref()
// const eventsTriggers = ref(['encounter', 'sneezing'])
// const eventsEffects = ref(['encounter', 'sneezing'])
// const eventsActions = ref(['encounter', 'sneezing'])
// const events = {'t': eventsTriggers, 'e': eventsEffects, 'a': eventsActions}
// const pragmatics = ref(['greeting', 'joy', 'wish'])

const Test = (info) => {
    console.log('test', info)
}

const changeStructure = (event) => {
    updateTagsForStructure()
    console.log('changed structure', event.value)
    const new_str = event.value
    switch (new_str) {
        case 'reaction':
            eventFields.value = ['t']
            pickedActions.value = []
            pickedEffects.value = []
            break;
        case 'prompt':
            eventFields.value = ['e']
            pickedTriggers.value = []
            pickedActions.value = []
            break;
        case 'reaction + prompt':
            eventFields.value = ['t', 'e']
            pickedActions.value = []
            break;
        case 'accompaniment':
            eventFields.value = ['t', 'a', 'e'];
            break;
        default:
            eventFields.value = [];
    }
    store.userFrame.fullFrame.sitStructure = situationStructure.value
}

const searchEvents = (event, relevantEventType, pickedItems) => {
    console.log('relevant type', relevantEventType)
    console.log('structure', store.frameAnnotation.structure)
    const relevantEvents = store.frameAnnotation.structure[relevantEventType]
    console.log(relevantEvents)
    console.log(pickedItems)
    if (!event.query.length) {
        console.log('triggered')
        filteredEventSuggestions.value = [{'group': 'Events', 'events': relevantEvents.filter(e => !pickedItems.includes(e))}]
        return false
    }
    const exactOccurence = relevantEvents.filter(e => e===event.query)
    const suggs = relevantEvents.filter(e => e.startsWith(event.query) && !pickedItems.includes(e))
    if (suggs.length) {
        console.log(suggs)
        filteredEventSuggestions.value = [{'group': 'All', 'events': suggs}]
    }
    else {
        filteredEventSuggestions.value = []
    }
    if (!exactOccurence.length && !pickedItems.includes(event.query)) {
        filteredEventSuggestions.value.unshift({'group': 'Add?', 'events':[event.query]})
    }
}

const searchPragmatics = (event) => {
    if (!event.query.length) {
        console.log('triggered')
        filteredPragmaticsSuggestions.value = [{'group': 'Tags', 'tags': store.frameAnnotation.structure.p.filter(p => !pickedPragmatics.value.includes(p))}]
        return false
    }
    const exactOccurence = store.frameAnnotation.structure.p.filter(p => p===event.query)
    const suggs = store.frameAnnotation.structure.p.filter(p => p.startsWith(event.query) && !pickedPragmatics.value.includes(p))
    if (suggs.length) {
        console.log(suggs)
        filteredPragmaticsSuggestions.value = [{'group': 'All', 'tags': suggs}]
    }
    else {
        filteredPragmaticsSuggestions.value = []
    }
    if (!exactOccurence.length && !pickedPragmatics.value.includes(event.query)) {
        filteredPragmaticsSuggestions.value.unshift({'group': 'Add?', 'tags':[event.query]})
    }
}

const saveTriggers = () => {
    store.userFrame.fullFrame.events.triggers = pickedTriggers.value
}

const saveActions = () => {
    store.userFrame.fullFrame.events.actions = pickedActions.value
}

const saveEffects = () => {
    store.userFrame.fullFrame.events.effects = pickedEffects.value
}

const savePragmatics = () => {
    store.userFrame.fullFrame.pragmatics = pickedPragmatics.value
}

async function updateTagsForStructure() {
    const struct = situationStructure.value
    const response = await fetch(
        'http://localhost:7000/get-structure-tags',
        {method: 'POST',
            mode: 'cors',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({struct})
        })
    const received = await response.json()
    store.frameAnnotation.structure = received
}

onMounted(async () => {
    console.log('step', store.userFrame.step)
    if (store.userFrame.reusing || store.userFrame.editing) {
        situationStructure.value = store.userFrame.fullFrame.sitStructure
        updateTagsForStructure()
        pickedPragmatics.value = store.userFrame.fullFrame.pragmatics
        pickedTriggers.value = store.userFrame.fullFrame.events.triggers || []
        pickedActions.value = store.userFrame.fullFrame.events.actions || []
        pickedEffects.value = store.userFrame.fullFrame.events.effects || []
        switch (situationStructure.value) {
        case 'reaction':
            eventFields.value = ['t']
            break;
        case 'prompt':
            eventFields.value = ['e']
            break;
        case 'reaction + prompt':
            eventFields.value = ['t', 'e']
            break;
        case 'accompaniment':
            eventFields.value = ['t', 'a', 'e'];
            break;
        default:
            eventFields.value = [];
        }
    return true
    }
    situationStructure.value = 'reaction'
    store.userFrame.fullFrame.sitStructure = 'reaction'
})

</script>