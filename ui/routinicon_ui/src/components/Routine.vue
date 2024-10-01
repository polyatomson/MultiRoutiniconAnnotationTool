<template>
    <Toast />
    <ConfirmDialog />
    <Message v-if="erMessage" severity="error">{{ erMessage }}</Message>
    <div v-else>
        <div class="flex flex-row justify-content-center px-3 py-4 gap-3">
            <div class="flex align-content-center">
                <Inplace :closable="true" @close="closeRoutineEdit" class="min-h-full" :active="editRoutine">
                    <template #display>
                         <span class="text-2xl font-bold">{{ currentRoutine.routine }}</span>
                        </template>
                        <template #content>
                            <InputText v-model="currentRoutine.routine"/>
                        </template>
                        <template #closeicon>
                            <i class="pi pi-check"></i>
                        </template>
                    </Inplace>
                </div>
            <!-- <div class="flex flex-grow-1"></div> -->
            <div class="flex align-content-center"><Tag :value="'id ' + currentRoutine.routine_id" rounded severity="info"/></div>
            <div class="flex align-content-center"><Tag :value="currentRoutine.lang" severity="contrast"/></div>
        </div>
        <DataTable :value="currentRoutine.exprs" :pt="{header: {style: 'padding-top: 0.5rem; padding-bottom: 0.5rem; background-color: inherit;'}}">
            <template #header>
                <div class="flex flex-row justify-content-start gap-3">
                    <div class="felx align-content-center text-xl">Expressions</div>
                    <div class="flex flex-grow-1"></div>
                    <Button icon="pi pi-link" severity="secondary" text @click="linkExpressions"/>
                    <Button icon="pi pi-pencil" severity="secondary" text disabled/>
                </div>
            </template>
            <Column field="expr_id" header="ID"></Column>
            <Column field="expr_full" header="FullExpr"></Column>
            <Column field="realization" header="Realization"></Column>
            <Column field="glossing" header="Glossing"></Column>
            <Column field="lemmas" header="Lemmas"></Column>
            <Column field="pos" header="POS"></Column>
        </DataTable>
    <div class="pt-3">
        <DataTable v-show="!editingCxInfo" :value="currentRoutine.cxs" 
        v-model:expanded-rows="expandedCxs" dataKey="cx_id" 
        :pt="{header: {style: 'padding-top: 0.5rem; padding-bottom: 0.5rem; background-color: inherit;'}}"
        >
            <template #header>
                <div class="flex flex-row justify-content-start gap-3">
                    <div class="flex align-items-center text-xl">Constructions</div>
                    <div class="flex flex-grow-1"></div>
                    <Button icon="pi pi-link" severity="secondary" text @click="linkCxs"/>
                    <Button icon="pi pi-pencil" severity="secondary" text @click="editCxInfo"/>
                </div>
            </template>
            <Column field="cx_id" header="ID"></Column>
            <Column field="cx_formula" header="Cx"></Column>
            <Column field="syntactic_type" header="SyntType"></Column>
            <Column field="cx_semantics" header="SemType"></Column>
            <Column expander></Column>
            <template #expansion="{data}">
                <DataTable v-if="data.reductions" :value="data.reductions">
                    <Column field="reduction_id" header="ID"></Column>
                    <Column field="change" header="Change"></Column>
                    <Column field="component" header="Element"></Column>
                    <Column field="sem_role" header="SemRole"></Column>
                </DataTable>
                <DataTable v-if="data.examples" :value="data.examples">
                    <Column field="example_id" header="ID"></Column>
                    <Column field="example" header="Example"></Column>
                    <Column field="translation" header="Translation">
                        <template #body="{data, field}">
                            {{ data[field] || '&mdash;' }}
                        </template>
                    </Column>
                    <Column field="source" header="Source">
                        <template #body="{data, field}">
                            {{ data[field] || '&mdash;' }}
                        </template>
                    </Column>
                    <Column field="dated" header="Year"></Column>
                </DataTable>
            </template>
        </DataTable>
        <DataTable v-show="editingCxInfo" v-model:expanded-rows="expandedCxsEdit" dataKey="cx_id" :value="currentRoutine.cxs" :pt="{header: {style: 'padding-top: 0.5rem; padding-bottom: 0.5rem; background-color: inherit;'}}">
            <template #header>
                <div class="flex flex-row justify-content-start gap-3">
                    <div class="flex align-items-center text-xl">Constructions</div>
                    <div class="flex flex-grow-1"></div>
                    <div class="flex align-items-center gap-3">
                        <Button icon="pi pi-times" severity="danger" rounded outlined @click="editingCxInfo = false;" />
                        <Button icon="pi pi-check" severity="success" rounded outlined @click="saveCxInfoEdits" />
                    </div>
                </div>
            </template>
            <Column field="cx_id" header="ID"/>
            <Column field="cx_formula" header="Formula"/>
            <Column header="Edit" expander headerStyle="width: 3rem"/>
            <template #expansion="slotProps">
                <div class="font-bold py-3">Reductions</div>
                <DataTable :value="reductionsEditing.filter(red => red.cx_id === slotProps.data.cx_id)" 
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
                                <Button icon="pi pi-minus" rounded size="small" severity="danger" @click="deleteReduction(data)" />
                            </template>
                        </Column>
                </DataTable>
                <div class="font-bold py-3">Examples</div>
                <DataTable :value="cxExamplesEditing.filter(cx => cx.cx_id === slotProps.data.cx_id)"
                editMode="cell" @cell-edit-complete="onCellEditComplete($event, slotProps)" @cell-edit-init="onCellEditInit" @cell-edit-cancel="onCellEditCancel"
                dataKey="example_id">
                <template #footer>
                    <div class="flex flex-row justify-content-center">
                        <Button icon="pi pi-plus" rounded @click="addCxExample(slotProps)"/>
                    </div>
                </template>
                <Column header="Example" field="example">
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
                        <Button icon="pi pi-minus" rounded size="small" severity="danger" @click="deleteCxExample(data)" />
                    </template>
                </Column>
                </DataTable>
            </template>
        </DataTable>
    </div>
    <div class="flex align-content-center text-xl font-bold px-3 py-3 text-gray-700">
        <div class="flex align-items-center">Frames</div>
        <div class="flex flex-grow-1"></div>
        <div class="flex align-items-center">
            <Button icon="pi pi-link" text severity="secondary" @click="linkFrames"/>
        </div>
    </div>
    <Accordion :activeIndex="activeFrame" expandIcon="pi pi-plus" collapseIcon="pi pi-minus" lazy>
        <AccordionTab v-for="(frame, i) of currentRoutine.frame_info" :key="frame.frame_id"
        >
            <template #header>
                <div class="flex flex-row flex-wrap gap-4 w-full justify-content-end">
                        <div class="flex align-items-center text-lg">{{frame.routine}}</div>
                        <div class="flex align-items-center">[frame {{frame.frame_id}}]</div>
                        <div class="flex align-items-center"><Tag :value="frame.situation_structure" rounded severity="danger"/></div>
                        <div class="flex align-items-center gap-2"><Tag v-for="p of frame.pragmatics" :value="p" severity="primary"/></div>
                        <div class="flex align-items-center gap-2"><Tag v-for="st of frame.sit_tags" :value="st" severity="warning"/></div>
                        <div class="flex align-items-center gap-2">
                            <i v-if="frame.usage_conditions.length" v-badge.secondary="frame.usage_conditions.length" class="pi pi-id-card" style="font-size: 1.5rem" severity="secondary" />
                        </div>
                        <div class="flex align-items-center" v-if="!editingFrames[frame.frame_id]">
                            <Button icon="pi pi-pencil" text severity="secondary" @click="$event.stopPropagation(); console.log(i); activeFrame = i; editingFrames[frame.frame_id] = true;"/>
                        </div>
                        <div class="flex align-items-center gap-3" v-if="editingFrames[frame.frame_id]">
                            <Button icon="pi pi-times" severity="danger" rounded outlined @click="$event.stopPropagation(); editingFrames[frame.frame_id] = false; getRoutine()" />
                            <Button icon="pi pi-save" severity="success" rounded outlined @click="$event.stopPropagation(); saveFrameInfoEdits(frame)" />
                        </div>
                </div>
            </template>   
            <div class="flex flex-row flex-wrap gap-2 py-2">
                <div class="flex flex-row gap-2">
                    <div class="flex align-items-center text-l font-bold">Situation structure:</div>
                    <div class="flex align-items-center"><Tag severity="danger" :value="frame.situation_structure"/></div>
                </div>
                <div class="flex flex-grow-1"/>
                <div class="flex flex-row gap-2">
                    <div class="flex align-items-center text-l font-bold">SitTags:</div>
                    <div class="flex align-items-center flex-row gap-2"><Tag v-for="tag of frame.sit_tags" severity="warning" :value="tag"/></div>
                </div>
            </div>  
            <div class="flex flex-row flex-wrap gap-6 py-3">
                <div v-if="frame.situations?.trigger" class="flex flex-column">
                    <div class="text-l font-bold py-2">Triggers:</div>
                    <div class="flex flex-row flex-wrap gap-1">
                        <Tag severity="secondary" v-for="ev of frame.situations?.trigger" :value="ev"/>
                    </div>
                </div>
                <div v-if="frame.situations?.action" class="flex flex-column">
                    <div class="text-l font-bold py-2">Actions:</div>
                    <div>
                        <div class="flex flex-row flex-wrap gap-1 py-2">
                        <Tag severity="secondary" v-for="ev of frame.situations?.action" :value="ev"/>
                        </div>
                    </div>
                </div>
                <div v-if="frame.pragmatics" class="flex flex-column">
                    <div class="text-l font-bold py-2">Pragmatics:</div>
                    <div class="flex flex-row flex-wrap gap-1">
                        <Tag severity="primary" v-for="p of frame.pragmatics" :value="p"/>
                    </div>
                </div>
                <div v-if="frame.situations?.effect" class="flex flex-column">
                    <div class="text-l font-bold py-2">Effects:</div>
                    <div class="flex flex-row flex-wrap gap-1">
                        <Tag severity="secondary" v-for="ev of frame.situations?.effect" :value="ev"/>
                    </div>
                </div>
            </div>
            <div v-if="frame.usage_conditions?.length" class="text-l font-bold py-2">Usage conditions:</div>
                        <DataTable :value="frame.usage_conditions" v-if="frame.usage_conditions.length && frame.usage_conditions[0]" class="py-3">
                            <!-- <Column field="condition_id" header="ID"/> -->
                            <Column field="category" header="Category"/>
                            <Column field="condition" header="Condition" :pt="{body: {class: 'flex flex-wrap'}}"/>
                        </DataTable>
            <div v-if="editingFrames[frame.frame_id]">
                <div class="py-2">
                    <div class="text-l font-bold py-2">Definition:</div>
                    <Textarea v-model="frame.definition" autoResize style="width: 100%;"></Textarea>
                </div>
                <div class="py-2">
                    <div class="text-l font-bold py-2">Intonation:</div>
                    <Textarea v-model="frame.intonation" autoResize style="width: 100%;"></Textarea>
                </div>
                <div class="py-2">
                    <div class="text-l font-bold py-2">Comments:</div>
                    <Textarea v-model="frame.comments" autoResize style="width: 100%;"></Textarea>
                </div>
                <div class="font-bold py-3">Examples</div>
                <DataTable :value="frame.examples" editMode="cell" @cell-edit-complete="onExampleEditComplete" dataKey="example_id">
                    <template #footer>
                        <div class="flex flex-row justify-content-center gap-3">
                            <Button icon="pi pi-plus" rounded @click="addExample(frame)"/>
                            <Button icon="pi pi-bolt" rounded severity="secondary" @click="generateExamples(frame.frame_id)"/>
                        </div>
                    </template>
                    <Column field="example" header="Example" body-style="max-width: 35%;" :pt="{body: {class: 'flex flex-wrap'}}">
                        <template #editor="{data, field}">
                            <Textarea autoResize v-model="data[field]" style="width: 100%;"/>
                        </template>
                        <template #body="{data, field}">
                            <div class="flex flex-row flex-wrap">{{ data[field] }}</div>
                        </template>
                    </Column>
                    <Column field="translation" body-style="max-width: 35%;" header="Translation">
                        <template #editor="{data, field}">
                            <Textarea autoResize v-model="data[field]" style="width: 100%;"/>
                        </template>
                        <template #body="{data, field}">
                            <div class="flex flex-row flex-wrap">{{ data[field] }}</div>
                        </template>
                    </Column>
                    <Column field="source" header="Source" body-style="max-width: 10%;">
                        <template #editor="{data, field}">
                            <AutoComplete v-model="data[field]" class="flex flex-wrap" style="width: 100%;" :suggestions="suggestedSources" @complete="findSource" dropdown></AutoComplete>
                        </template>
                    </Column>
                    <Column header="Year" field="dated" body-style="max-width: 10%;">
                    <template #editor="{data, field}">
                        <InputNumber v-model="data[field]" :useGrouping="false" showButtons :min="0" :max="store.curYear" />
                    </template>
                </Column>
                <Column body-style="max-width: 10%">
                    <template #body="{data, index}">
                        <Button icon="pi pi-minus" rounded size="small" severity="danger" @click="deleteEx(frame.examples, index)" />
                    </template>
                </Column>
                </DataTable>
            </div>
            <div v-else>
            <div v-if="frame.definition?.length" class="flex flex-row flex-wrap gap-2">
                <div class="flex align-items-center text-l font-bold py-2">Definition:</div>
                <div class="flex align-items-center">{{ frame.definition }}</div>
            </div>
            <div v-if="frame.intonation?.length" class="flex flex-row flex-wrap gap-2">
                <div class="flex align-items-center text-l font-bold py-2">Intonation:</div>
                <div class="flex align-items-center">{{ frame.intonation }}</div>
            </div>
            <div v-if="frame.comments?.length" class="flex flex-row flex-wrap gap-2">
                <div class="flex align-items-center text-l font-bold py-2">Comments:</div>
                <div class="flex align-items-center">{{ frame.comments }}</div>
            </div>
            <div v-if="frame.examples?.length">
                <div class="text-l font-bold py-2">Examples:</div>
                <!-- <div class="flex flex-column"> -->
                <div class="flex flex-column py-2" v-for="ex of frame.examples">
                    <div class="flex flex-row flex-wrap gap-1">
                        <span class="flex align-items-center font-italic">{{ ex.example}}</span>
                        <Tag v-if="ex.source" :value="ex.source" class="flex align-items-center"/>
                        <Tag v-if="ex.dated" :value="ex.dated" class="flex align-items-center"/>
                    </div>
                    <div v-if="ex.translation?.length">'{{ex.translation }}'</div>
                </div>
                <!-- </div> -->
            </div>
        </div>
        </AccordionTab>
    </Accordion>
    <!-- <Dialog v-model:visible="linkExpressions">
        <pick-expressions curLang="{lang: 'si', lang_id: 57}"/>
    </Dialog> -->
    </div>
    <Dialog v-model:visible="showCorporaExamples" @after-hide="addGeneratedExamples" modal>
