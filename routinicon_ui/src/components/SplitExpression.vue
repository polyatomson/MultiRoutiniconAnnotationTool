<template>
    <BlockUI :blocked="props.invalidate" :pt="{ mask: {class: 'bg-white opacity-20'} }">
<Card :pt="{ 
        header: { class: 'bg-primary border-round-lg' }, 
        title: {class: 'flex justify-content-center'},
        content: { class: 'flex flex-column row-gap-1' }, 
        footer: { class: 'flex justify-content-center'} 
        }">
<template #header>
            <div style="height: 1rem;"></div>
            <!-- <img alt="user header" src="../assets/random_header.png" /> -->
</template>

<template #title>Step #2</template>

<template #content>
        <DataTable v-model:editingRows="editingRows" :value="unitsInfo" editMode="row" dataKey="n" @row-edit-init="chooseSuggestions" @row-edit-save="onRowEditSave"
    :pt="{
        table: { style: 'min-width: 50rem' },
        column: {
            bodycell: ({ state }) => ({
              style:  state['d_editing']&&'padding-top: 0.6rem; padding-bottom: 0.6rem'
            })
        }
    }">
    <Column field="n" header="N"></Column>
    <Column field="unit" header="Word"></Column>
    <Column field="realization" header="Realization">
      <template #editor="{ data, field }">
        <AutoComplete v-model="data[field]" :suggestions="suggRealizations" dropdown 
        @complete="searchRealizations"/>
        </template>
    </Column>
    <Column field="lemma" header="Lemma">
      <template #editor="{ data, field }">
            <AutoComplete v-model="data[field]" :suggestions="suggLemmas" 
            optionGroupLabel="group" optionGroupChildren="items"
            dropdown 
            @complete="searchLemmas"/>
        </template>
    </Column>
    <Column field="pos" header="POS">
        <template #body="{ data, field }">
            {{ data[field].toUpperCase() }}
        </template>
      <template #editor="{ data, field }">
            <AutoComplete v-model="data[field]" :suggestions="suggPos" 
            optionGroupLabel="group" optionGroupChildren="items"
            dropdown
            @complete="searchPos"/>
        </template>
    </Column>
    <Column :rowEditor=true style="width: 10%; min-width: 8rem" bodyStyle="text-align:center"></Column>
</DataTable>
</template>
<template #footer>
    <Button icon="pi pi-check" severity="success" label="Submit" @click="FinishStep"></Button>
