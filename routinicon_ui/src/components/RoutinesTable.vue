<template>
    <Card style="overflow: hidden; width: 100%;" class="my-5">
        <template #content>
    <div class="flex justify-content-end">
                <SelectButton v-model="pickedLang" :options="store.langIds" optionLabel="lang"
                            aria-labelledby="basic" inputId="user_lang"
                            class="pb-3"
                            :allowEmpty = true
                            @change="ChangeLanguage">
                </SelectButton>
            </div>
    <ContextMenu ref="cm" :model="menuModel" @hide="menuSelected = null" />
    <DataTable :value="routines" table-style="width: 100%;"
     showGridlines resizable-columns
    v-model:expandedRows="expandedRows" breakpoint="100rem"
    contextMenu v-model:contextMenuSelection="menuSelected"
    @rowContextmenu="onRowContextMenu"
    >
    <Column expander style="width: 3rem"></Column>
    <Column header="ID" field="routine_id"></Column>
    <Column header="Routine" field="routine"></Column>
    <Column header="Lang" field="lang">
        <template #body="{data, field}">
            <Tag :value="data[field]"></Tag>
        </template>
    </Column>
    <Column header="FrameID" field="frame_id"/>
    <Column header="SitStruct" field="situation_structure">
        <template #body="{data, field}">
            <Tag :value="shortenStructure(data[field])" severity="danger" rounded></Tag>
        </template>
    </Column>
    <Column header="Glosses" field="exprs"">
        <template #body="{data, field}">
            <div class="flex flex-row flex-wrap text-sm">{{ data[field][0].glossing }}</div>
        </template>
    </Column>
    <Column header="Pragmatics" field="pragmatics">
        <template #body="{data, field}">
            <div class="flex flex-wrap flex-row gap-1">
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
    <Column frozen>
        <template #body="{data}">
            <ConfirmPopup />
            <Button icon="pi pi-trash" severity="danger" @click="confirmDeletion($event, data)"/>
        </template>
    </Column>
    <template #expansion="slotProps">
        <div class="p-1">
            <div v-if="slotProps.data.frame_id"><strong>Situation structure</strong></div>
            <DataTable v-if="slotProps.data.frame_id" :value="[slotProps.data]" class="py-3">
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
            <div><strong>Variation</strong></div>
            <DataTable v-if="slotProps.data.exprs.length" :value="slotProps.data.exprs" dataKey="expr_id" class="py-3">
                <Column field="expr_full" header="Expression"></Column>
                <Column field="realization" header="Realization"></Column>
                <Column field="glossing" header="Glosses"></Column>
                <Column field="lemmas" header="Lemmas"></Column>
                <Column field="pos" header="POS"></Column>
            </DataTable>
        </div>
        <div class="p-1">    
            <div v-if="slotProps.data.cxs?.length"><strong>Constructions</strong></div>
                <DataTable v-if="slotProps.data.cxs?.length" :value="slotProps.data.cxs" class="py-3" v-model:expanded-rows="expandedCxs"
                columnResizeMode="fit">
                    <Column header="ID" field="cx_id"></Column>
                    <Column field="formula" header="Formula"/>
                    <Column header="Semantics" field="semantics"/>
                    <Column header="SyntType" field="syntactic_type" />
                    <Column expander/>
                    <template #expansion="slotProps">
                    <div class="flex py-3 text-lg font-bold">Changes</div>
                    <DataTable :value="slotProps.data.reductions" columnResizeMode="fit">
                        <Column field="reduction_id"/>
                        <Column field="change" header="Change"></Column>
                        <Column field="component" header="Element"></Column>
                        <Column field="sem_role" header="SemRole"></Column>
                    </DataTable>

                        <div class="flex py-3 text-lg font-bold">Examples</div>
                        <DataTable :value="slotProps.data.examples" scrollable resizableColumns>
                            <Column field="example_id" header="ID"></Column>
                            <Column field="example" header="Example"></Column>
                            <Column field="translation" header="Translation"></Column>
                            <Column field="source" header="Source"></Column>
                            <Column field="dated" header="Year"></Column>
                        </DataTable>
                    </template>
                </DataTable>
        </div>

        <div class="p-1">    
        <div><strong>Usage conditions</strong></div>
            <DataTable v-if="slotProps.data.usage_conditions?.length" :value="slotProps.data.usage_conditions" class="py-3">
                <Column field="category" header="Category"/>
                <Column field="condition" header="Condition" :pt="{body: {class: 'flex flex-wrap'}}"/>
            </DataTable>
        </div>
        <div  v-if="slotProps.data.definition !== null" class="p-1">
            
            <Card>
                <template #header><div class="pt-2"><strong>Definition</strong></div></template>
                <template #content>{{ slotProps.data.definition }}</template></Card>
        </div>
        <div v-if="slotProps.data.intonation !== null" class="p-1">
                <div class="pt-2"><strong>Intonation</strong></div>
                {{ slotProps.data.intonation }}
        </div>
        <div v-if="slotProps.data.comments !== null" class="p-1">
                <div class="pt-2"><strong>Comments</strong></div>
                {{ slotProps.data.comments }}
        </div>
        <div  v-if="slotProps.data.examples_for_case !== null" class="p-1">
            <div class="py-3"><strong>Examples</strong></div>
                <div class="flex flex-column gap-3">
                    <div v-for="e of slotProps.data.examples_for_case">
                        <div class="flex flex-row gap-2 align-items-center">
                            <i class="pi pi-circle-fill" style="font-size: 0.5rem"></i>
                            <em>{{e.example }}</em> 
                            <Tag v-if="e.source" :value="e.source" severity="secondary"/>
                        </div>
                            <div v-if="e.translation">'{{ e.translation }}'</div>
                    </div>
                </div>
        </div>
    </template>
    </DataTable>
    </template>
