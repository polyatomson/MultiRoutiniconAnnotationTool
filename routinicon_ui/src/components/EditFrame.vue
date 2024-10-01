<template>
    <Toast />
    <situation-structure class="my-5" ref="firstStep"/>
    <div class="my-5">
        <situation-tags v-if="store.userFrame.step>1" ref="secondStep"/>
    </div>
    <div class="my-5">
        <conditions v-if="store.userFrame.step>2" ref="thirdStep"/>
    </div>
    <div class="my-5">
        <check-frame v-if = "store.userFrame.step>3"/>
    </div>
    <div v-if = "store.userFrame.step>4" class="my-5">
        <Card :pt="{ 
            header: { class: 'bg-primary border-round-lg' }, 
            title: {class: 'flex justify-content-center'},
            content: { class: 'flex justify-content-center row-gap-1' }, 
            footer: { class: 'flex flex-column align-items-center'} 
        }">
            <template #header>
                    <div style="height: 1rem;"></div>
                    <!-- <img alt="user header" src="../assets/random_header.png" /> -->
            </template>
            <template #title>Apply to...</template>
            <template #content>
                <div class="flex flex-column gap-4">
                <div v-for="routine in linkedRoutines" :key="routine.routine_id" class="flex align-items-center">
                    <Checkbox v-model="keepLinked" :inputId="routine.routine_id" :value="routine.routine_id" />
                    <label :for="routine.routine_id" class="ml-2">{{ routine.routine + ' ('+ routine.lang + ')' }}</label>
                </div>
                <div v-if="!linkedRoutines.length">
                No routines are linked to this frame, it is safe to save the edits.
                </div>
                </div>

            </template>
        </Card>
    </div>
    <div class="flex justify-content-center my-5">
        <Button v-if="store.userFrame.step<4" label="Next" @click="nextStep" />    
        <Button v-if="store.userFrame.step===4" label="Checkout" @click="getExamples(); nextStep()" />    
        <Button v-if="store.userFrame.step===5" label="Save" @click="saveChanges()" />    
    </div>
    </template>
<script setup>
import { onMounted, onBeforeMount, ref } from 'vue';
import { store } from '../store.js'
import { useToast } from 'primevue/usetoast';

const linkedRoutines = ref([])
const keepLinked = ref([])
const toast = useToast()
const nextStep = () => {
    store.userFrame.previousStep = store.userFrame.step * 1
    store.userFrame.step += 1
}


async function getTags() {
    const response = await fetch(
        'http://localhost:7000/get-frame-tags',
        {method: 'GET',
            headers: {
              "Content-Type": "application/json"
            }
        })
    const received = await response.json()
    return received
}

const saveChanges = async() => {
    const response = await fetch(
        'http://localhost:7000/save-frame-edits',
        {method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({...store.userFrame.fullFrame, keepLinked: keepLinked.value, linkedRoutines: linkedRoutines.value.map(item => item.routine_id)})
        })
    const received = await response.json()
    if (received.status === 'unchanged') {
        toast.add({'summary': 'Unchanged', 'severity': 'warn'})
    }
    else { toast.add({'summary': 'Edits saved', 'detail': 'New frame_id: ' + received.new_frame})}
    
}

const getExamples = async() => {
    const response = await fetch(
        'http://localhost:7000/get-routines-for-frame',
        {method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({frame_id: store.userFrame.fullFrame.frame_id})
        })
    const received = await response.json()
    linkedRoutines.value = received['routines']
}


onBeforeMount(async () => 
    {
        const tags = await getTags()
        store.frameAnnotation = tags
    }
)



onMounted(() => {
    store.userFrame.step = 1
    
})

</script>