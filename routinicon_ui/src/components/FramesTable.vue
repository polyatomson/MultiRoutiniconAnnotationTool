<template>
    <Toast />
            <div class="flex justify-content-center pb-1">
                <Button v-show="showSave" icon="pi pi-save" text @click="closeSelfAndSave" />
                <div class="flex flex-grow-1"/>
                <SelectButton v-model="pickedLang" :options="store.langIds" optionLabel="lang"
                            aria-labelledby="basic" inputId="user_lang"
                            :allowEmpty = true
                            @change="ChangeLanguage">
                </SelectButton>
            </div>
            <DataTable :value="frames" 
             resizableColumns columnResizeMode="fit" showGridlines 
             v-model:expandedRows="expandedRows" dataKey="frame_id"
             v-model:selection="store.selectedFrames"
             v-model:filters="filters"
             filterDisplay="row"
             scrollable
             scroll-height="30rem"
             :globalFilterFields="['examples', 'pragmatics', 'sit_tags']">
             <template #header>
                <div class="flex flex-row gap-1">
                    <div class="flex align-items-center">
                        <Button icon="pi pi-plus" @click="newFrameFromScratch=true" />
                    </div>
                    <div class="flex flex-grow-1"></div>
                    <div class="flex align-items-center">
                        <InputText v-model="filters['global'].value" placeholder="Keyword Search"/>
                    </div>
                </div>
      </template>
                <Column selectionMode="multiple">
                <template #header>
                    <InputSwitch v-model="showingOnlyPicked" label="Selected" @update:model-value="showPickedOnly"/>
                </template>
            </Column>
                <Column expander style="width: 3rem" />
                <Column field="situation_structure" header="SitStruct">
                    <template #filter="{ filterModel, filterCallback }">
                        <Dropdown v-model="filterModel.value" @change="filterCallback()" :options="structOptions" class="p-column-filter" style="min-width: 3rem" :showClear="false" />
                    </template>
                    <template #body="{data, field}">
                        <Tag class="text-base" :value="shortenStructure(data[field])" rounded severity="danger"/>
                    </template>
                </Column>
                <Column field="pragmatics" header="Pragmatics">
                    <template #filter="{ filterModel, filterCallback }">
                        <Dropdown v-model="filterModel.value" @change="filterCallback()" :options="pragmOptions" class="p-column-filter" style="min-width: 3rem" :showClear="false"/>
                    </template>
                    <template #body="{data, field}">
                        <div class="flex flex-row gap-2 flex-wrap">
                            <Tag v-for="t in data[field]" :value="t"/>
                        </div>
                        <i v-if="!data[field].length" class="pi pi-minus"></i>
                    </template>
                </Column>
                <Column field="sit_tags" header="Tags">
                    <template #filter="{ filterModel, filterCallback }">
                        <Dropdown v-model="filterModel.value" @change="filterCallback()" :options="tagsOptions" class="p-column-filter" style="min-width: 3rem" :showClear="false"/>
                    </template>
                    <template #body="{data, field}">
                        <div class="flex flex-row gap-2 flex-wrap">
                            <Tag v-for="t in data[field]" :value="t"/>
                        </div>
                        <i v-if="!data[field].length" class="pi pi-minus"></i>
                    </template>
                </Column>
                <Column header="Conditions" field="usage_conditions">
                    <template #filter="{ filterModel, filterCallback }">
                        <Dropdown v-model="filterModel.value" @change="filterCallback()" :options="condCategoryOptions" class="p-column-filter" style="min-width: 3rem" :showClear="false"/>
                    </template>
                    <template #body="{data}">
                        <div class="flex flex-wrap gap-3">
                            <Tag v-for="c in data.usage_conditions" :value="c.category"></Tag>
                            <div v-if="!data.usage_conditions.length">&mdash;</div>
                        </div>
                    </template>
                </Column>
                <Column field="examples" header="Examples">
                    <template #filter="{ filterModel, filterCallback }">
                        <InputText v-model="filterModel.value" @change="filterCallback()"/>
                    </template>
                        <template #body="{data, field}">
                            <div class="flex flex-row gap-2 flex-wrap">
                                <Tag v-for="r in data[field].slice(0,3)" style="background-color: var(--surface-000); 
                                color: var(--surface-700); border: 1px; 
                                border-color: var(--surface-300); border-style: solid; font-weight: normal;" rounded>
                                    <div class="flex align-items-center gap-2 px-1">
                                        <Badge :value="r.lang" rounded label=""></Badge>
                                        <span>{{r.r}}</span>
                                    </div>
                                </Tag>
                            </div>
                            <i v-if="!data[field].length" class="pi pi-minus"></i>
                    </template>
                </Column>
                <Column>
                    <template #body="slotProps">
                        <SplitButton size="small" icon="pi pi-cog" :model="[
                            {icon: 'pi pi-clone', label: 'Clone', command: () => {useAsTemplate(slotProps)}},
                            {icon: 'pi pi-pencil', label: 'Edit', command: () => {eFrame(slotProps)}},
                            {icon: 'pi pi-trash', label: 'Delete', command: () => {deleteFrame(slotProps)}, disabled: slotProps.data.examples.length}
                            ]" >
                        </SplitButton>
                    </template>
                </Column>
                <template #expansion="slotProps">
                    <div class="p-1">
                        <strong>Situation structure</strong>
                        <DataTable :value="[slotProps.data.situations]" class="py-3"
                        >
                            <Column v-if="'trigger' in slotProps.data.situations && slotProps.data.situations.trigger?.length" field="trigger" header="Trigger">
                                <template #body="{data, field}">
                                    <div class="flex flex-row flex-wrap gap-2">    
                                        <Tag v-for="tag of data[field]" :value="tag" severity="secondary"/>
                                    </div>
                                </template>
                            </Column>
                            <Column v-if="'action' in slotProps.data.situations && slotProps.data.situations.action?.length" field="action" header="Action">
                                <template #body="{data, field}">
                                    <div class="flex flex-row flex-wrap gap-2">    
                                        <Tag v-for="tag of data[field]" :value="tag" severity="secondary"/>
                                    </div>
                                </template>
                            </Column>
                            <Column v-if="'effect' in slotProps.data.situations && slotProps.data.situations.effect?.length" field="effect" header="Effect">
                                <template #body="{data, field}">
                                    <div class="flex flex-row flex-wrap gap-2">
                                        <Tag v-for="tag of data[field]" :value="tag" severity="secondary"/>
                                    </div>
                                </template>
                            </Column>
                        </DataTable>
                        <div><strong>Usage conditions</strong></div>
                        <DataTable v-if="slotProps.data.usage_conditions.length && slotProps.data.usage_conditions[0] !== null" :value="slotProps.data.usage_conditions" class="py-3">
                            <Column field="category" header="Category"/>
                            <Column field="condition" header="Condition" :pt="{body: {class: 'flex flex-wrap'}}"/>
                        </DataTable>
                            <div v-else class="flex justify-content-center"><i class="pi pi-minus py-3"></i></div>
                        <div><strong>Examples</strong></div>
                        <div v-if="slotProps.data.frame_examples">
                            <div class="flex flex-column py-2" v-for="ex of slotProps.data.frame_examples">
                                <div class="flex flex-row flex-wrap gap-1">
                                    <span class="flex align-items-center">{{ ex.example}}</span>
                                    <Tag v-if="ex.source" :value="ex.source" class="flex align-items-center"/>
                                    <Tag v-if="ex.dated" :value="ex.dated" class="flex align-items-center"/>
                                </div>
                                <div v-if="ex.translation?.length">'{{ex.translation }}'</div>
                            </div>
                        </div>
                        <div v-else>&mdash;</div> 
                    </div>
                </template>
             </DataTable>

    <Dialog v-model:visible="newFrameFromTemplate" @after-hide="updateFrames" modal>
        <new-frame></new-frame>
    </Dialog>

    <Dialog v-model:visible="newFrameFromScratch" @after-hide="updateFrames" modal>
        <new-frame></new-frame>
    </Dialog>

    <Dialog v-model:visible="editingFrame" @after-hide="collectFrames()" modal>
        <edit-frame></edit-frame>
    </Dialog>
    </template>
