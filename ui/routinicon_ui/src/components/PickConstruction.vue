<template>
<Toast />
<div class="flex flex-row justify-content-end">
    <SelectButton v-model="store.curLang" :options="store.langIds" optionLabel="lang"
                            aria-labelledby="basic"
                            class="py-3"
                            @change="changedLang" :disabled="props.langSwitch" />
</div>
<DataTable :value="store.allConstructions" dataKey="cx_id"
filter v-model:filters="filters" filterDisplay="row" 
editMode="row" v-model:editingRows="editingRows"
@row-edit-init="editIfNew" @row-edit-save="saveEditCheck" @row-edit-cancel="removeEmptyNew"
v-model:selection="store.selectedCxs" @row-unselect="unselectCx" @row-unselect-all="showPickedOnly = false; switchPickedShow()"
scrollable :scroll-height="props.scrollHeight"
>
    <template #footer>
        <div class="flex flex-row justify-content-center gap-3">
        <Button icon="pi pi-plus" @click="addCxRow"/>
        </div>
    </template>
    <Column selectionMode="multiple" headerStyle="width: 3rem">
    <template #header><InputSwitch v-model="showPickedOnly" @change="switchPickedShow"/></template>
    </Column>
    <Column header="ID" field="cx_id" sortable></Column>
        <Column header="Lang" field="lang" sortable>
        <template #filter="{filterModel, filterCallback}">
            <Dropdown :options="langs" v-model="filterModel.value" @change="filterCallback" class="p-column-filter" options="{{[1,2]}}"/>
        </template>
        </Column>
        <Column header="Formula" field="cx_formula" sortable>
            <template #filter="{filterModel, filterCallback}">
                <InputText v-model="filterModel.value" type="text" 
                        @input="filterCallback" class="p-column-filter" />
            </template>
            <template #editor="{data, field}">
                <InputText v-model="data[field]"/>
            </template>
        </Column>
        <Column header="Semantics" field="cx_semantics" sortable>
            <template #filter="{filterModel, filterCallback}">
                <Dropdown :options="sem" v-model="filterModel.value" @change="filterCallback" class="p-column-filter" options="{{[1,2]}}"/>
            </template>
            <template #editor="{data, field}">
                <InputText v-model="data[field]"/>
            </template>
        </Column>
        <Column header="SyntType" field="syntactic_type" sortable>
            <template #filter="{filterModel, filterCallback}">
                <Dropdown :options="synt" v-model="filterModel.value" @change="filterCallback" class="p-column-filter" options="{{[1,2]}}"/>
            </template>
            <template #editor="{data, field}">
                <InputText v-model="data[field]"/>
            </template>
        </Column>
        <Column :rowEditor="true"/>
</DataTable>
<Dialog modal v-model:visible="confirmDialog" header="Warning" style="width: 90%;">
<div class="pb-3">You are trying to edit an already existing construction. </div>
<div v-if="cxReferenced">
<DataTable small :value="cxInfo" v-model:expanded-rows="expandedExamples" @rowExpand="checkIfRowEmpty" dataKey="routine_id"
            strippedRows>
            <template #header>References</template>
            <Column field="routine_id" header="ID"></Column>
            <Column field="routine" header="Routine"></Column>
            <Column field="pragmatics" header="Pragmatics">
                <template #body="{data, field}">
                    <div class="flex flex-wrap flex-row gap-1">
                        <Tag v-for="p of data[field]" :value="p"/>
                    </div>
                </template>
            </Column>
            <Column expander></Column>
            <template #expansion="slotProps">
                    <div v-if="slotProps.data.reduction" class="flex justify-content-center py-3 text-lg font-bold">Changes</div>
                    <div class="flex justify-content-center">
                        <DataTable small v-if="slotProps.data.reduction" :value="slotProps.data.reduction" style="width: 80%;">
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
    <div class="flex flex-row justify-content-center py-3 gap-3 font-lg">
        <div class="flex align-items-center"> Would you like to apply your changes to these references?</div>
        <div class="flex align-items-center">
        <RadioButton v-model="applyChanges" inputId="applyTrue" name="apply" :value="true" />
        <label for="ingredient1" class="ml-2">Apply</label>
    </div>
    <div class="flex align-items-center">
        <RadioButton v-model="applyChanges" inputId="applyFalse" name="create new" :value="false" />
        <label for="ingredient2" class="ml-2">Create another instance</label>
    </div>
    </div>
        </div>
    <div class="flex flex-row justify-content-center">
        <Button label="Save Cx" @click="saveEdit"/>
    </div>
