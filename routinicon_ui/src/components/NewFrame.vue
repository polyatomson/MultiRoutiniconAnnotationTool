<template>
    <situation-structure class="my-5" ref="firstStep"/>
    <div class="my-5">
        <situation-tags v-if="store.userFrame.step>1" ref="secondStep"/>
    </div>
    <div class="my-5">
        <conditions v-if="store.userFrame.step>2" ref="thirdStep"/>
    </div>
    <div class="my-5">
        <routine-example v-if = "store.userFrame.step>3" ref="fourthStep"/>
    </div>
    <div class="my-5">
        <check-frame v-if = "store.userFrame.step>4"/>
    </div>
    <div class="flex justify-content-center my-5">
        <Button v-if="store.userFrame.step<5" label="Next" @click="nextStep" />    
    </div>
</template>
<script setup>
import { defineCustomElement, onMounted, watch, ref, onBeforeMount } from 'vue';
import { store } from '../store.js'

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