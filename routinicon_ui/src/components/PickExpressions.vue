<template>
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
            <Column field="expr_id" header="Expr"></Column>
            <Column field="expr_full" header="Expr"></Column>
            <Column field="glossing" header="Glossing"></Column>
        </DataTable>
    </template>
    <template #footer>
        <Button label="Save" @click="closeSelfAndSave"/>
    </template>
</Card>
<Dialog v-model:visible="newExprVisible" @after-hide="NewExprAdded">
    <new-expression :predefinedLanguage="true"/>
</Dialog>
</template>
<script setup>

// import { defineProps } from 'vue';
import { store } from '../store'
import { inject, onBeforeMount, onMounted, ref } from 'vue';
import { FilterMatchMode } from 'primevue/api';
import { onBeforeUnmount } from 'vue';


const dialogRef = inject('dialogRef');
const closeSelfAndSave = () => {
    dialogRef.value.close({
            exprIds: store.pickedExpressions.map(e => e.expr_id)
        });

}
    
// const props = ['curLang']

const newExprVisible = ref(false)
const existingExpressions = ref([])
const showingOnlyPicked = ref(true)

const showPickedOnly = (switchValue) => {
    if (switchValue) {
        console.log('hiding non-selected', switchValue)
        existingExpressions.value = [...store.pickedExpressions]
        console.log(existingExpressions.value)
    }
    else {
        console.log('showing all')
        GetAllExpressions()
    }
}

async function NewExprAdded() {
    await GetAllExpressions()
    const newExpr = existingExpressions.value.filter(e => e.expr_id === store.newExrSubmittedId)[0]
    console.log('NewExprAdded', newExpr);
    if (newExpr !== undefined) 
        {
            console.log('not undefined')
            store.pickedExpressions = [...store.pickedExpressions, newExpr]
        }
    showPickedOnly(true)
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

const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }})

onBeforeMount (async() => {
    console.log(store.curLang)
    await GetAllExpressions()
    showPickedOnly(true)
})

onBeforeUnmount (() => {
})
</script>