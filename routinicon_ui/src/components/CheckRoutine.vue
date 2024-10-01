<template>
    <Toast />
    <Card style="overflow: hidden; max-width: 100%;" :pt="{content: {props: {style: 'max-width: 100%'}}}" class="my-5">
        <template #content>
    <DataTable v-if="store.userRoutine.length" :value="store.userRoutine"
    dataKey="frame_id"
    showGridlines 
    v-model:expandedRows="expandedRows"
    style="max-width: 100%;" :pt="{rowExpansion: {props: {style: 'max-width: 100%'}}}"
    >
    <Column expander style="width: 3rem"></Column>
    <Column header="Routine" field="routine">
    </Column>
    <Column header="Lang" field="lang">
        <template #body="{data, field}">
            <Tag :value="data[field]"></Tag>
        </template>
    </Column>
    <Column header="SitStruct" field="situation_structure">
        <template #body="{data, field}">
            <Tag :value="shortenStructure(data[field])" severity="danger" rounded></Tag>
        </template>
    </Column>
    <Column header="Glosses" field="exprs">
        <template #body="{data, field}">
            {{ data[field][0]?.glossing }}
        </template>
    </Column>
    <Column header="Pragmatics" field="pragmatics" >
        <template #body="{data, field}">
            <div class="flex flex-row flex-wrap gap-1">
                <Tag v-for="t in data[field]" :value="t" rounded severity="success"/>
            </div>
        </template>
    </Column>
    <Column header="SitTags" field="sit_tags">
        <template #body="{data, field}">
            <div class="flex flex-row gap-1">
                <Tag v-for="t in data[field]" :value="t" rounded severity="warning"/>
            </div>
        </template>
    </Column>
    <template #expansion="slotProps">
        <div class="p-1">
            <strong>Situation structure</strong>
            <DataTable :value="[slotProps.data]" class="py-3">
                <Column v-if="'trigger' in slotProps.data.situations && slotProps.data.situations.trigger?.length" field="situations" header="Trigger">
                    <template #body="{data, field}">
                        <div class="flex flex-row flex-wrap gap-2">    
                            <Tag v-for="tag of data[field].trigger" :value="tag" severity="secondary"/>
                        </div>
                    </template>
                </Column>
                <Column v-if="'trigger' in slotProps.data.situations && slotProps.data.situations.trigger?.length">
                <template #body>
                    =>
                </template>
                </Column>
                <Column v-if="'action' in slotProps.data.situations && slotProps.data.situations.action?.length" field="situations" header="Action">
                    <template #body="{data, field}">
                        <div class="flex flex-row flex-wrap gap-2">    
                            <Tag v-for="tag of data[field].action" :value="tag" severity="secondary"/>
                        </div>
                    </template>
                </Column>
                <Column v-if="'action' in slotProps.data.situations && slotProps.data.situations.action?.length">
                <template #body>
                    +
                </template>
                </Column>
                <Column header="Pragmatics">
                    <template #body="{data}">
                        <div class="flex flex-row flex-wrap gap-2">
                           <Tag v-for="t of data.pragmatics" :value="t" severity="success"/>
                        </div>
                    </template>
                </Column>
                <Column v-if="'effect' in slotProps.data.situations && slotProps.data.situations.effect?.length">
                <template #body>
                    =>
                </template>
                </Column>
                <Column v-if="'effect' in slotProps.data.situations && slotProps.data.situations.effect?.length" field="situations" header="Effect">
                    <template #body="{data, field}">
                        <div class="flex flex-row flex-wrap gap-2">
                            <Tag v-for="tag of data[field].effect" :value="tag" severity="secondary"/>
                        </div>
                    </template>
                </Column>
            </DataTable>
            </div>
            <div class="p-1">
            <div v-if="slotProps.data.exprs.length"><strong>Variation</strong></div>
            <DataTable v-if="slotProps.data.exprs.length" :value="slotProps.data.exprs" dataKey="expr_id" class="py-3">
                <Column field="expr_full" header="Expression"></Column>
                <Column field="realization" header="Realization"></Column>
                <Column field="glossing" header="Glosses"></Column>
                <Column field="lemmas" header="Lemmas"></Column>
                <Column field="pos" header="POS"></Column>
            </DataTable>
        </div>

        <div class="p-1">    
            <div v-if="store.selectedCxs.length"><strong>Constructions</strong></div>
                <DataTable v-if="store.selectedCxs.length" :value="store.selectedCxs" class="py-3" v-model:expanded-rows="expandedCxs"
                columnResizeMode="fit" dataKey="cx_id">
                    <Column header="ID" field="cx_id"></Column>
                    <Column field="formula" header="Formula"/>
                    <Column header="Semantics" field="semantics"/>
                    <Column header="SyntType" field="syntactic_type" />
                    <Column expander/>
                    <template #expansion="slotProps">
                    <div class="flex py-3 text-lg font-bold">Changes</div>
                    <DataTable v-if="store.cxReductions[slotProps.data.cx_id].length" :value="store.cxReductions[slotProps.data.cx_id]" columnResizeMode="fit">
                        <Column field="change" header="Change"></Column>
                        <Column field="component" header="Element"></Column>
                        <Column field="sem_role" header="SemRole"></Column>
                    </DataTable>
                    <div v-else>&dash;</div>
                    <div class="flex py-3 text-lg font-bold">Examples</div>
                    <DataTable v-if="store.cxExamples[slotProps.data.cx_id].length" :value="store.cxExamples[slotProps.data.cx_id]" scrollable resizableColumns>
                        <Column field="cx_example" header="Example"></Column>
                        <Column field="translation" header="Translation"></Column>
                        <Column field="source" header="Source"></Column>
                        <Column field="dated" header="Year"></Column>
                    </DataTable>
                    <div v-else>&dash;</div>
                    </template>
                </DataTable>
        </div>


        <div class="p-1">    
        <div><strong>Usage conditions</strong></div>
            <DataTable v-if="slotProps.data.usage_conditions.length" :value="slotProps.data.usage_conditions" class="py-3">
                <Column field="category" header="Category"/>
                <Column field="condition" header="Condition" :pt="{body: {class: 'flex flex-wrap'}}"/>
            </DataTable>
        </div>
        <Card>
            <template #header>
            <div class="card flex justify-center">
                <div class="flex flex-col gap-4">
                    <div v-for="field in additionalFields" :key="field.key" class="flex items-center">
                        <RadioButton v-model="shownAdditionalField" :inputId="field.key" name="dynamic" :value="field.name" @update:modelValue="showField" />
                        <label :for="field.key" class="ml-2">{{ field.name }}</label>
                    </div>
                </div>
            </div>
        </template>
            <template #content>
        <div v-show="showDefinition" class="p-1">
                <Textarea v-model="slotProps.data.definition" rows="3" style="min-width: 50rem;"/>
            </div>
            <div v-show="showIntonation" class="p-1">
                <Textarea v-model="slotProps.data.intonation" rows="3" style="min-width: 50rem;"/>
            </div>
            <div v-show="showComments" class="p-1">
                <Textarea v-model="slotProps.data.comments" rows="3" style="min-width: 50rem;"/>
            </div>
            <div v-show="showExamples" class="p-1">
                <DataTable :value="slotProps.data.examples" editMode="cell" @cell-edit-complete="onExampleEditComplete" dataKey="example_id">
                    <template #footer>
                        <div class="flex flex-row justify-content-center gap-3">
                            <Button icon="pi pi-plus" rounded @click="addExample(slotProps.index)"/>
                            <Button icon="pi pi-bolt" rounded severity="secondary" @click="generateExamples(slotProps.index)"/>
                        </div>
                    </template>
                    <Column field="example" header="Example" body-style="max-width: 35%;" :pt="{body: {class: 'flex flex-wrap'}}">
                        <template #editor="{data, field}">
                            <Textarea autoResize v-model="data[field]" style="width: 100%;"/>
                        </template>
                        <template #body="{data, field}">
                            <div class="flex flex-row flex-wrap">{{ data[field] }}</div>
                        </template>
                    </Column>
                    <Column field="translation" body-style="max-width: 35%;" header="Translation">
                        <template #editor="{data, field}">
                            <Textarea autoResize v-model="data[field]" style="width: 100%;"/>
                        </template>
                        <template #body="{data, field}">
                            <div class="flex flex-row flex-wrap">{{ data[field] }}</div>
                        </template>
                    </Column>
                    <Column field="source" header="Source" body-style="max-width: 10%;">
                        <template #editor="{data, field}">
                            <AutoComplete v-model="data[field]" class="flex flex-wrap" style="width: 100%;" :suggestions="suggestedSources" @complete="findSource" dropdown></AutoComplete>
                        </template>
                    </Column>
                    <Column header="Year" field="dated" body-style="max-width: 10%;">
                    <template #editor="{data, field}">
                        <InputNumber v-model="data[field]" :useGrouping="false" showButtons :min="0" :max="store.curYear" />
                    </template>
                </Column>
                <Column body-style="max-width: 10%">
                    <template #body="{data}">
                        <Button icon="pi pi-minus" rounded size="small" severity="danger" @click="deleteEx(data, slotProps)" />
                    </template>
                </Column>
                </DataTable>
            </div>
        </template></Card>
    </template>
    </DataTable>
    <div v-if="!store.userRoutine.length">To see the preview, enter the routine and choose at least one frame and at least one expression.</div>
    </template>
    <template #footer>
        <div class="flex flex-row justify-content-center"><Button :disabled="store.userRoutine.length < 1" label="Save" @click="sendToDB"/></div>
    </template>
