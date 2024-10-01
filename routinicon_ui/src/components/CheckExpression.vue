<template>
<BlockUI :blocked=props.invalidate
    :pt="{ mask: {class: 'bg-white opacity-20'} }"
    >
    
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
<template #title>Step #4: Check</template>
<template #content>
<DataTable :value="expressionReady">
<Column v-for="col of columns" :key="col.field" :field="col.field" :header="col.header"></Column>
</DataTable>
</template>
<template #footer>
    <Button icon="pi pi-check" severity="success" label="Save" @click="SubmitExpression">
    </Button>
</template>
</Card>
</BlockUI>

</template>

<script setup>
import { onMounted } from 'vue';
import { ref } from 'vue';
import { defineProps } from 'vue';
import { store } from '../store.js'


const props = defineProps(["invalidate"])

const expressionReady = ref()

const CreateExpressionLine = () => {
    const lang = store.userExpression.lang
    const expr = store.userExpression.expr
    const lemmas = store.userExpression.units.map( unit => {
        return unit.lemma
    }
    ).join(' ')
    // console.log(lemmas)
    const poses = store.userExpression.units.map( unit => {
        return unit.pos
    }
    ).join(' ')
    // console.log(poses)
    const realizations =  store.userExpression.units.map( unit => {
        return unit.realization
    }).join(' ')
    // console.log(realizations)
    const glossed = store.userExpression.units.map( unit => {
        return store.userExpression.glossed.filter( 
            morph => morph.unit.toLowerCase() === unit.unit.toLowerCase()
            ).map( morph => { 
                return morph.picked_glosses.map( gl => {
                    return gl.gloss_value
            } ).join('.')
        }).join('-')
    } ).join(' ')
    // console.log(glossed)
    expressionReady.value = [{
        'lang': lang,
        'expr': expr,
        'realizations': realizations,
        'glosses': glossed,
        'lemmas': lemmas,
        'poses': poses
    }]
    store.userExpression.singleLineResult = expressionReady.value
}

const columns = [
    { field: 'lang', header: 'Language' },
    { field: 'expr', header: 'Expression' },
    { field: 'realizations', header: 'Realization' },
    { field: 'glosses', header: 'Glosses' },
    { field: 'lemmas', header: 'Lemmas' },
    { field: 'poses', header: 'POSes' },

];

async function SubmitExpression () {
    console.log('sending to backend')
    const response = await SendToDB()
    console.log(response)
    store.userExpression.submitted = store.userExpression.expr
    store.userExpression.previousStep = null
    store.userExpression.step = 1
    
}

async function SendToDB () {
    const response = await fetch(
          'http://localhost:7000/submit-expression', 
          {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(store.userExpression.singleLineResult)
          }
          )
    const received = await response.json();
    console.log(received)
    store.newExrSubmittedId = received.inserted_id
    console.log(store.newExrSubmittedId)
    return received
}

onMounted(() => {
    console.log('check expression')
    // console.log(store.userExpression.units)
    // console.log(store.userExpression.glossed)
    CreateExpressionLine()
})

</script>