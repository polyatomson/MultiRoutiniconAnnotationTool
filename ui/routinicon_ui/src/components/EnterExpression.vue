<template>
<BlockUI :blocked="props.invalidate" :pt="{ mask: {class: 'bg-white opacity-20'} }">
<Card :pt="{ 
    header: { class: 'bg-primary border-round-lg' }, 
    title: {class: 'flex justify-content-center'},
    content: { class: 'flex flex-column row-gap-1' }, 
    footer: { class: 'pd-card-footer'} 
    }">
    <template #header>
        <div style="height: 1rem;"></div>
        <!-- <img alt="user header" src="../assets/random_header.png" /> -->
    </template>
    <template #title>Step #1</template>
    <template #content>
        <!-- <div class="flex justify-content-center"> -->
            <form method="POST" @submit="submitForm">
                <div class="flex justify-content-center">
                    <SelectButton v-model="store.curLang" :options="langs" optionLabel="lang_id"
                    aria-labelledby="basic" inputId="user_lang"
                    class="pb-3"
                    :allowEmpty = false :disabled="props.predefinedLanguage">
                <template #option="SlotProps">
                <div>{{ SlotProps.option.lang }}</div>
                </template>    
                </SelectButton>
                </div>
                
                <InputGroup>
                
                    <span class="p-float-label">
                        <AutoComplete v-model="selectedExpression" 
                        :suggestions="filteredExpressions" 
                        @complete="search"
                        :class="{'p-invalid': isInvalid(selectedExpression)}"
                        inputId = "new_expression"
                        />
                        <label for="new_expression">{{ invalidMessage }}</label>
                    </span>
                    <Button type="submit" icon="pi pi-check" severity="success" />
                </InputGroup>
            </form>
    </template>
    <template #footer>
    </template>
</Card>
</BlockUI>

</template>
<script setup>
import { watch, defineAsyncComponent, initCustomFormatter, onMounted } from 'vue';
import { store } from '../store.js'
import { ref } from 'vue'


const props = defineProps(["invalidate", "predefinedLanguage"])
// console.log('prop', props.invalidate, typeof(props.invalidate))
// console.log('prop', props.placeholderText, typeof(props.placeholderText))

// async function ChangeLanguage(event) {
//     console.log('event',event)
//     store.curLang = event.value
//     console.log(store.curLang)
//     await getExpressionsLanguage()
// }

watch (() => store.curLang, async(newLang) => {
    console.log('watcher', newLang)
    await getExpressionsLanguage()
})

async function getExpressionsLanguage() {
    
    if (store.userExpression.step > 1) {
        return false
    }
    
    else if (store.expressions != null && store.curLang === store.userExpression.lang) {
        console.log("reusing the expressions")
        return false
    }

    else {
    const lang = store.curLang.lang
    console.log('load expressions', lang)
    store.userExpression.lang = lang
    const lang_id = store.langIds.filter(item => item.lang === lang)[0].lang_id
    const lang_id_str = JSON.stringify({"lang_id": lang_id})
    console.log('lang_id', lang_id_str)
    const response = await fetch(
          'http://localhost:7000/expressions', 
          {
            mode: 'cors',
            method: 'POST',
            headers: {
              "Content-Type": "application/json"
            },
            body: lang_id_str,
          })
    const received = await response.json();
    // console.log(received)
    store.expressions = received.expressions
        }
}


const invalidMessage = ref()

function isInvalid (enteredInput) {
    if (typeof(enteredInput) == 'undefined' || enteredInput == '') {
            invalidMessage.value = 'Enter the expression'
            return false
    }
    else if (store.expressions.includes(enteredInput)) {
        // console.log("here")
        invalidMessage.value = 'Already exists'
        return true
    }
    else {
        invalidMessage.value = 'Looks valid'
    }
}


const langs = ref()
// const langs = ref([
//     {'lang':'si', 'lang_id':55}, 
//     {'lang':'ru', 'lang_id':56}  
// ])

// const default_lang_value = ref()


    const submitForm = (event) => {
    event.preventDefault()
    const submittedExpression = event.target.elements.new_expression.value
    console.log('submittedExpression', submittedExpression)
    if (!isInvalid(submittedExpression)) {
        // console.log('valid input', submittedExpression)
        if (store.userExpression.expr != null) {
            store.userExpression.previousExpr = store.userExpression.expr
        }
        store.userExpression.expr = submittedExpression
        console.log('expr in store', store.userExpression.expr)
        store.userExpression.step = 2
    }
    else {
        console.log('invalid')
    }
}

const selectedExpression = ref();

function inputDefault() {
        langs.value = store.langIds
}

const filteredExpressions = ref();

function isSimilar (givenData, searchInput) {
    const regexstr = "(^| )"+searchInput.toLowerCase()
    const regex = new RegExp(regexstr)
    // console.log(regex.test(givenData));
    return regex.test(givenData)
}

const search = (event) => {
    setTimeout(() => {
        // console.log(store.expressions)
        // console.log(event.query)
        if (!event.query.trim().length) {
            filteredExpressions.value = store.expressions;
        } else {
            filteredExpressions.value = store.expressions.filter((expr) => {
                return isSimilar(expr, event.query.toLowerCase());
            });
        }
    }, 250);}


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
    langs.value = received
    if (store.curLang === null) {
        console.log('no curLang')
        store.curLang = received[0]
    }
    else {
        // default_lang_value.value = store.curLang
        console.log(store.curLang)
    }
    console.log('langs', store.langIds)
    // console.log('lang', store.curLang.value)
}


 onMounted(async () => {
        if (!store.langIds.length) {
        await GetLangs()}
        inputDefault()
        console.log('languages', langs.value)
        console.log('curlang', store.curLang)
        await getExpressionsLanguage()
})
</script>

<style>

</style>