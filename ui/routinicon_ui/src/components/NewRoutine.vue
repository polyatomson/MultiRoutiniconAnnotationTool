<template>
    <Toast/>
    <Stepper orientation="horizontal" v-model:active-step="curStep" @step-change="loadData">
        <StepperPanel header="Routine">
            <template #content="{ nextCallback }">
                <Card :pt="{ 
                header: { class: 'bg-primary border-round-lg' }, 
                title: {class: 'flex justify-content-center'},
                content: { class: 'flex flex-column row-gap-1' }, 
                footer: { class: 'pd-card-footer'} 
                }">
                    <template #header>
                        <div style="height: 1rem;"></div>
                        <!-- <img alt="user header" src="../assets/random_header.png" /> -->
                    </template>
                    <template #title>New routine</template>
                    <template #content>
                        <div class="flex justify-content-center">
                            <SelectButton v-model="store.curLang" :options="store.langIds" optionLabel="lang_id"
                            aria-labelledby="basic" inputId="user_lang"
                            class="pb-3" @change="GetBareRoutines"
                            :allowEmpty = false>
                        <template #option="SlotProps">
                        <div>{{ SlotProps.option.lang }}</div>
                        </template>    
                        </SelectButton>
                        </div>
                        
                        <InputGroup>
                            <span class="p-float-label">
                                <AutoComplete v-model="store.newRoutine" 
                                :suggestions="filteredRoutines" 
                                @complete="search" @change="isInvalid"
                                :class="{'p-invalid': invalid}" :pt="{root: {class: 'flex flex-grow'}, container: {style: 'width: max-content;'}}"
                                />
                                <!-- <label for="new_expression">{{ invalidMessage }}</label> -->
                            </span>
                            <Button type="submit" icon="pi pi-check" :severity="butSeverity()" :disabled="invalid" @click="nextCallback" />
                        </InputGroup>
                    </template>
                </Card>
            </template>
</StepperPanel>
<StepperPanel header="Expressions">
    <template #content="{nextCallback, prevCallback}">
        <Card :pt="{ 
            header: { class: 'bg-primary border-round-lg' }, 
            title: {class: 'flex justify-content-center'},
            content: { class: 'flex flex-column row-gap-1' }, 
            footer: { class: 'pd-card-footer'} 
            }">
            <template #header><div style="height: 1rem;"></div></template>
            <template #title>Choose from existing expressions</template>
            <template #content>
                <DataTable :value="existingExpressions" dataKey="expr_id" v-model:selection="store.pickedExpressions" @row-select="console.log(store.pickedExpressions)" scrollHeight="20rem" scrollable v-model:filters="filters" :globalFilterFields="['expr_full', 'glossing']">
                <template #header>
                    <div class="flex flex-row gap-1">
                        <div class="flex align-items-center">
                            <Button icon="pi pi-plus" @click="newExprVisible=true" />
                        </div>
                        <div class="flex align-items-center">
                            <InputSwitch v-model="showingOnlyPicked" @update:model-value="showPickedOnly"/>
                        </div>
                        <div class="flex flex-grow-1"></div>
                        <div class="flex align-items-center">
                </div>
                    <InputText v-model="filters['global'].value" placeholder="Search"/>
                </div>
                </template>
                    <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
                    <Column field="expr_full" header="Expr"></Column>
                    <Column field="glossing" header="Glossing"></Column>
                </DataTable>
            </template>
        </Card>
    </template>
</StepperPanel>
<StepperPanel header="Constructions"">
    <template #content="{nextCallback, prevCallback}">
        <!-- <div class="flex flex-row justify-content-center" style="max-width: 80%;"> -->
            <pick-constructions langSwitch scrollHeight="30rem"/>
        <!-- </div> -->
    </template>