<TabView>
<TabPanel v-for="expr in generatedExamples" :header="expr.expr_full">
    <DataTable :value="expr.examples" v-model:selection="pickedExamples">
        <template #header>
            <div class="flex flex-row gap-4 justify-content-end">
                <div class="flex align-items-center"><Button icon="pi pi-refresh" @click="generateNew(expr.expr_full, expr.page_num)"/></div>
                <div class="flex align-items-center"><Tag severity="secondary" :value="expr.corpname"/></div>
                <div class="flex align-items-center"><Tag severity="secondary" :value="expr.page_num"/></div>
                <div class="flex align-items-center"><Tag severity="secondary" :value="expr.fullsize + ' hits'" rounded/></div>
                <div class="flex align-items-center"><Tag severity="secondary" :value="expr.ipm + ' ipm'"/></div>
                <div class="flex align-items-center"><Tag severity="secondary" :value="'CQL: '+expr.query"/></div>
            </div>
        </template>
        <Column selection-mode="multiple"/>
        <Column field="left"/>
        <Column field="kwic"/>
        <Column field="right"/>
        <Column field="source_name"/>
        <Column field="year"/>
    </DataTable>
</TabPanel>    
</TabView>
</Dialog>
</template>

<script setup>
import { onBeforeMount, ref } from 'vue';
import { useRoute } from 'vue-router';
import { store } from '../store'
import { useDialog } from 'primevue/usedialog';
import PickExpressions from './PickExpressions.vue';
import { onMounted } from 'vue';
import PickConstruction from './PickConstruction.vue';
import FramesTable from './FramesTable.vue';
import { useConfirm } from 'primevue/useconfirm';
import { useToast } from 'primevue/usetoast'