</Dialog>
<Button label="Save" @click="closeSelfAndSave" />
</template>
<script setup>
import { onMounted, inject, ref, defineProps } from 'vue';
import { FilterMatchMode } from 'primevue/api';
import { useToast } from 'primevue/usetoast';
import {store} from '../store.js'

const dialogRef = inject('dialogRef');
const closeSelfAndSave = () => {
    dialogRef.value.close({
            newCxIds: store.selectedCxs.map(cx => cx.cx_id)
        });
}


const props = defineProps(['langSwitch', 'scrollHeight'])
const toast = useToast()
const confirmDialog = ref(false)
const cxReferenced = ref(false)
const changes = ref({})
const cxInfo = ref()
const applyChanges = ref(true)
const savingRowData = ref()

const showPickedOnly = ref(false)
var bufferCxs = []

const unselectCx = (event) => {
    console.log(event)
    // lahko bi še dodala confirmation popup
    store.cxExamples[event.data.cx_id] = []
    store.cxReductions[event.data.cx_id] = []
}

const switchPickedShow = () => {
    if (editingRows.value.length) {
        showPickedOnly.value = !showPickedOnly.value
        toast.add({summary: 'Finish editing first', life: 2000})
        return false
    }
    if (showPickedOnly.value) {
        if (!store.selectedCxs.length) {
            showPickedOnly.value = false
            return false
        }
        bufferCxs = store.allConstructions
        store.allConstructions = store.selectedCxs
        return true
    }
    else {
        var merged = []
        for (let i = 0; i < bufferCxs.length; i++) {
            const inNew = store.allConstructions.filter(item => item.cx_id === bufferCxs[i].cx_id)
            if (inNew.length === 1) {
                console.log(inNew[0].cx_id, 'using pickedonly')
                merged.push(inNew[0])
            }
            else {
                console.log('using buffer')
                merged.push(bufferCxs[i])
            }
        }
        merged.sort((a, b) => a.cx_id - b.cx_id)
        store.allConstructions = merged
    }
}

const changedLang = () => {
    filters.value.lang.value = store.curLang.lang
}

const removeEmptyNew = (event) => {
    if (event.newData.cx_id > maxId.value) {
        store.allConstructions = store.allConstructions.filter(c => c.cx_id !== event.newData.cx_id)
    }
}

const saveEdit = async () => {
    if (applyChanges.value) {
        await updateCx()
        confirmDialog.value = false
    }
    else {
        await saveNewCx(savingRowData.value)
        confirmDialog.value = false
    }
}


const expandedExamples = ref({})
const checkIfRowEmpty = (event) => {
    console.log(event)
    if (event.data.examples || event.data.reduction) {
        return true
    }
    else {
        // event.preventDefault()
        console.log(expandedExamples.value)
        delete expandedExamples.value[event.data.routine_id]
        console.log(expandedExamples.value)
    }
}
const saveEditCheck = (event) => {
    const row = store.allConstructions.filter(c => c.cx_id === event.newData.cx_id)[0]
    console.log(row)
    console.log(event)
    if (row.cx_id > maxId.value) {
        console.log('saving new')
        saveNewCx(event.newData)
    }
    else {
        if (row.cx_formula === event.newData.cx_formula && row.cx_semantics === event.newData.cx_semantics && row.syntactic_type === event.newData.syntactic_type) {
            console.log('same')
            return true
        }
        else {
            console.log('tried to change existing')
            if (row.cx_formula !== event.newData.cx_formula) {
                changes.value['cx_formula'] = {'old': row.cx_formula, 'new': event.newData.cx_formula}}
            if (row.cx_semantics !== event.newData.cx_semantics) {
                changes.value['cx_semantics'] = {'old': row.cx_semantics, 'new': event.newData.cx_semantics}}
            if (row.syntactic_type !== event.newData.syntactic_type) {
                changes.value['syntactic_type'] = {'old': row.syntactic_type, 'new': event.newData.syntactic_type}}
            savingRowData.value = event.newData
            confirmDialog.value = true
            getCxInfo(row.cx_id)
        }
    }
}