</StepperPanel>
<StepperPanel v-if="store.selectedCxs.length" header="Cx info">
    <template #content="{nextCallback, prevCallback}">
        <DataTable :value="store.selectedCxs" v-model:expanded-rows="cxInfoExpanded" dataKey="cx_id" :pt="{bodyRow: {class: 'text-primary font-bold'}}">
            <Column field="cx_id" header="ID"/>
            <Column field="cx_formula" header="Formula"/>
            <Column header="Edit" expander headerStyle="width: 3rem"/>
            <template #expansion="slotProps">
                <div class="font-bold py-3">Reductions</div>
                <DataTable :value="store.cxReductions[slotProps.data.cx_id]" 
                editMode="cell" @cell-edit-complete="onCellEditComplete($event, slotProps)" @cell-edit-init="onCellEditInit"  @cell-edit-cancel="onCellEditCancel"
                dataKey="reduction_id">
                    <template #footer>
                        <div class="flex flex-row justify-content-center">
                        <Button icon="pi pi-plus" rounded @click="addReduction(slotProps)"/>
                    </div>
                    </template>
                        <Column header="Change" field="change">
                        <template #editor="{data, field}">
                            <AutoComplete v-model="data[field]" dropdown :suggestions="changeSugg" @complete="filterChanges"></AutoComplete>
                        </template>
                        </Column>
                        <Column header="Element" field="component">
                            <template #editor="{data, field}">
                                <AutoComplete v-model="data[field]" dropdown :suggestions="elSugg" @complete="filterElements"></AutoComplete>
                            </template>
                            </Column>
                        <Column header="SemRole" field="sem_role">
                            <template #editor="{data, field}">
                                <AutoComplete v-model="data[field]" dropdown :suggestions="semRolesSugg" @complete="filterRoles"></AutoComplete>
                            </template>
                        </Column>
                        <Column>
                            <template #body="{data}">
                                <Button icon="pi pi-minus" rounded size="small" severity="danger" @click="deleteReduction(data, slotProps)" />
                            </template>
                        </Column>
                </DataTable>
                <div class="font-bold py-3">Examples</div>
                <DataTable :value="store.cxExamples[slotProps.data.cx_id]"
                editMode="cell" @cell-edit-complete="onCellEditComplete" @cell-edit-init="onCellEditInit" @cell-edit-cancel="onCellEditCancel"
                dataKey="example_id">
                <template #footer>
                    <div class="flex flex-row justify-content-center">
                        <Button icon="pi pi-plus" rounded @click="addExample(slotProps)"/>
                    </div>
                </template>
                <Column header="Example" field="cx_example">
                    <template #editor="{data, field}">
                        <InputText v-model="data[field]"/>
                    </template>
                </Column>
                <Column header="Translation" field="translation">
                    <template #editor="{data, field}">
                        <InputText v-model="data[field]"/>
                    </template>
                </Column>
                <Column header="Source" field="source" >
                    <template #editor="{data, field}">
                        <AutoComplete v-model="data[field]" dropdown :suggestions="suggestedSources" @complete="findSource"/>
                    </template>
                </Column>
                <Column header="Year" field="dated" >
                    <template #editor="{data, field}">
                        <InputNumber v-model="data[field]" :useGrouping="false" showButtons :min="0" :max="store.curYear" />
                    </template>
                </Column>
                <Column>
                    <template #body="{data}">
                        <Button icon="pi pi-minus" rounded size="small" severity="danger" @click="deleteExample(data, slotProps)" />
                    </template>
                </Column>
                </DataTable>
            </template>
        </DataTable>
        <div class="flex flex-row justify-content-center py-3">
            <Button label="Submit" @click="moveOn(nextCallback)"/>
        </div>
    </template>
</StepperPanel>
<StepperPanel header="Frames">
    <template #content="{nextCallback, prevCallback}">
        <frames-table scrollHeight="30rem"/>
    </template>
</StepperPanel>
<StepperPanel header="Check">
    <check-routine/>
</StepperPanel>
</Stepper>

<Dialog v-model:visible="newExprVisible" @after-hide="NewExprAdded">
    <new-expression :predefinedLanguage="true"/>
</Dialog>