const activeFrame = ref(0)

const linkFrames = () => {
    const frameIds = currentRoutine.value.frame_info.map(f => f.frame_id)
    dialog.open(FramesTable, {
        props: {style: 'height: 80%', content: {props: {scrollHeight: '60%'}}},
        data: {frameIds},
        onClose: (opt) => {
            if (!opt.data?.frameIds) {
                console.log('closing without saving', opt)
                return true
            }
            const frameIds = opt.data.frameIds
            console.log(frameIds)
            const unlinking = currentRoutine.value.frame_info.filter(f => !frameIds.includes(f.frame_id))
            if (!unlinking.length) {
                console.log('all kept')
                return SaveNewFrames(frameIds)
            }
            else {
                const unlinkingFilled = unlinking.filter(f => f.examples?.length || f.comments?.length || f.definition || f.intonation)
                if (!unlinkingFilled.length) {
                    return SaveNewFrames(frameIds)
                }
                const unlinkingFilledIds = unlinkingFilled.map(f => f.frame_id)
                confirmation.require({
                    message: 'Are you sure you want to unlink the frames ' + unlinkingFilledIds + '? The related definitions, comments, intonation, and examples will be lost',
                    icon: 'pi pi-exclamation-triangle',
                    rejectClass: 'p-button-sm p-button-outlined',
                    acceptClass: 'p-button-danger p-button-sm p-button-outlined',
                    rejectLabel: 'Do not unlink filled',
                    acceptLabel: 'Unlink all',
                    accept: () => {
                        console.log('unlinking')
                        SaveNewFrames(frameIds)
                    },
                    reject: () => {
                        console.log('withouth unlinking filled')
                        const newAndFilled = [...frameIds, ...unlinkingFilledIds]
                        console.log(newAndFilled)
                        SaveNewFrames(newAndFilled)
                    }
                })
        }
    }
})
}