<script setup>
import { ref, onMounted, onBeforeMount, watch, inject } from 'vue';
import { store } from '../store';
import { FilterMatchMode, FilterService } from 'primevue/api';
import { defineProps } from 'vue';



const dialogRef = inject('dialogRef');

const showSave = ref(false)

const closeSelfAndSave = () => {
    dialogRef?.value.close({
            frameIds: store.selectedFrames.map(e => e.frame_id)
        });
}

defineProps({'scrollHeight': '30rem'})
const newFrameFromTemplate = ref(false)
const newFrameFromScratch = ref(false)
const editingFrame = ref(false)

const eFrame = (row) => {
    console.log('useas', row)
    store.userFrame.editing = true
    store.userFrame.fullFrame.sitStructure = row.data?.situation_structure
    store.userFrame.fullFrame.events.triggers = row.data?.situations.trigger || []
    store.userFrame.fullFrame.events.actions = row.data?.situations.action || []
    store.userFrame.fullFrame.events.effects = row.data?.situations.effect || []
    store.userFrame.fullFrame.tags = row.data?.sit_tags
    store.userFrame.fullFrame.conditions = row.data?.usage_conditions
    store.userFrame.fullFrame.pragmatics = row.data?.pragmatics
    store.userFrame.fullFrame.frame_id = row.data?.frame_id
    console.log('wrote all into store')
    editingFrame.value = true
}