</template>
<script setup>
import { onBeforeMount, ref, watch } from 'vue';
import { store } from '../store';
import { FilterMatchMode } from 'primevue/api';
import { useToast } from 'primevue/usetoast';

// cx reductions etc.
const cxInfoExpanded = ref({})

const suggestedSources = ref()
var redId = 1
var cxExId = 1

const editingReductions = ref([])
const editingExamples = ref([])
const toast = useToast()


const checkCxInfo = () => {
    for (const [cx_id, reductions] of Object.entries(store.cxReductions)) {
        for (const red of reductions) {
            if (red.component === null) {
                toast.add({summary: 'Incomplete input', detail: 'The field Element cannot be empty, check cx with ID ' + cx_id , severity: 'error', life: 5000})
                return false
            }
            if (red.change === null) {
                toast.add({summary: 'Incomplete input', detail: 'The field Reduction cannot be empty, check cx with ID ' + cx_id , severity: 'error', life: 5000})
                return false
            }
        }
    }
    for (const [cx_id, examples] of Object.entries(store.cxExamples)) {
        for (const ex of examples) {
            if (ex.cx_example === null) {
                console.log(ex)
                toast.add({summary: 'Incomplete input', detail: 'The example cannot be empty, check cx with ID ' + cx_id , severity: 'error', life: 5000})
                return false
            }
        }
    }
    return true
}

const moveOn = (nextCallback) => {
    if (editingExamples.value.length === 0 && editingReductions.value.length === 0) {
        const allFilled = checkCxInfo()
        if (allFilled) nextCallback()
        else console.log(allFilled)
    }
    else {
        console.log('still editing', editingExamples.value, editingReductions.value)
        toast.add({summary: 'Please, finish editing first', severity: 'error', life: 3000})
    }
}

const onCellEditInit = (event) => {
    let {data, field} = event;
    if (data.reduction_id) editingReductions.value.push({'reduction_id': data.reduction_id, 'field': field})
    else if (data.example_id) editingExamples.value.push({'example_id': data.example_id, 'field': field})
}

const onCellEditCancel = (event) => {
    let { data, field } = event;
    if (data.reduction_id) editingReductions.value = editingReductions.value.filter(r => !(r.reduction_id === data.reduction_id && r.field === field))
    else if (data.example_id) editingExamples.value.filter(e => !(e.example_id === data.example_id && e.field === field))
}

const onCellEditComplete = (event, cx) => {
    let { data, newValue, field } = event;
    console.log('cx', cx)
    switch (field) {
        case 'change':
            if (newValue !== null && newValue.length > 0) {
                    console.log('cell not empty')
                    data[field] = newValue; 
                    editingReductions.value = editingReductions.value.filter(r => !(r.reduction_id === data.reduction_id && r.field === field))
                }
                else {
                    console.log('cell empty');
                    event.preventDefault();}
                break;
        case 'component':
            if (cx.data.cx_formula.includes(newValue)) {
                console.log('ok')
                data[field] = newValue;
                editingReductions.value = editingReductions.value.filter(r => !(r.reduction_id === data.reduction_id && r.field === field))
                break
            }
            else {
                console.log('not ok')
                event.preventDefault()
                break
            }
        case 'sem_role':
            data[field] = newValue;
            console.log(data, field)
            editingReductions.value = editingReductions.value.filter(r => !(r.reduction_id === data.reduction_id && r.field === field))
            console.log('saved null', editingReductions.value)
            break;
        case 'cx_example':
            if (newValue !== null && newValue.length > 0) {
                console.log('cell not empty')
                data[field] = newValue; 
                editingExamples.value = editingExamples.value.filter(e => !(e.example_id === data.example_id && e.field === field))
            }
            else {
                console.log('cell empty');
                event.preventDefault();}
            break;
        case 'source':
            if (newValue !== null && newValue.length > 0) {
                data[field] = newValue.replace(/^\[+|\]+$/g, '')
            }
            else {
                data[field] = null
            }
            editingExamples.value = editingExamples.value.filter(e => !(e.example_id === data.example_id && e.field === field))
            break;
        default: // translation and year
            data[field] = newValue;
            editingExamples.value = editingExamples.value.filter(e => !(e.example_id === data.example_id && e.field === field))
                break;
            
    }
}