const saveFrameInfoEdits = async(frame) => {
    if (frame.examples?.filter(e => e.example === null || e.example.trim() === '').length) {
        toast.add({summary: 'Cannot save', detail: "The example field cannot be empty. Delete the empty examples if you don't want them", severity: 'error'})
        return false
    }
    const response = await fetch(
        'http://localhost:7000/change-frame-info',
        { method: 'POST',
            mode: 'cors',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({...frame, routine_id: currentRoutine.value.routine_id})
        }
    )
    const received = await response.json()
}


const editRoutine = ref(false)

const confirmation = useConfirm()
const editingCxInfo = ref(false)
const editingFrames = ref({})
const expandedCxsEdit = ref({})

const reductionsEditing = ref([])
const cxExamplesEditing = ref([])

const frameTags = ref()

const toast = useToast()

const onExampleEditComplete = (event) => {
    let { data, newValue, field } = event;
    data[field] = newValue;
}

const changeRoutine = async() => {
    const response = await fetch(
        'http://localhost:7000/change-routine',
        { method: 'POST',
            mode: 'cors',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({routine_id: currentRoutine.value.routine_id, routine: currentRoutine.value.routine})
        }
    )
    const received = await response.json()
    if (received.error) {
        toast.add({summary: 'Could not save edits', detail: received.error, severity: 'error'})
        editRoutine.value = true
    }
}

