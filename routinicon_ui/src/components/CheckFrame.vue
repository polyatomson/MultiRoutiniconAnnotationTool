<template>
    <Toast />
    <Card :pt="{ 
    header: { class: 'bg-primary border-round-lg' }, 
    title: {class: 'flex justify-content-center'},
    content: { class: 'flex justify-content-center' }, 
    footer: { class: 'flex justify-content-center'} 
    }">
        <template #title>
            Check frame
        </template>
        <template #header>
            <div style="height: 1rem;"></div>
        </template>
        <template #content>
             <DataTable :value="[store.userFrame.fullFrame]" 
             resizableColumns columnResizeMode="fit" showGridlines 
             v-model:expandedRows="expandedRows" dataKey="frame_id">
                <Column expander style="width: 3rem" />
                <Column field="sitStructure" header="Type">
                <template #body="{data, field}">
                    <Tag class="text-base" :value="shortenStructure(data[field])" rounded severity="danger"/>
                </template>
                </Column>
                <Column field="pragmatics" header="Pragmatics">
                    <template #body="{data, field}">
                        <div class="flex flex-row gap-2 flex-wrap">
                            <Tag v-for="t in data[field]" :value="t"/>
                        </div>
                        <i v-if="!data[field].length" class="pi pi-minus"></i>
                    </template>
                </Column>
                <Column field="tags" header="Tags">
                    <template #body="{data, field}">
                        <div class="flex flex-row gap-2 flex-wrap">
                            <Tag v-for="t in data[field]" :value="t"/>
                        </div>
                        <i v-if="!data[field].length" class="pi pi-minus"></i>
                    </template>
                </Column>
                <Column field="examples" header="Examples">
                        <template #body="{data, field}">
                            <div class="flex flex-row gap-2 flex-wrap">
                                <Tag v-for="r in data[field]" style="background-color: var(--surface-000); 
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
                <template #expansion="slotProps">
                    <div class="p-1">
                        <strong>Situation structure</strong>
                        <DataTable :value="[slotProps.data.events]" class="py-3"
                        >
                            <Column v-if="'triggers' in slotProps.data.events && slotProps.data.events.triggers?.length" field="triggers" header="Trigger">
                                <template #body="{data, field}">
                                    <div class="flex flex-row flex-wrap gap-2">    
                                        <Tag v-for="tag of data[field]" :value="tag" severity="secondary"/>
                                    </div>
                                </template>
                            </Column>
                            <Column v-if="'actions' in slotProps.data.events && slotProps.data.events.actions?.length" field="actions" header="Action">
                                <template #body="{data, field}">
                                    <div class="flex flex-row flex-wrap gap-2">    
                                        <Tag v-for="tag of data[field]" :value="tag" severity="secondary"/>
                                    </div>
                                </template>
                            </Column>
                            <Column v-if="'effects' in slotProps.data.events && slotProps.data.events.effects?.length" field="effects" header="Effect">
                                <template #body="{data, field}">
                                    <div class="flex flex-row flex-wrap gap-2">
                                        <Tag v-for="tag of data[field]" :value="tag" severity="secondary"/>
                                    </div>
                                </template>
                            </Column>
                        </DataTable>
                        <div><strong>Usage conditions</strong></div>
                        <DataTable v-if="slotProps.data.conditions.length" :value="slotProps.data.conditions" class="py-3">
                            <Column field="category" header="Category"/>
                            <Column field="condition" header="Condition" :pt="{body: {class: 'flex flex-wrap'}}"/>
                        </DataTable>
                            <div v-else class="flex justify-content-center"><i class="pi pi-minus py-3"></i></div>
                    </div>
                </template>
             </DataTable>
            </template>
        <template #footer>
            <Button v-if="!store.userFrame.editing" label="Save" @click="saveData"/>
        </template>
    </Card>
</template>
<script setup>
import { ref } from 'vue';
import { store } from '../store';
import { useToast } from 'primevue/usetoast';

const toast = useToast();

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

const expandedRows = ref({'new1': true})

const checkUserFrame = () => {
    toast.remove()
    switch (store.userFrame.fullFrame.sitStructure) {
        case 'reaction':
            if (!store.userFrame.fullFrame.events.triggers?.length) {
                toast.add({ severity: 'warn', summary: 'Incomplete data', detail: 'Triggers must be annotated' })
                return false
            }
            else {
                break;
            }
        case 'prompt':
            if (!store.userFrame.fullFrame.events.effects?.length) {
                toast.add({ severity: 'warn', summary: 'Incomplete data', detail: 'Effects must be annotated' })
                return false
            }
            else {
                break;
            }
        case 'reaction + prompt':
            if (!store.userFrame.fullFrame.events.triggers?.length) {
                    toast.add({ severity: 'warn', summary: 'Incomplete data', detail: 'Triggers must be annotated' })
                    return false
                }
            else if (!store.userFrame.fullFrame.events.effects?.length) {
                toast.add({ severity: 'warn', summary: 'Incomplete data', detail: 'Effects must be annotated' })
                return false
            }
            else {
                break;
            }
        case 'accompaniment':
            // if (!store.userFrame.fullFrame.events.triggers?.length) {
            //         toast.add({ severity: 'warn', summary: 'Incomplete data', detail: 'Triggers must be annotated' })
            //         return false
            //     }
            // if (!store.userFrame.fullFrame.events.effects?.length) {
            //     toast.add({ severity: 'warn', summary: 'Incomplete data', detail: 'Effects must be annotated' })
            //     return false
            // }
            if (!store.userFrame.fullFrame.events.actions?.length) {
                toast.add({ severity: 'warn', summary: 'Incomplete data', detail: 'Actions must be annotated' })
                return false
            }
            else {
                break;
            }
    }
    if (!store.userFrame.fullFrame.pragmatics.length) {
        toast.add({ severity: 'warn', summary: 'Incomplete data', detail: 'Pragmatics must be annotated' })
                return false
    }
    if (!store.userFrame.fullFrame.tags.length) {
        toast.add({ severity: 'warn', summary: 'Incomplete data', detail: 'Situation tags must be provided' })
                return false
    }
    // if (!store.userFrame.fullFrame.examples.length) {
    //     toast.add({ severity: 'warn', summary: 'Incomplete data', detail: 'At least one example must be provided' })
    //             return false
    // }
    return true
}

async function sendFrame(data) {
    const response = await fetch(
          'http://localhost:7000/submit-frame', 
          {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
          }
          )
    const received = await response.json();
    console.log(received)
    if (received.added === false) {
        toast.add({severity: 'danger', summary: 'The frame already exists', detail: 'This combination of tags already exists in the db'})
        store.newFrameSubmittedId = received.frame_id
        return false
    }
    store.newFrameSubmittedId = received.frame_id
    return received
}

const saveData = () => {
    const allGood = checkUserFrame()
    console.log('AllGood', allGood)
    if (allGood) {
        console.log('sending to backend')
        sendFrame(store.userFrame.fullFrame)
        toast.add({severity: 'success', summary: 'Success', detail: 'The frame was saved into the db'})
        store.userFrame.step = 1
    }
    else {
        console.log('did not send')
    }
}

</script>
<style></style>