const addReduction = (cx_info) => {
    console.log(cx_info.data.cx_id)
    const newRow = {'reduction_id': redId, 'cx_id': cx_info.data.cx_id, 'change': null, 'component': null, 'sem_role': null}
    redId += 1
    const already = store.cxReductions[cx_info.data.cx_id] || []
    store.cxReductions[cx_info.data.cx_id] = [...already, newRow]
}

const deleteReduction = (rowValue, cx_info) => {
    // console.log(rowValue, cx_info)
    // const newRow = {'example_id': cxExId, 'cx_id': cx_info.data.cx_id, 'example': null, 'translation': null, 'source': null, 'dated': 2000}
    // cxExId += 1
    const toKeep = store.cxReductions[cx_info.data.cx_id].filter(r => r.reduction_id !== rowValue.reduction_id)
    store.cxReductions[cx_info.data.cx_id] = toKeep
}

const addExample = (cx_info) => {
    const newRow = {'example_id': cxExId, 'cx_id': cx_info.data.cx_id, 'cx_example': null, 'translation': null, 'source': null, 'dated': 2000}
    cxExId += 1
    const already = store.cxExamples[cx_info.data.cx_id] || []
    store.cxExamples[cx_info.data.cx_id] = [...already, newRow]
}

const deleteExample = (rowValue, cx_info) => {
    // console.log(rowValue, cx_info)
    // const newRow = {'example_id': cxExId, 'cx_id': cx_info.data.cx_id, 'example': null, 'translation': null, 'source': null, 'dated': 2000}
    // cxExId += 1
    const toKeep = store.cxExamples[cx_info.data.cx_id].filter(ex => ex.example_id !== rowValue.example_id)
    store.cxExamples[cx_info.data.cx_id] = toKeep
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


const getExistingReds = async() => {
    const response = await fetch('http://localhost:7000/reductions',
        {
            mode: 'cors',
            method: 'GET',
            headers: {
              "Content-Type": "application/json"
            }
        })
    const received = await response.json()
    elements.value = received.components
    changes.value = received.changes
    semRoles.value = received.sem_roles

}
const changes = ref()
const changeSugg = ref([])
const elements = ref()
const elSugg = ref([])
const semRoles = ref()
const semRolesSugg = ref([])
const filterChanges = (event) => {
    changeSugg.value = changes.value.filter(ch => ch.includes(event.query))
}
const filterElements = (event) => {
    elSugg.value = elements.value.filter(e => e.startsWith(event.query))
}
const filterRoles = (event) => {
    console.log('filterRoles', semRoles.value, semRolesSugg)
    semRolesSugg.value = semRoles.value.filter(s => s.startsWith(event.query))
}
// end


const curStep = ref()
const newExprVisible = ref(false)
// const newRoutine = ref()
const existingRoutines = ref([])
const invalid = ref(false)
const existingExpressions = ref([])
// const pickedExpressions = ref([])
const showingOnlyPicked = ref(false)
var bufferExpressions = []

const showPickedOnly = (event) => {
    if (event) {
        console.log('hiding non-selected', event)
        bufferExpressions = existingExpressions.value
        existingExpressions.value = [...store.pickedExpressions]
        console.log(existingExpressions.value)
    }
    else {
        console.log('showing all')
        var merged = [...store.pickedExpressions, ...bufferExpressions]
        // console.log(merged)
        merged = [... new Set(merged)]
        // console.log(merged)
        existingExpressions.value = merged
        // console.log(existingExpressions.value)
    }
}


const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }})

async function GetLangs() {
    const response = await fetch(
        'http://localhost:7000/languages',
        {
            mode: 'cors',
            method: 'GET',
            headers: {
              "Content-Type": "application/json"
            }
        })
    const received = await response.json()
    store.langIds = received
    store.curLang = received[0]
}