const closeRoutineEdit = (event) => {
    if (!currentRoutine.value.routine?.length) {
        console.log('not saving', currentRoutine.value.routine?.length)
        editRoutine.value = true
        return false
    }
    changeRoutine(event)
}

// const editFrames = async() => {
    
//     editingFrames.value[frame.frame_id] = true
// }

const editCxInfo = () => {
    var examplesOld = []
    var reductionsOld = []
    currentRoutine.value.cxs.forEach(cx => {
        if (cx.examples?.length) {
            // console.log(cx.examples)
            cx.examples.forEach(ex => {
                examplesOld.push(
                    {cx_id: cx.cx_id,
                        ...ex
                    }
                )
            })
        }
        if (cx.reductions?.length) {
            // console.log(cx.examples)
            cx.reductions.forEach(r => {
                reductionsOld.push(
                    {cx_id: cx.cx_id,
                        ...r
                    }
                )
            })
        }
    });

        cxExamplesEditing.value = examplesOld
        reductionsEditing.value = reductionsOld
        console.log(examplesOld)
        editingCxInfo.value = true
        expandedCxsEdit.value[currentRoutine.value.cxs[0].cx_id] = true
}

const linkExpressions = () => {
    console.log(currentRoutine.value.exprs)
    store.pickedExpressions = currentRoutine.value.exprs
    dialog.open(PickExpressions, {
        onClose: (opt) => {
            const newExprIds = opt.data?.exprIds
            console.log(newExprIds)
            if (newExprIds?.length) {
                SaveNewExpressions(newExprIds)
            }
        }
})
}

