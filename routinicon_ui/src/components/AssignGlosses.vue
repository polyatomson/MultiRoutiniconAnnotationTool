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
<template #title>Step #3</template>
<template #content>
    <DataTable :value="MorphInfo" editMode="cell" @cell-edit-complete="onCellEditComplete" @cell-edit-init="onStartCellEdit" rowGroupMode="subheader" groupRowsBy="unit"
    columnResizeMode="expand" tableStyle="width: 40rem"
    showGridlines
    :rowClass="rowClass"
    :pt="{
        rowGroupHeader: { class: 'font-semibold' }

    }">
        <Column field="unit" header="Unit"></Column>
        <Column field="morph" header="Morph" style="width: 50%"
        class="text-center"
        :pt="{
            headerContent: { class: 'flex justify-content-center' }
            }"></Column>
        <Column field="picked_glosses" header="Glossing" style="width: 50%"
        :pt="{
            headerContent: { class: 'flex justify-content-center' }
        }"
        >
            <template #body="slotProps">
                <div class="flex flex-wrap justify-content-center flex-row gap-1">
                    <Tag v-for="gloss in slotProps.data.picked_glosses" 
                    :value="gloss.gloss_value" :key="gloss.gloss_id" 
                    :pt="{ 
                        root: { class: [
                            'border-1', 
                            {'bg-yellow-100': ColorNewGloss(gloss),
                            'surface-200': !ColorNewGloss(gloss)},  
                            'border-300', 'text-color',
                            'text-sm', 'font-normal' ] } 
                    }" />
                    
                </div>
            </template>
            <template #editor="{ data, field, index}">
            
            <AutoComplete v-model="data[field]" multiple dropdown
            :suggestions="filteredSuggestions"
            optionLabel="gloss_value"
            optionGroupLabel="group" optionGroupChildren="glosses"
            @complete="searchGlosses($event, data[field])"
            />

        </template>
            
            </Column>
        <template #groupheader="slotProps">
                    <div class="text-center">
                        <Tag severity="success" 
                        :pt="{
                            root: { class: 'text-base'}
                        }">
                            {{ slotProps.data.unit }}
                        </Tag>
                    </div>
            </template>
    </DataTable>

</template>
<template #footer>
        <Button icon="pi pi-check" severity="success" label="Submit" @click="FinishStep"></Button>
        <Message v-for="msg of submitMessages" :key="msg.id" :severity="msg.severity" :closable="false">
            {{ msg.content }}
        </Message>
</template>
</Card>
</BlockUI>
</template>

<script setup>
import { onMounted } from 'vue';
import { ref } from 'vue';
import { defineProps } from 'vue';
import { store } from '../store.js'

const onCellEditComplete = (event) => {
    let { data, newValue, field } = event;
    data[field] = newValue;
}
const rowClass = (data) => {
    return [{ 'bg-orange-100': !data.picked_glosses.length }];
};

const onStartCellEdit = (event) => {
    let { data, field, index } = event;
    // console.log('index', index)
    const ExistingAll = data.other_glosses.filter((gl_group) => gl_group.group=='All')
    // console.log('all', ExistingAll)
    if (ExistingAll.length) {
        console.log('reusing the full suggestions set')
        suggGlosses.value = data.other_glosses
        return false
    }
    const prioritizedGlossesIds = data.other_glosses.flatMap((x) => x.glosses.map((y) => y.gloss_id))
    // console.log('prioritized', prioritizedGlossesIds)
    const restOfGlosses = Glosses.value.filter((gl) => !prioritizedGlossesIds.includes(gl.gloss_id));
    data.other_glosses.push({'group':'All', 'glosses': restOfGlosses})
    suggGlosses.value = data.other_glosses
    
}

const ColorNewGloss = (gl) => {
    if (gl.gloss_id === 'new') {
        return true
    }
    else {
        return false
    }
}

const props = defineProps(["invalidate"])
const MorphInfo = ref([])
const unitsInfo = {...store.userExpression.units}
const Glosses = ref()
const suggGlosses = ref()
const filteredSuggestions = ref()
// const selectedGlosses = ref()
// const testMorphInfo = [{'unit': 'nov', 'morph': 'nov', 'picked_glosses': [], 'other_glosses': []}, {'unit': 'nov', 'morph': '0', 'picked_glosses': [], 'other_glosses': [{'group': 'Morph-specific (0)', 'glosses': [{'gloss_id': 485, 'gloss_value': 'NOM/ACC'}, {'gloss_id': 486, 'gloss_value': 'SG'}]}]}]