</Card>
<Dialog v-model:visible="showCorporaExamples" @after-hide="addGeneratedExamples" modal>
<TabView>
<TabPanel v-for="expr in generatedExamples" :header="expr.expr_full">
    <DataTable :value="expr.examples" v-model:selection="pickedExamples">
        <template #header>
            <div class="flex flex-row gap-4 justify-content-end">
                <div class="flex align-items-center"><Button icon="pi pi-refresh" @click="generateNew(expr.expr_full, expr.page_num)"/></div>
                <div class="flex align-items-center"><Tag severity="secondary" :value="expr.corpname"/></div>
                <div class="flex align-items-center"><Tag severity="secondary" :value="expr.page_num"/></div>
                <div class="flex align-items-center"><Tag severity="secondary" :value="expr.fullsize + ' hits'" rounded/></div>
                <div class="flex align-items-center"><Tag severity="secondary" :value="expr.ipm + ' ipm'"/></div>
                <div class="flex align-items-center"><Tag severity="secondary" :value="'CQL: '+expr.query"/></div>
            </div>
        </template>
        <Column selection-mode="multiple"/>
        <Column field="left"/>
        <Column field="kwic"/>
        <Column field="right"/>
        <Column field="source_name"/>
        <Column field="year"/>
    </DataTable>
