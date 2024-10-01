<template>
<Card style="overflow: hidden;" class="my-5">
<template #content>
    <DataTable :value="store.allConstructions" v-model:expanded-rows="expanded" 
    v-model:filters="filters" dataKey="cx_id" filterDisplay="row"
    :pt="{bodyRow: {class: 'surface-ground'}}" @rowExpand="checkIfRoutinesEmpty"
    >
        <Column header="ID" field="cx_id"></Column>
        <Column header="Lang" field="lang">
        <template #filter="{filterModel, filterCallback}">
            <Dropdown :options="langs" v-model="filterModel.value" @change="filterCallback" class="p-column-filter" options="{{[1,2]}}"/>
        </template>
        </Column>
        <Column header="Formula" field="cx_formula">
            <template #filter="{filterModel, filterCallback}">
                <InputText v-model="filterModel.value" type="text" 
                        @input="filterCallback" class="p-column-filter" />
            </template>
        </Column>
        <Column header="Semantics" field="cx_semantics">
            <template #filter="{filterModel, filterCallback}">
                <Dropdown :options="sem" v-model="filterModel.value" @change="filterCallback" class="p-column-filter" options="{{[1,2]}}"/>
            </template>
        </Column>
        <Column header="SyntType" field="syntactic_type">
            <template #filter="{filterModel, filterCallback}">
                <Dropdown :options="synt" v-model="filterModel.value" @change="filterCallback" class="p-column-filter" options="{{[1,2]}}"/>
            </template>
        </Column>
        <Column expander></Column>
        <template #expansion="slotProps">
            <div class="flex py-3 text-lg font-bold">Routines</div>
            <DataTable small :value="slotProps.data.all_routines" v-model:expanded-rows="expandedExamples" @rowExpand="checkIfRowEmpty" dataKey="routine_id"
            strippedRows>
            <Column field="routine_id" header="ID"></Column>
            <Column field="routine" header="Routine"></Column>
            <Column field="pragmatics" header="Pragmatics">
                <template #body="{data, field}">
                    <div class="flex flex-wrap flex-row gap-1">
                        <Tag v-for="p of data[field]" :value="p"/>
                    </div>
                </template>
            </Column>
            <!-- <Column field="shift" header="SemShift"></Column> -->
            <Column expander></Column>
            <template #expansion="slotProps">
                    <div v-if="slotProps.data.reduction" class="flex justify-content-center py-3 text-lg font-bold">Changes</div>
                    <div class="flex justify-content-center">
                        <DataTable small v-if="slotProps.data.reduction" :value="slotProps.data.reduction" style="width: 60%;">
                            <Column field="reduction_id" header="ID"></Column>
                            <Column field="change" header="Change"></Column>
                            <Column field="component" header="Element"></Column>
                            <Column field="sem_role" header="SemRole"></Column>
                        </DataTable>
                    </div>
                    <div v-if="slotProps.data.examples" class="flex justify-content-center py-3 text-lg font-bold">Examples</div>
                    <div class="flex justify-content-center">
                        <DataTable small v-if="slotProps.data.examples" :value="slotProps.data.examples" scrollable resizableColumns style="width: 80%;">
                            <Column field="example_id" header="ID"></Column>
                            <Column field="example" header="Example"></Column>
                            <Column field="translation" header="Translation"></Column>
                            <Column field="source" header="Source"></Column>
                            <Column field="dated" header="Year"></Column>
                        </DataTable>
                    </div>
                </template>
            </DataTable>
        </template>
    </DataTable>
</template>
</Card>
</template>
<script setup>
import {ref, onMounted} from 'vue'
import { store } from '../store';
import { FilterMatchMode } from 'primevue/api';
// console.log('cxs in store', store.userConstructions)
const expanded = ref({})
const expandedExamples = ref({})

const checkIfRowEmpty = (event) => {
    console.log(event)
    if (event.data.examples || event.data.reduction) {
        console.log('all good')
        console.log(expandedExamples.value[event.data.routine_id])
    }
    else {
        event.preventDefault()
        expandedExamples.value[event.data.routine_id] = false
        return false
    }
}

const checkIfRoutinesEmpty = (event) => {
    console.log(event)
    if (event.data.all_routines !== null) {
        console.log('all good')
        console.log(expanded.value)
    }
    else {
        // event.preventDefault()
        expanded.value[event.data.cx_id] = false
        console.log(expanded.value)
        return false
    }
}

const test = ref(
    [{"cx_id": 1, "lang_id": 58, "lang": "ru", "cx_formula": "VP-Imper!", 
    "all_routines": [
        {
            "shift": "no reduction", 
            "routine": "помогите", 
            "examples": [{
                "example_id": 1,
                "dated": 2001, 
                "source": "[RNC]", 
                "example": "Но это такая взрослая жизнь.  Помоги мне.  Я прошу тебя.", 
                "translation": null}
            ], 
            "reduction": null, 
            "routine_id": 1}
        ], 
        "cx_semantics": "imperative", 
        "syntactic_type": "verbal"}
    ]
)

const loadCxs = async() => {
    const response = await fetch(
        'http://localhost:7000/get-constructions',
        {
            mode: 'cors',
            method: 'GET',
            headers: {
              "Content-Type": "application/json"
            }
        }
    )
    const recieved = await response.json()
    store.allConstructions = recieved
    langs.value = [...recieved].map(item => item.lang)
    sem.value = [...recieved].map(item => item.cx_semantics)
    synt.value = [...recieved].map(item => item.syntactic_type)

}

const langs = ref([])
const sem = ref([])
const synt = ref([])

const filters = ref({
    lang: {value: null, matchMode: FilterMatchMode.STARTS_WITH},
    cx_formula: {value: null, matchMode: FilterMatchMode.CONTAINS},
    syntactic_type: {value: null, matchMode: FilterMatchMode.EQUALS},
    cx_semantics: {value: null, matchMode: FilterMatchMode.EQUALS},
});

onMounted(async() => {
    await loadCxs()
})

</script>