</template>
</Card>
</BlockUI>
    
    </template>
    <script setup>
    import { defineCustomElement, onMounted } from 'vue';
    import { FilterMatchMode, FilterService } from 'primevue/api';
    import { store } from '../store.js'
    import { ref, watch } from 'vue'

    const props = defineProps(["invalidate"])


    const editingRows = ref([]);
    var units = store.userExpression.expr.split(' ')
    for (let index = 0; index < units.length; index++) {
        if (units[index] == '–' || units[index] == '—' || units[index] == '-') {
            units.splice(index, 1)
        }
        units[index] = units[index].replace("-", "=")
        units[index] = units[index].replace(/[ !\.\?\:,;— ]+/g, "")
        units[index] = units[index].toLowerCase()
    }
    
    const FinishStep = () => {
        // console.log('res', unitsInfo.value)
        store.userExpression.units = unitsInfo.value
        store.userExpression.step = 3
    }


    const searchRealizations = (event) => {
        setTimeout(() => {
        if (!event.query.trim().length) {
            suggRealizations.value = [...allRealizations]
        } else {
            suggRealizations.value = [...allRealizations].filter((real) => {
                return real.includes(event.query.toUpperCase())
            }
        )
        }
        
    }, 250)
    }

    const searchLemmas = (event) => {
        let query = event.query;
        let newSuggLemma = [];
        // console.log(allLemmas.value)
        for (let group of allLemmas.value) {
        let filteredItems = FilterService.filter(group.items, ['group'], query, FilterMatchMode.CONTAINS);
        if (filteredItems && filteredItems.length) {
            newSuggLemma.push({...group, ...{items: filteredItems}});
        }
    }
    suggLemmas.value = newSuggLemma;
}

    const searchPos = (event) => {
        let query = event.query;
        let newSuggPos = [];
        // console.log(allPos.value)
        for (let group of allPos.value) {
        let filteredItems = FilterService.filter(group.items, ['group'], query, FilterMatchMode.CONTAINS);
        if (filteredItems && filteredItems.length) {
            newSuggPos.push({...group, ...{items: filteredItems}});
        }
    }

    suggPos.value = newSuggPos;
    }

    const unitsInfo = ref()
    
    let allPos = ref([])
    const suggPos = ref([])
    let allLemmas = ref([])
    const suggLemmas = ref()
    let allRealizations = []
    const suggRealizations = ref()
    
    async function chooseSuggestions(event) {
        // console.log("editing row", event.data.n)
        const rowIndex = event.data.n
        // allPos.value = []
        if (allPos.value.length > 1) {
            allPos.value[0] = {group: "Recommended", items: store.unitsSuggestions[rowIndex].poses}
        }
        else {
            allPos.value.unshift({group: "Recommended", items: store.unitsSuggestions[rowIndex].poses})
        }
        if (allLemmas.value.length > 1) {
            allLemmas.value[0] = {group: "Recommended", items: store.unitsSuggestions[rowIndex].lemmas}
        }
        else {
            allLemmas.value.unshift({group: "Recommended", items: store.unitsSuggestions[rowIndex].lemmas})
        }
        // allLemmas = store.unitsSuggestions[rowIndex].lemmas
        allRealizations = store.unitsSuggestions[rowIndex].realizations
    }



    async function getUnitsInfo(units) {
        console.log()
        if ((store.userExpression.previousStep>2 
        || store.userExpression.step>2) 
        ||  (store.userExpression.units.length && store.userExpression.expr == store.userExpression.previousExpr)){
            
            unitsInfo.value = store.userExpression.units
            if (store.userExpression.step==2) {
            store.userExpression.unitsChanged = false}
            console.log("keeping units info")
            return false
            
        }
        else {
            console.log("loading new units info")
        }
    const lang = store.userExpression.lang
    const lang_id = store.langIds.filter(item => item.lang === lang)[0].lang_id
    const lang_id_str = JSON.stringify({"lang_id": lang_id, "units": units})
    const response = await fetch(
          'http://localhost:7000/units-suggestions', 
          {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: lang_id_str,
          })
    const received = await response.json();
    // console.log('recieved', received)
    unitsInfo.value = []
    for (let index = 0; index < units.length; index++) {
        const newRowIndex = index+1
        
        const unit = units[index];
        const info = received[unit]
        
        store.unitsSuggestions[newRowIndex] = {realizations: [], lemmas: [], poses: []}
        
        if (info != null) {
            for (let index2 = 0; index2 < info.length; index2++) {
            store.unitsSuggestions[newRowIndex].lemmas.push(info[index2].lemma)
            store.unitsSuggestions[newRowIndex].realizations.push(info[index2].realization)
            store.unitsSuggestions[newRowIndex].poses.push(info[index2].pos)
            }
        
            const ready_row = Object.assign({}, info[0])
            ready_row.n = newRowIndex
            unitsInfo.value.push(ready_row)
        }
        else {
            // console.log('pridem sem')
            unitsInfo.value.push({"n":newRowIndex, "unit": unit, "realization":unit, "lemma": unit, pos: ""})
        }
    }
}

    async function getLemmasforLanguage() {
        const lang = store.userExpression.lang
        console.log('language', lang)
        if (store.userExpression.previousStep > 2) {
            console.log('reusing lemmas')
            allLemmas.value.push({group: "All", items: store.lemmas[lang]})
            console.log('allLemmas', allLemmas.value)
            return false
        }
        else {
            console.log("not reusing lemmas")
        }
        
        const lang_id = store.langIds.filter(item => item.lang === lang)[0].lang_id
        const lang_id_str = JSON.stringify({"lang_id": lang_id})
        const response = await fetch(
          'http://localhost:7000/lemmas', 
          {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: lang_id_str,
          })
        const received = await response.json();
        store.lemmas[lang] = received
        // store.lemmas = received
        allLemmas.value.push({group: "All", items: received})
    }

    async function getPOSesforLanguage() {
        const lang = store.userExpression.lang

        if (store.userExpression.previousStep > 2) {
            console.log('reusing poses')
            allPos.value.push({group: "All", items: store.poses[lang]})
            return false
        }
        else {
            console.log("not reusing poses")
        }

        const lang_id = store.langIds.filter(item => item.lang === lang)[0].lang_id
        const lang_id_str = JSON.stringify({"lang_id": lang_id})
        const response = await fetch(
          'http://localhost:7000/poses', 
          {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: lang_id_str,
          })
        const received = await response.json();
        store.poses[lang] = received
        allPos.value.push({group: "All", items: received})
    }
    
    const onRowEditSave = (e) => {
        let { newData, index } = e;
            // console.log(index)
            if (JSON.stringify(unitsInfo.value[index]) !== JSON.stringify(newData)) {
                console.log('row changed')
                console.log('old', unitsInfo.value[index])
                console.log('new', newData)
            unitsInfo.value[index] = newData;
            store.userExpression.unitsChanged = true
        }
        else {
            console.log('no change')
        }
            // console.log('saved unitsInfo')
            // const gloss_row = JSON.stringify(unitsInfo.value[index])
            // console.log(gloss_row)
    }

    // console.log(unitsInfo)
     onMounted(async () => {
        // createInitialUnits()
        
        getLemmasforLanguage()
        getPOSesforLanguage()
        getUnitsInfo(units)
    })
    </script>
    
    <style>
    
    </style>