</TabPanel>    
</TabView>
</Dialog>
</template>

<script setup>
import { defineProps, ref } from 'vue';
import { store } from '../store';
import { useToast } from 'primevue/usetoast';


const expandedCxs = ref([])

const toast = useToast()
const expandedRows = ref()
const showDefinition = ref(false)
const showComments = ref(false)
const showIntonation = ref(false)
const showExamples = ref(true)
const suggestedSources = ref([])

// const examples = ref([])

const onExampleEditComplete = (event) => {
    let { data, newValue, field } = event;
    data[field] = newValue;
}

async function getSources () {
    const response = await fetch(
        'http://localhost:7000/example-sources',
        {
            mode: 'cors',
            method: 'GET',
            headers: {
              "Content-Type": "application/json"
            }
        }
    )
    const received = await response.json()
    store.exampleSources = received.sources
    // console.log('sources in store', store.exampleSources)
}

async function findSource (event) {
    if (!store.exampleSources.length) {
        await getSources()
    }
    // console.log(event)
    suggestedSources.value = store.exampleSources.filter(es => es.toLowerCase().startsWith(event.query.toLowerCase()))
}

var n_examples = 0

const addExample = (index) => {
    console.log(index)
    n_examples += 1
    var existingExamples = store.userRoutine[index].examples
    console.log(existingExamples)
    existingExamples.push({'example_id': n_examples, 'example': null, 'source': null, 'translation': null, 'dated': 2000})
    store.userRoutine[index].examples = existingExamples
}