const linkCxs = () => {
    console.log(currentRoutine.value.cxs)
    if (!currentRoutine.value.cxs) {
        currentRoutine.value.cxs = []
    }
    store.selectedCxs = currentRoutine.value.cxs
    dialog.open(PickConstruction, {
        onClose: (opt) => {
            const newCxIds = opt.data?.newCxIds
            if (newCxIds === undefined || newCxIds === null) {
                return true
            }
            console.log(newCxIds)
            // const currentCxIds = currentRoutine.value.cxs.map(cx => cx.cx_id)
            // console.log(currentCxIds)
            const unlinking = currentRoutine.value.cxs.filter(cx => !newCxIds.includes(cx.cx_id))
            if (!unlinking.length) {
                console.log('all kept')
                return SaveNewCxs(newCxIds)
            }
            else {
                const unlinkingFilled = unlinking.filter(cx => cx.examples?.length || cx.reductions?.length)
                if (!unlinkingFilled.length) {
                    return SaveNewCxs(newCxIds)
                }
                const unlinkingFilledIds = unlinkingFilled.map(cx => cx.cx_id)
                confirmation.require({
                    message: 'Are you sure you want to unlink the Cxs ' + unlinkingFilledIds + '? The related reduction and example records will be lost',
                    icon: 'pi pi-exclamation-triangle',
                    rejectClass: 'p-button-sm p-button-outlined',
                    acceptClass: 'p-button-danger p-button-sm p-button-outlined',
                    rejectLabel: 'Do not unlink filled',
                    acceptLabel: 'Unlink all',
                    accept: () => {
                        console.log('withouth unlinking filled')
                        const newAndFilled = newCxIds + unlinkingFilledIds
                        SaveNewCxs(newAndFilled)
                    },
                    reject: () => {
                        console.log('unlinking')
                        SaveNewCxs(newCxIds)
                        
                    }
                })
            }
        }
    })
}

