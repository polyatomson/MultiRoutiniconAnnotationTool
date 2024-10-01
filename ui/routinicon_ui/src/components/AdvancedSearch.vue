<template>
    <div class="flex justify-content-center py-1">
        <div class="flex flex-column py-6 gap-3" style="width: 70%;">
            <div class="text-large font-bold">Pragmatics</div>
            <div class="flex flex-row">
                <Dropdown v-model="pragmaticsLogics" :options="logics" dropdown-icon="None" :pt="{trigger: {style: 'width: 0%;'}, input: {class: 'surface-200'}}">
                    <template #value="slotProps">
                        <!-- {{ slotProps }} -->
                        <i :class="slotProps.value.icon"/>
                    </template>
                    <template #option="{ option }">
                        <i :class=option.icon></i>
                    </template>
                </Dropdown>
                <MultiSelect filter :options="pragmaticsTags" display="chip" :max-selected-labels="3" placeholder="Select tags" optionValue="pragmatics_id" @change="console.log($event)" optionLabel="pragmatics" v-model="pragmaticTagsPicked" class="w-full"/>
            </div>
            <div class="text-large font-bold">SitTags</div>
            <div class="flex flex-row">
                <Dropdown v-model="stLogics" :options="logics" dropdown-icon="None" :pt="{trigger: {style: 'width: 0%;'}, input: {class: 'surface-200'}}">
                    <template #value="slotProps">
                        <!-- {{ slotProps }} -->
                        <i :class="slotProps.value.icon"/>
                    </template>
                    <template #option="{ option }">
                        <i :class=option.icon></i>
                    </template>
                </Dropdown>
                <MultiSelect filter :options="sitTags" display="chip" :max-selected-labels="5" placeholder="Select tags" optionValue="sit_tag_id" optionLabel="st" v-model="sitTagsPicked" class="w-full"/>
            </div>
            <div class="text-large font-bold">Events</div>
            <div class="flex flex-row">
                <Dropdown v-model="evLogics" :options="logics" dropdown-icon="None" :pt="{trigger: {style: 'width: 0%;'}, input: {class: 'surface-200'}}">
                    <template #value="slotProps">
                        <!-- {{ slotProps }} -->
                        <i :class="slotProps.value.icon"/>
                    </template>
                    <template #option="{ option }">
                        <i :class=option.icon></i>
                    </template>
                </Dropdown>
                <CascadeSelect filter :options="events" display="chip" @change="$event.stopPropagation; singleEventPicked = null; if (!eventsPicked.filter(e => e.event_id === $event.value.event_id && e.stage === $event.value.stage).length) {eventsPicked = [...eventsPicked, $event.value]};" :max-selected-labels="5" placeholder="Select tags" optionLabel="event" optionGroupLabel="stage" :optionGroupChildren="['event_tags']" v-model="singleEventPicked" class="w-full" selectOnFocus :pt="{label: {class: 'py-0 flex align-items-center'}}">
                    <template #value>
                        <div class="flex flex-row gap-2">
                            <Tag v-for="e in eventsPicked" rounded class="font-normal text-base surface-200 text-color" style="height: 2rem;">
                                <template #default>
                                    <div class="flex flex-row gap-2 align-items-center">
                                        <div>{{ e.stage + ': ' + e.event }}</div>
                                        <i class="pi pi-times-circle" @click="eventsPicked.splice(eventsPicked.indexOf(e), 1);"></i>
                                    </div>
                                </template>
                            </Tag>
                        </div>
                    </template>    
                </CascadeSelect>
            </div>
        </div>
    </div>
<div class="flex flex-column py-6">
    <div v-for="r in routines" class="flex justify-content-center">
        <RouterLink :to="{name: 'routine', params: {id: r.routine_id}}" class="appearance-none">
        <Button severity="secondary" text elevated>
            <template #default>
            <div class="flex flex-row gap-2">
            <div>{{r.routine}}</div>
            <Tag :value="r.lang" />
            </div>
            </template>
        </Button>
        </RouterLink>
    </div>
</div>
</template>
<script setup>
import { onMounted, ref } from 'vue';
import SituationTags from './SituationTags.vue';
const pragmaticTagsPicked = ref([])
const pragmaticsLogics = ref({icon: "pi pi-chevron-up", value: "and"})
const pragmaticsTags = ref([{pragmatics: 'smth', pragmatics_id: 1}, {pragmatics: 'smth else', pragmatics_id: 2}])
const sitTagsPicked = ref([])
const sitTags = ref([{st: 'smth', sit_tag_id: 1}, {st: 'smth else', sit_tag_id: 2}])
const stLogics = ref({icon: "pi pi-chevron-up", value: "and"})
const logics = ref([{icon: "pi pi-chevron-up", value: "and"}, {icon: "pi pi-chevron-down", value: "or"}])
const sitStructurePicked = ref()
const evLogics = ref({icon: "pi pi-chevron-up", value: "and"})
const singleEventPicked = ref()
const eventsPicked = ref([])
const events = ref([
    {
        stage: 'effect',
        event_tags: [
            {
                event: 'smth',
                event_id: 1,
                stage: 'effect'
            },
            {
                event: 'smth else',
                event_id: 2,
                stage: 'effect'
            }
        ]
    },
    {
        stage: 'action',
        event_tags: [
            {
                event: 'smth',
                event_id: 1,
                stage: 'action'
            },
            {
                event: 'smth else',
                event_id: 2,
                stage: 'action'
            }
        ]
    },
    {
        stage: 'effect',
        event_tags: [
            {
                event: 'smth',
                event_id: 1,
                stage: 'effect'
            },
            {
                event: 'smth else',
                event_id: 2,
                stage: 'effect'
            }
        ]
    }
])

const routines = ref()
const getFullRoutineList = async() => {
    const response = await fetch(
            'http://localhost:7000/get-routines-simple', 
            {
                mode: 'cors',
                method: 'GET',
                headers: {
                "Content-Type": "application/json"
                }
            })
    const received = await response.json()
    routines.value = received
    }
onMounted(() => {
    getFullRoutineList()}
)
</script>