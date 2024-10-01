<template>
    <Card :pt="{ 
    header: { class: 'bg-primary border-round-lg' }, 
    title: {class: 'flex justify-content-center'},
    content: { class: 'flex justify-content-center' }, 
    footer: { class: 'flex justify-content-center'} 
    }">
        <template #title>
            Usage conditions
        </template>
        <template #header>
            <div style="height: 1rem;"></div>
        </template>
        <template #content>
            <ContextMenu ref="cm" :model="menuModelController()" @hide="selectedRow = null" >
            </ContextMenu>
            <DataTable v-model:selection="pickedConditions" :value="conditions" dataKey="condition_id"
            v-model:filters="filters" filterDisplay="row"
            style="max-width: 60rem;"
            scrollable scrollHeight="20rem"
            :frozenValue="lockedNew"
            :rowClass="getRowClass"
            v-model:editingRows="editingRows" editMode="row" @row-edit-save="onRowEditSave"
            contextMenu v-model:contextMenuSelection="selectedRow" @rowContextmenu="onRowContextMenu"
            >
                <template #header>
                    <div class="flex flex-row align-items-center flex-wrap gap-3">
                        <div class="flex flex-row flex-wrap gap-3">
                            <div class="flex align-items-center"><InputSwitch v-model="selectedOnly" size="small" severity="secondary" @change="showOnlyPicked"/></div>
                            <div class="flex align-items-center">Current conditions</div>
                            <div class="flex align-items-center"><Badge :value="pickedConditions.length" /></div>
                        </div>
                        <div class="flex-grow-1"></div>
                        <div class="flex-none align-items-center"><Button icon="pi pi-plus" size="small" @click="addNewRow" /></div>
                    </div>
                </template>

                <Column selectionMode="multiple" headerStyle="width: 3rem" header="Use">
                </Column>
                <Column field="category" header="Type" 
                sortable style="max-width: 10rem;"
                :showFilterMenu="false">
                    <template #filter="{ filterModel, filterCallback }">
                        <Dropdown v-model="filterModel.value" @change="filterCallback()" 
                        :options="categories" class="p-column-filter"  />
                    </template>
                    <template #editor="{ data, field }">
                        <Dropdown v-model="data[field]" :options="categories" style="min-width: 8rem" />
                    </template>
                </Column>
                <Column field="condition" header="Usage condition" bodyStyle="max-width: 30rem"
                :pt="{body: {class: 'flex flex-wrap'}}">
                    <template #filter="{ filterModel, filterCallback }">
                        <InputText v-model="filterModel.value" type="text" 
                        @input="filterCallback()" class="p-column-filter" />
                    </template>
                    <template #editor="{ data, field }">
                        <InputText v-model="data[field]">
                        </InputText>
                    </template>
                    
                </Column>
                <Column 
                :rowEditor="true" style="width: 10%; min-width: 8rem" 
                bodyStyle="text-align:center"
                :pt="{rowEditorInitButton: (data) => (
                    {style: {'visibility': hideEdit(data)}})
                }"/>
        </DataTable>
    </template>
        
    </Card>

</template>

<script setup>
import { onMounted, ref } from 'vue'
// import { onMounted } from 'vue';
import { store } from '../store.js'
import { FilterMatchMode } from 'primevue/api'
import { watch } from 'vue';
import Button from 'primevue/button';
import InputSwitch from 'primevue/inputswitch';

const conditions = ref([
    {"category": "time", "condition": "Evening", "condition_id": '1'}, 
    {"category": "space", "condition": "Speaker's personal space (home / office)", "condition_id": '2'},
    {"category": "relationship", "condition": "The speaker knows the addressee well", "condition_id": '3'},
    {"category": "time", "condition": "smth else", "condition_id": '4'}
])
const categories = ref(['time', 'space', 'pretext', 'relationship', 'other'])
const pickedConditions = ref([])
const filters = ref({
    condition: {value: null, matchMode: FilterMatchMode.CONTAINS},
    category: {value: null, matchMode: FilterMatchMode.EQUALS}
});
const lockedNew = ref([])
const nNewRows = ref(0)

const getRowClass = (data) => { 
    // console.log(data)
    return [{'bg-green-100': data.condition_id.startsWith('new')}]
}

const addNewRow = () => {
    nNewRows.value += 1
    lockedNew.value.push({"category": "", "condition": "", "condition_id": "new"+nNewRows.value.toString()})
}

const hideEdit = (data) => {
    // const frozen = data.parent.instance.frozenRow
    const customLine = data.parent.props.rowData.condition_id.startsWith('new')
    // console.log()
    if (customLine) {return 'visible'}
    else {return 'hidden'}
}

const onRowEditSave = (event) => {
    let { newData, index } = event;
    const editedId = newData.condition_id
    const inLocked = lockedNew.value.filter((c) => c.condition_id === editedId).length
    if (inLocked){
    lockedNew.value.splice(index, 1)
    conditions.value.unshift(newData)}
    else {
        conditions.value[index] = newData
    }
    pickedConditions.value = [...pickedConditions.value.filter((c) => c.condition_id !== editedId), newData]
    console.log(pickedConditions)

};

const editingRows = ref([]);

const selectedRow = ref()
const cm = ref()

const onRowContextMenu = (event) => {
    console.log('right click', event)
    cm.value.show(event.originalEvent)
};

const menuModelController = () => {
    const cond_id = selectedRow?.value?.condition_id || 'empty'
    // console.log('picking menu', cond_id)
    if (cond_id !== 'empty' && cond_id.startsWith('new')) {
        return [{label: 'Delete', icon: 'pi pi-fw pi-times', command: () => deleteUserCondition()}]
    }
    else {
        return [{label: 'No options'}]
    }
}


const deleteUserCondition = () => {
    console.log('deleting', selectedRow.value)
    lockedNew.value = lockedNew.value.filter((c) => c.condition_id !== selectedRow.value.condition_id);
    conditions.value = conditions.value.filter((c) => c.condition_id !== selectedRow.value.condition_id);
    pickedConditions.value = pickedConditions.value.filter((c) => c.condition_id !== selectedRow.value.condition_id)
    selectedRow.value = null;
};

const reserveConditions = ref()
const selectedOnly = ref(false)
const showOnlyPicked = (event) => {
    if (selectedOnly.value) { 
        reserveConditions.value = [...conditions.value]
        conditions.value = [...pickedConditions.value]
     }
     else {
        const newlyAdded = conditions.value.filter((c) => {
            return reserveConditions.value.filter((rc) => 
            rc.condition_id === c.condition_id).length === 0
        })
        console.log('newly added', newlyAdded)
        conditions.value = [...reserveConditions.value, ...newlyAdded]
        reserveConditions.value = null
     }

}

watch (pickedConditions, async(newConditions, oldCondition) => {
    console.log('watcher works', newConditions)
    store.userFrame.fullFrame.conditions = pickedConditions.value
})

onMounted (() => {
    conditions.value = [...store.frameAnnotation.conditions]
    pickedConditions.value = store.userFrame.fullFrame.conditions
}
)

</script>