const deleteEx = (data, slotProps) => {
    // console.log(data, slotProps)
    store.userRoutine[slotProps.index].examples = store.userRoutine[slotProps.index].examples.filter(e => e.example_id !== data.example_id)
}

const shownAdditionalField = ref('Examples')
const additionalFields = ref([
    {name: 'Examples', key: 'E'},
    {name: 'Definition', key: 'D'},
    {name: 'Intonation', key: 'D'},
    {name: 'Comment', key: 'C'}
])

const showField = (event) => {
    console.log(event)
    if (event==='Definition') {showDefinition.value = true; showComments.value = false; showIntonation.value = false; showExamples.value = false}
    else if (event==='Comment') {showComments.value = true; showDefinition.value = false; showIntonation.value = false; showExamples.value = false}
    else if (event==='Intonation') {showIntonation.value = true; showComments.value = false; showDefinition.value = false; showExamples.value = false}
    else if (event==='Examples' ){showIntonation.value = false; showComments.value = false; showDefinition.value = false; showExamples.value = true}
}

const shortenStructure = (structureTag) => {
    switch (structureTag) {
        case 'reaction':
            return 'R'
        case 'prompt':
            return 'P'
        case 'reaction + prompt':
            return 'R + P'
        case 'accompaniment':
            return 'A'
        default:
            return structureTag;
    }
}

async function sendToDB () {
    console.log('sending', store.userRoutine)
    const response = await fetch(
        'http://localhost:7000/save-new-routine', 
          {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({...store.userRoutine[0], 'cxs': store.selectedCxs.map(c => c.cx_id), 'cx_reductions': store.cxReductions, 'cx_examples': store.cxExamples}),
          })
    const received = await response.json();
    if (received.routine_id == null) {
        console.log('null')
        toast.add({ severity: 'error', summary: 'Already exists', detail: 'Unique violation' })
    }
    else {
        store.routineSubmitted = true
        toast.add({severity: 'success', summary: 'Added', detail: 'The routine was added under id' + (received.routine_id).toString()})
    }
}

const generateNew = async(full_expr, page_num) => {
        await addGeneratedExamples()
        const response = await fetch(
        'http://localhost:7000/generate-examples',
        {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({'exprs': store.userRoutine[0].exprs.filter(e => e.full_expr = full_expr), 'lang_id': store.curLang.lang_id, 'page_num': page_num + 1})
        })
        const received = await response.json()
        if (received.error) {
            return false
        }
        for (let index = 0; index < generatedExamples.value.length; index++) {
            const expression = generatedExamples.value[index];
        
            if (expression.expr_full === full_expr) {
                console.log('assigned new')
                generatedExamples.value[index] = received[0]
            }
            else {
                console.log(expression.expr_full, full_expr)
            }
            
            console.log(generatedExamples.value)
        }
    }


const generateExamples = async(index) => {
    const response = await fetch(
        'http://localhost:7000/generate-examples',
        {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({'exprs': store.userRoutine[0].exprs, 'lang_id': store.curLang.lang_id, 'page_num': 1})
        })
    const received = await response.json()
    if (received.error) {
        return false
    }
    generatedExamples.value = received
    showCorporaExamples.value = true
    workingWFrame.value = index

}

const addGeneratedExamples = () => {
    const index = workingWFrame.value
    console.log(index)
    var existingExamples = store.userRoutine[index].examples
    for (const ex of pickedExamples.value) {
        if (!existingExamples.filter(e => e.example === ex.full).length) {
                n_examples += 1
                const newExample = {'example_id': n_examples, 'example': ex.full, 'source': generatedExamples.value[0].corpname, 'dated': ex.year}
                existingExamples.push(newExample)}
    }
    store.userRoutine[index].examples = existingExamples
}

const pickedExamples = ref([])

const showCorporaExamples = ref(false)

const workingWFrame = ref()

const generatedExamples = ref([])



</script>