const deleteFrame = async(row) => {
    const frame_id = row.data.frame_id
    const response = await fetch('http://localhost:7000/delete-frame',
        {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({frame_id})
        })
    const received = response.json()
    await collectFrames()
}

const showingOnlyPicked = ref(false)

const showPickedOnly = (event) => {
    console.log(event)
    if (event) {
        console.log('hiding non-selected', event)
        frames.value = [...store.selectedFrames]
        console.log(store.selectedFrames)
    }
    else {
        console.log('showing all')
        collectFrames()
    }
}

async function updateFrames() {
    await collectFrames()
    console.log(store.newFrameSubmittedId)
    const newFrame = frames.value.filter(f => f.frame_id === store.newFrameSubmittedId)[0]
    console.log(newFrame)
    store.selectedFrames = [...store.selectedFrames, newFrame]
}

const useAsTemplate = (row) => {
    console.log('useas', row)
    newFrameFromTemplate.value = true
    store.userFrame.reusing = true
    store.userFrame.fullFrame.sitStructure = row.data.situation_structure
    store.userFrame.fullFrame.events.triggers = row.data.situations.trigger || []
    store.userFrame.fullFrame.events.actions = row.data.situations.action || []
    store.userFrame.fullFrame.events.effects = row.data.situations.effect || []
    store.userFrame.fullFrame.tags = row.data.sit_tags
    store.userFrame.fullFrame.conditions = row.data.usage_conditions
    store.userFrame.fullFrame.pragmatics = row.data.pragmatics
}

const ROUTINES_FILTER = ref('ROUTINES_FILTER')
const CONDITION_FILTER = ref('CONDITION_FILTER')

FilterService.register(ROUTINES_FILTER.value, (value, filter) => {
    if (filter === undefined || filter === null || filter.trim() === '') {
        return true;
    }

    if (value === undefined || value === null) {
        return false;
    }

    const result = value.filter((item) => item.r.startsWith(filter)).length > 0
    return result
});

FilterService.register(CONDITION_FILTER.value, (value, filter) => {
    if (filter === undefined || filter === null || filter.trim() === '') {
        return true;
    }

    if (value === undefined || value === null) {
        return false;
    }

    const result = value.filter((item) => item.category === filter).length > 0
    return result
})

const filters = ref({
                global: { value: null, matchMode: FilterMatchMode.CONTAINS },
                situation_structure: { value: null, matchMode: FilterMatchMode.EQUALS},
                pragmatics: {value: null, matchMode: FilterMatchMode.CONTAINS},
                sit_tags: {value: null, matchMode: FilterMatchMode.CONTAINS},
                examples: {value: null, matchMode: ROUTINES_FILTER.value},
                usage_conditions: {value: null, matchMode: CONDITION_FILTER.value}
            })

const frames = ref([])
const pickedLang = ref(null)
// const langs = ref()
const expandedRows = ref()

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

const structOptions = ref(["reaction", "prompt", "reaction + prompt", "accompaniment"])
const pragmOptions = ref([])
const tagsOptions = ref([])
const condCategoryOptions = ref([])
// const langOptions = ref()

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
    // langOptions.value = received.map((l) => l.lang_id)
    console.log('langs', store.langIds)
    console.log('lang', pickedLang.value)
}

async function ChangeLanguage(event) {
    pickedLang.value = event.value
    console.log(pickedLang.value)
    collectFrames()
}

async function collectFrames() {
    const lang_id = pickedLang.value?.lang_id || pickedLang.value
    const response = await fetch(
          'http://localhost:7000/get-all-frames', 
          {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({'lang_id': lang_id})
          }
          )
    const received = await response.json();
    frames.value = received
    return true
}

async function getTags() {
    const response = await fetch(
        'http://localhost:7000/get-frame-tags',
        {method: 'GET',
            headers: {
              "Content-Type": "application/json"
            }
        })
    const received = await response.json()
    pragmOptions.value = received.structure.p
    tagsOptions.value = received.stags
    const cats = received.conditions.map(c => c.category)
     condCategoryOptions.value = cats.filter((cat,ind) => cats.indexOf(cat) === ind)
     console.log(condCategoryOptions.value)
    return received
}

watch (() => store.newFrameSubmittedId, async(newId, oldId) => {
    console.log('frame submitted')
    newFrameFromScratch.value = false
    newFrameFromTemplate.value = false

})

onBeforeMount(async () => {
    const tags = await getTags()
    store.frameAnnotation = tags
    GetLangs()
})

onMounted(async () => {
    await collectFrames()
    console.log(dialogRef?.value.data)
    if (dialogRef?.value.data.frameIds) {
        store.selectedFrames = frames.value.filter(f => dialogRef.value.data.frameIds.includes(f.frame_id))
        frames.value = frames.value.filter(f => dialogRef.value.data.frameIds.includes(f.frame_id))
        showingOnlyPicked.value = true
        showSave.value = true
    }
})

</script>
<style>

</style>