// const addGlossToSelection = (event, currentfield) => {
//     console.log('selected new', event.value)
//     selectedGlosses.value = currentfield
//     selectedGlosses.value.push(event.value)
// }


const searchGlosses = (event, currentValues) => {
    console.log('event', event)
    console.log(currentValues)
    const alreadyChosen = currentValues.flatMap(chosenGl => chosenGl.gloss_id)
    console.log('already chosen', alreadyChosen)
    // console.log(MorphInfo[index].other_glosses)
    let query = event.query.trim();
    console.log('query', query)
    const suggGlossesArray = JSON.parse(JSON.stringify(suggGlosses.value))
    // console.log('new', suggGlossesArray)
    // console.log('test', [{'a':'b'}].includes({'a':'b'}))
    const filteredItems = suggGlossesArray.map(gl_group => {
        const validGlosses = gl_group.glosses.filter(gl => {
        return (gl.gloss_value.startsWith(query.toUpperCase()) || 
        gl.gloss_value.startsWith(query.toLowerCase())) && !alreadyChosen.includes(gl.gloss_id)
    })
        if (validGlosses.length) {
            const newObject = new Object()
            newObject['group'] = gl_group.group
            newObject['glosses'] = validGlosses
            return newObject
        }
        else {
            return null
        }
    }).filter(ready_gr => ready_gr != null);
    console.log('result', filteredItems)
    filteredSuggestions.value = filteredItems
    if (query != '' && !currentValues.filter(v => 
            v.gloss_value === query).length &&
            !Glosses.value.filter(gl => gl.gloss_value == query).length
            ) {
            
    const CustomGloss = {
            'group': 'Add gloss?', 
            'glosses': [{
                'gloss_id': 'new',
                'gloss_value': query
            }]}
    filteredItems.push(CustomGloss)}
    }

const submitMessages = ref([])

const FinishStep = () => {
    // console.log(MorphInfo)
    const NotGlossed = MorphInfo.value.filter(row => !row.picked_glosses.length)
    // console.log('NotAllAreGlossed', NotAllAreGlossed)
    if (NotGlossed.length) {
        console.log('Gloss everything!')
        submitMessages.value.push({ 
            severity: 'error', content: 'All morphs need to be glossed', id: 'error1' 
        })
        if (submitMessages.value.length > 1) {
            submitMessages.value.splice(0, 1)
        }
        return false
    }
    store.userExpression.glossed = MorphInfo.value
    store.userExpression.previousStep = store.userExpression.step
    store.userExpression.step += 1
    console.log('step', store.userExpression.step)
}

async function getMorphs() {
    console.log('units unchanged', store.userExpression.unitsChanged === false)
    // console.log('old morphs', store.userExpression.glossed)
    console.log('old morphs exist', store.userExpression.glossed.length>0)
    if (store.userExpression.previousStep  > 3 || 
    store.userExpression.unitsChanged === false || 
    store.userExpression.step > 3) {
        console.log('reusing morphs')
        MorphInfo.value = store.userExpression.glossed
        return false
    }
    console.log('making a backend query for morphs')
    const lang = store.userExpression.lang
    const lang_id = store.langIds.filter(item => item.lang === lang)[0].lang_id
    // console.log(store.userExpression.units)
    const send_info = JSON.stringify({"lang_id": lang_id, "units": unitsInfo})
    const response = await fetch(
          'http://localhost:7000/morphs-vs-glosses', 
          {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: send_info,
          })
    const received = await response.json()
    MorphInfo.value = received
    store.userExpression.glossed = received
}

async function getGlossIdPairs() {
    if (store.glosses) {
        console.log('reusing glosses')
        Glosses.value = store.glosses
        return false
    }
    const response = await fetch(
          'http://localhost:7000/glosses-simplified', 
          {
            mode: 'cors',
            method: 'GET',
            headers: {
              "Content-Type": "application/json"
            }
          }
          )
    const received = await response.json();
    Glosses.value = received
    store.glosses = received
    
}

// send it to the backend


onMounted(async () => {
    
    getMorphs()
    // console.log(MorphInfo.value)
    getGlossIdPairs()
    // console.log(Glosses.value)
})
</script>
<style></style>