</Card>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { store } from '../store'
import { useConfirm } from 'primevue/useconfirm'
import { useRouter } from 'vue-router';

const router = useRouter()
const cm = ref()

const onRowContextMenu = (event) => {
    cm.value.show(event.originalEvent);
};

const menuSelected = ref()
const menuModel = ref([
    {label: 'Edit', icon: 'pi pi-fw pi-search', command: () => router.push({name: 'routine', params: {id: menuSelected.value.routine_id}}) }]
);



const confirm = useConfirm();

const deleteRoutine = async(routine_id) => {
    const response = await fetch(
        'http://localhost:7000/delete-routine',
        {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(routine_id)
        })
    const received = await response.json()
    collectRoutines()
}

const confirmDeletion = (event, data) => {
    console.log(data)
    confirm.require({
        target: event.currentTarget,
        message: 'Are you sure you want to delete the routine ' + data.routine + '? This will destroy all its records in all the frames.',
        icon: 'pi pi-exclamation-triangle',
        rejectClass: 'p-button-sm p-button-outlined',
        acceptClass: 'p-button-danger p-button-sm p-button-outlined',
        rejectLabel: 'Cancel',
        acceptLabel: 'Delete',
        accept: () => {
            deleteRoutine(data.routine_id)
        },
        reject: () => {
            console.log('canceling deletion')
        }
    });
};

const expandedRows = ref()
const expandedCxs = ref()
const pickedLang = ref()

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
    console.log('langs', store.langIds)
    // console.log('lang', pickedLang.value)
}

async function ChangeLanguage() {
    collectRoutines()
}

async function collectRoutines() {
    var lang_ids = null
    if (pickedLang.value) {lang_ids = Array.of(pickedLang.value.lang_id)}
    else {lang_ids = []}
    console.log(lang_ids)
    const response = await fetch(
          'http://localhost:7000/get-all-routines', 
          {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({'lang_id': lang_ids})
          }
          )
    const received = await response.json();
    routines.value = received
    return true
}

const routines = ref()

onMounted(async () => {
    GetLangs()
    collectRoutines()
})

</script>