<template>
    <Toast />
    <ScrollPanel style="width: 100%; height: 100%;">
        <enter-expression v-if="store.userExpression.step==1" class="my-5" 
        :invalidate=false :predefinedLanguage="props.predefinedLanguage"
        />

        <enter-expression v-else class="my-5"
        :invalidate=true :placeholderText=store.userExpression.expr
        />
        
        <split-expression v-if="store.userExpression.step==2" class="my-5"
        :invalidate=false
        />

        <split-expression v-if="store.userExpression.step>2" class="my-5"
        :invalidate=true
        />

        <assign-glosses v-if="store.userExpression.step==3" class="my-5" :invalidate=false
            />
        <assign-glosses v-if="store.userExpression.step>3" class="my-5" :invalidate=true
        />

        <check-expression v-if="store.userExpression.step==4" class="my-5" :invalidate=false
            />
        <check-expression v-if="store.userExpression.step>4" class="my-5" :invalidate=true
        />

        <div class="flex justify-content-center">
            <Button v-if="store.userExpression.step>1 && store.userExpression.step<5" label="Back" severity="warning" @click="StepBack" />
        </div>
    </ScrollPanel>
</template>

<script setup>
import { defineCustomElement, onMounted, watch, defineProps } from 'vue';
import { store } from '../store.js'
import { useToast } from 'primevue/usetoast';

const props = defineProps(['predefinedLanguage'])

const toast = useToast();
const StepBack = () => {
    store.userExpression.previousStep = store.userExpression.step
    store.userExpression.step -= 1
}


watch(() => store.userExpression.submitted, async(newStatus) => {
    if (newStatus !== null) {
        console.log('watch works')
        const message = 'Expression "' + store.userExpression.expr + '" (' + store.userExpression.lang + ') successfully added'
        store.userExpression.expr = null
        store.userExpression.previousExpr = null
        store.userExpression.unitsChanged = true
        store.userExpression.glossed = []
        store.userExpression.singleLineResult = null
        store.userExpression.submitted = null
        store.userExpression.step = 1
        toast.add({ severity: 'success', summary: 'Success', detail: message })
    }
    
})

onMounted(async () => {
    store.userExpression.step = 1
    
})
</script>
<style>
</style>