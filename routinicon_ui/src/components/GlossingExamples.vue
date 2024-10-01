<template>
    <div v-if="examples && langStats">
        <div class="flex flex-row gap-1">
            <div class="flex align-items-center">N uses:</div>
            <Tag rounded class="flex" :value="nExamples"/>
        </div>
    <div class="flex flex-row justify-content-center pb-3">
        <Chart type="pie" :data="{datasets: [{data: langStats}], labels: langLabels}" style="width: 30%;"/>
    </div>
    <DataTable :value="examples" scrollable scrollHeight="28rem">
        <Column field="unit_id" header="ID"></Column>
        <Column field="lang" header="Lang"></Column>
        <Column field="unit" header="Unit" :pt="{bodyCell: {class: 'font-italic'}}"></Column>
        <Column field="glossing" header="Glossing">
        <template #body="{ data, field }">
            <table>
                <tr>
                    <template v-for="(morph, index) in data[field].morphs">
                        <template v-if="index > 0"><td>-</td></template>
                        <td class="font-italic">{{ morph }}</td>
                    </template>
                </tr>
                <tr>
                    <template v-for="(gloss, index) in data[field].glosses">
                        <template v-if="index > 0"><td>-</td></template>
                        <td :class="{'font-bold': (gloss.includes(props.gloss))}">{{ gloss }}</td>
                    </template>
                </tr>
            </table>
        </template>
        </Column>
    </DataTable>
</div>
<div v-else>Not used in any glossing yet</div>
</template>
<script setup>
// import { DefineProps } from 'vue';
import { onMounted, ref } from 'vue';

const props = defineProps(["gloss_id", "gloss"])
const examples = ref()
const langLabels = ref([])
const langStats = ref([])

const nExamples = ref(0)

const getExamples = async() => {
    const gl_id = props.gloss_id
    const response = await fetch('http://localhost:7000/glossing-examples',
        {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({'gloss_id': gl_id})
        })
    const recieved = await response.json()
    examples.value = recieved.glossing_examples
    langLabels.value = recieved.labels
    langStats.value = recieved.data
    if (langStats.value)
    {nExamples.value = recieved.data.reduce((partialSum, a) => partialSum + a, 0)}

}

onMounted(async() => {
    getExamples()
})

</script>