const addReduction = (cx_info) => {
    const newRow = {'cx_id': cx_info.data.cx_id, 'change': null, 'component': null, 'sem_role': null}
    reductionsEditing.value.push(newRow)
}

const deleteReduction = (rowValue) => {
    reductionsEditing.value = reductionsEditing.value.filter(r => r != rowValue)
}

const addCxExample = (cx_info) => {
    const newRow = {'cx_id': cx_info.data.cx_id, 'cx_example': null, 'translation': null, 'source': null, 'dated': 2000}
    cxExamplesEditing.value.push(newRow)
}

const deleteCxExample = (rowValue) => {
    cxExamplesEditing.value = cxExamplesEditing.value.filter(e => e != rowValue)
}

const addExample = (frame) => {
    if (!frame.examples) {frame.examples = []}
    frame.examples.push({example: null, translation: null, source: null, dated: 2000})
}

const deleteEx = (all_exs, index) => {
    // console.log(all_exs, index)
    all_exs.splice(index, 1)
}

const generateNew = async(full_expr, page_num) => {
        await addGeneratedExamples()
        const response = await fetch(
        'http://localhost:7000/generate-examples',
        {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({'exprs': store.userRoutine[0].exprs.filter(e => e.full_expr = full_expr), 'lang_id': store.curLang.lang_id, 'page_num': page_num + 1})
        })
        const received = await response.json()
        if (received.error) {
            return false
        }
        for (let index = 0; index < generatedExamples.value.length; index++) {
            const expression = generatedExamples.value[index];
        
            if (expression.expr_full === full_expr) {
                console.log('assigned new')
                generatedExamples.value[index] = received[0]
            }
            else {
                console.log(expression.expr_full, full_expr)
            }
            
            console.log(generatedExamples.value)
        }
    }

const generateExamples = async(frame_id) => {
    const response = await fetch(
        'http://localhost:7000/generate-examples',
        {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({'exprs': currentRoutine.value.exprs, 'lang_id': currentRoutine.value.lang_id, 'page_num': 1})
        })
    const received = await response.json()
    if (received.error) {
        return false
    }
    generatedExamples.value = received
    showCorporaExamples.value = true
    workingWFrame.value = frame_id
}

const pickedExamples = ref([])
const showCorporaExamples = ref(false)
const workingWFrame = ref()
const generatedExamples = ref()
const addGeneratedExamples = () => {
    const frame_id = workingWFrame.value
    const frame = currentRoutine.value.frame_info.filter(f => f.frame_id === frame_id)[0]
    console.log(frame)
    if (!frame.examples) {frame.examples = []}
    for (const ex of pickedExamples.value) {
        if (!frame.examples.filter(e => e.example === ex.full).length) {
                console.log('adding')
                const newExample = {'example': ex.full, 'source': generatedExamples.value[0].corpname, 'translation': null, 'dated': ex.year}
                frame.examples.push(newExample)
            }
    }
}

const editingReductionsUnfinished = ref([])
const editingCxExamplesUnfinished = ref([])
const onCellEditCancel = (event) => {
    let { data, field } = event;
    if (data.reduction_id) editingReductionsUnfinished.value = editingReductionsUnfinished.value.filter(r => !(r.reduction_id === data.reduction_id && r.field === field))
    else if (data.example_id) editingCxExamplesUnfinished.value.filter(e => !(e.example_id === data.example_id && e.field === field))
}