const updateCx = async() => {
    const response = await fetch(
        'http://localhost:7000/update-construction-info',
        {
            mode: 'cors',
                method: 'POST',
                headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(savingRowData.value)
        }
    )
    const received = await response.json()
    if (received.allgood) {
        toast.add({severity: 'success', summary: 'Success', detail: 'Construction '  + savingRowData.value.cx_id + ' updated'})
        if (store.selectedCxs.filter(c => c.cx_id == savingRowData.value.cx_id)) {
            const allsWOit = store.selectedCxs.filter(c => c.cx_id !== savingRowData.value.cx_id)
            store.selectedCxs = [...allsWOit, savingRowData.value]
        }
        const allWOit = store.allConstructions.filter(c => c.cx_id !== savingRowData.value.cx_id)
        store.allConstructions = [...allWOit, savingRowData.value].sort((a, b) => a.cx_id - b.cx_id)
        console.log(store.allConstructions)
    }
}

const getCxInfo = async(cx_id) => {
    const response = await fetch(
        'http://localhost:7000/get-one-construction',
        {
            mode: 'cors',
                method: 'POST',
                headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({cx_id})
        }
    )
    const received = await response.json()
    if (!(received.length == 1 && received[0] === null)) {
        cxInfo.value = received
        cxReferenced.value = true
    }
}


const saveNewCx = async(newData) => {
    console.log(newData)
    const response = await fetch(
        'http://localhost:7000/add-construction',
            {
                mode: 'cors',
                method: 'POST',
                headers: {
              "Content-Type": "application/json"
            },
        body: JSON.stringify(newData)}
    )
    const received = await response.json()
    if (received.allgood) {
        toast.add({severity: 'success', summary: 'Construction saved', detail: 'Construction added, id'+received.cx_id, life: 3000})
        await loadCxs()
        newData['cx_id'] = received.cx_id
        store.selectedCxs = [...store.selectedCxs, newData]
        // return to the show picked only state after the reload
        if (showPickedOnly.value) {
            console.log('switching')
            switchPickedShow()
        }
    }
    else {
        toast.add({severity: 'error', summary: 'Insuccessful', detail: received.problem, life: 3000})
        editingRows.value = [...editingRows.value, newData]
        return false
    }
}

const filters = ref({
    lang: {value: store.curLang.lang, matchMode: FilterMatchMode.STARTS_WITH},
    cx_formula: {value: null, matchMode: FilterMatchMode.CONTAINS},
    syntactic_type: {value: null, matchMode: FilterMatchMode.EQUALS},
    cx_semantics: {value: null, matchMode: FilterMatchMode.EQUALS},
});

const editIfNew = (event) => {
    const row = store.allConstructions[event.index]
    if (row.cx_id > maxId.value) {
        console.log('new')
    }
    else {
        console.log('old')
        // editingRows.value = editingRows.value.filter(r => r != row)
    }

}

const removeDuplicates = (ar) => {
    return ar.filter((value, index, array) => array.indexOf(value) === index);
}

const loadCxs = async() => {
    const response = await fetch(
        'http://localhost:7000/get-constructions-simple',
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
    sem.value = removeDuplicates([...recieved].map(item => item.cx_semantics))
    synt.value = removeDuplicates([...recieved].map(item => item.syntactic_type))
    const ids = [...recieved].map(item=>item.cx_id)
    // console.log(ids)
    maxId.value = Math.max(...ids)
    // console.log(maxId.value)
    console.log('max id', maxId.value)
}

const addCxRow = () => {
    const newRow = {'cx_id': maxId.value+nAddedRows.value+1, 'lang': store.curLang.lang, 'lang_id':store.curLang.lang_id, 'cx_formula':null, 'cx_semantics': null, syntactic_type: null}
    console.log('newRow', newRow)
    store.allConstructions = [...store.allConstructions, newRow]
    editingRows.value = [...editingRows.value, newRow]
}

const GetLangs = async() => {
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
    langs.value = [...received].map(item => item.lang)
}

const sem = ref([])
const synt = ref([])
const langs = ref([])
const maxId = ref()
const nAddedRows = ref(0)
const editingRows = ref([])
onMounted(async() => {
    await GetLangs()
    await loadCxs()
})
</script>