async function GetBareRoutines() {
    const lang_id = store.curLang.lang_id
    const response = await fetch(
        'http://localhost:7000/get-routines-simple',
        {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({lang_id})
        })
    const received = await response.json()
    existingRoutines.value = received
}

const filteredRoutines = ref([])

const search = (event) => {
    console.log(event)
    // const routines = existingRoutines.value.map((r) => r.routine)
    // console.log(routines)
    const filtered = existingRoutines.value.filter((r) => r.startsWith(event.query))
    console.log(filtered)
    filteredRoutines.value = filtered
    
}

const butSeverity = () => {
    if (invalid.value) {return 'danger'} else {return 'success'}
}

const isInvalid = () => {
    const fullmatch = existingRoutines.value.filter((r) => r == store.newRoutine)
    console.log(fullmatch)
    invalid.value = (fullmatch.length > 0)
    console.log(invalid.value)
}

async function GetAllExpressions() {
    const lang = store.curLang.lang
    const response = await fetch(
        'http://localhost:7000/get-full-expressions',
        {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({lang})
        })
    const received = await response.json()
    existingExpressions.value = received
}

const loadData = (event) => {
    console.log('change', event, curStep.value)
    if (event.index == 1) {
        GetAllExpressions()
    }
    if ((event.index == 4 && !store.selectedCxs.length) | (event.index == 5)) {
        console.log('checking')
        collectRoutine()
    }
    if (event.index == 3 && store.selectedCxs.length) {
        console.log('reductions')
        getExistingReds()
        cxInfoExpanded.value[store.selectedCxs[0].cx_id] = true
    }
}


function collectRoutine() {
    if (store.newRoutine === null || !store.newRoutine.length || !store.pickedExpressions.length) {
        return false
    }
    var routines = []
    for (let frame of store.selectedFrames) {
        var frameAlreadyThere = store.userRoutine.filter(f => f.frame_id === frame.frame_id)
        if (frameAlreadyThere.length) {
            console.log('preserving textual fields')
            frameAlreadyThere = frameAlreadyThere[0]
            frameAlreadyThere.routine = store.newRoutine
            frameAlreadyThere.lang = store.curLang.lang
            frameAlreadyThere.exprs = store.pickedExpressions
            // frameAlreadyThere.examples = frameAlreadyThere.examples.filter(e => e.example.length || e.translation.length || e.source.length)
            routines.push(frameAlreadyThere)
            continue
        }
        else {
        const routine = {
                'routine': store.newRoutine,
                'lang': store.curLang.lang,
                'exprs': store.pickedExpressions,
                'situation_structure': frame.situation_structure,
                'pragmatics':  frame.pragmatics,
                'sit_tags': frame.sit_tags,
                'situations': frame.situations,
                'usage_conditions': frame.usage_conditions,
                'frame_id': frame.frame_id,
                'definition': '',
                'comments': '',
                'intonation': '',
                'examples': []
            }
        routines.push(routine)
    }
    }
    console.log(routines)
    store.userRoutine = routines
}

async function NewExprAdded() {
    await GetAllExpressions()
    const newExpr = existingExpressions.value.filter(e => e.expr_id === store.newExrSubmittedId)[0]
    store.pickedExpressions = [...store.pickedExpressions, newExpr]
}

watch (() => store.newExrSubmittedId, async(oldId, newId) => {
    console.log('closing new expression')
    newExprVisible.value = false
})

watch (() => store.routineSubmitted, async(newr, oldr) => {
    if (newr === false) {
        return false
    }
    else {
        store.routineSubmitted = false
        store.userRoutine = []
        store.selectedFrames = []
        store.pickedExpressions = []
        store.newRoutine = null
        store.selectedCxs = []
        store.cxExamples = {}
        store.cxExamples = {}
        showingOnlyPicked.value = false
        curStep.value = 0
    }
})

onBeforeMount( async () => {
    store.selectedCxs = []
    await GetLangs()
    await GetBareRoutines()
    store.curYear = new Date().getFullYear()
})

</script>