const onCellEditComplete = (event, cx) => {
    let { data, newValue, field } = event;
    switch (field) {
        case 'change':
            if (newValue !== null && newValue.length > 0) {
                    console.log('cell not empty')
                    data[field] = newValue; 
                    editingReductionsUnfinished.value = editingReductionsUnfinished.value.filter(r => !(r.reduction_id === data.reduction_id && r.field === field))
                }
                else {
                    console.log('cell empty');
                    event.preventDefault();}
                break;
        case 'component':
            if (cx.data.cx_formula.includes(newValue)) {
                console.log('ok')
                data[field] = newValue;
                editingReductionsUnfinished.value = editingReductionsUnfinished.value.filter(r => !(r.reduction_id === data.reduction_id && r.field === field))
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
            editingReductionsUnfinished.value = editingReductionsUnfinished.value.filter(r => !(r.reduction_id === data.reduction_id && r.field === field))
            console.log('saved null', editingReductionsUnfinished.value)
            break;
        case 'cx_example':
            if (newValue !== null && newValue.length > 0) {
                console.log('cell not empty')
                data[field] = newValue; 
                editingCxExamplesUnfinished.value = editingCxExamplesUnfinished.value.filter(e => !(e.example_id === data.example_id && e.field === field))
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
            editingCxExamplesUnfinished.value = editingCxExamplesUnfinished.value.filter(e => !(e.example_id === data.example_id && e.field === field))
            break;
        default: // translation and year
            data[field] = newValue;
            editingCxExamplesUnfinished.value = editingCxExamplesUnfinished.value.filter(e => !(e.example_id === data.example_id && e.field === field))
                break;
            
    }
}

const saveCxInfoEdits = async() => {
    const cx_examples = cxExamplesEditing.value.filter(ex => ex.example?.length)
    const cx_reductions = reductionsEditing.value.filter(r => r.change?.length && r.component?.length)
    const response = await fetch(
        'http://localhost:7000/change-cx-info',
        { method: 'POST',
            mode: 'cors',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({cx_examples, cx_reductions, routine_id: currentRoutine.value.routine_id})
        }
    )
    const received = await response.json()
    if (received.error) {
        console.log(received.error)
        return false
    }
    else {
        await getRoutine()
        editingCxInfo.value = false
    }
}

const SaveNewFrames = async(frameIds) => {
    const response = await fetch(
        'http://localhost:7000/change-frame-refs',
        { method: 'POST',
            mode: 'cors',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({'routine_id': Number(route.params.id), 'frame_ids': frameIds})
        }
    )
    const received = await response.json()
    if (received.n_deleted || received.n_added) {
        await getRoutine()
        return true
    }
}

const SaveNewCxs = async(newCxIds) => {
    const response = await fetch(
        'http://localhost:7000/change-cx-refs',
        { method: 'POST',
            mode: 'cors',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({'routine_id': Number(route.params.id), 'cx_ids': newCxIds})
        }
    )
    const received = await response.json()
    if (received.n_deleted || received.n_added) {
        await getRoutine()
        return true
    }
}

const SaveNewExpressions = async(newExprIds) => {
    const response = await fetch(
        'http://localhost:7000/change-expression-refs',
        { method: 'POST',
            mode: 'cors',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({'routine_id': Number(route.params.id), 'expr_ids': newExprIds})
        }
    )
    const received = await response.json()
    if (received.n_deleted || received.n_added) {
        await getRoutine()
        return true
    }
}

// const openedInDialog = ref()
const dialog = useDialog();


const route = useRoute()
const currentRoutine = ref({})
const erMessage = ref()

const expandedCxs = ref({})

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

const getRoutine = async() => {
    const response = await fetch(
        'http://localhost:7000/get-routine',
        { method: 'POST',
            mode: 'cors',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({'routine_id': Number(route.params.id)})
        }
    )
    const received = await response.json()
    if (received.error) {
        erMessage.value = received.error
        return false
    }
    currentRoutine.value = received

}

onBeforeMount (async() => {
    await getRoutine()
    if (!currentRoutine.value.error)
        {
            store.curLang = {'lang': currentRoutine.value.lang, 'lang_id': currentRoutine.value.lang_id}
            console.log(store.curLang)
        }
})

</script>
