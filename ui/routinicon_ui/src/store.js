import { reactive } from 'vue'

export const store = reactive({
  curYear: null,
  expressions: null,
  curLang: {"lang":"ru","lang_id":58},
  newRoutine: null,
  selectedFrames: [],
  pickedExpressions: [],
  userRoutine: [],
  selectedCxs: [],
  cxReductions: {},
  cxExamples: {},
  routineSubmitted: false,
  exampleSources: [],
  allConstructions: [],
  userExpression: {
    lang: null,
    expr: null,
    previousExpr: null,
    units: {},
    unitsChanged: true,
    glossed: [],
    step: null,
    previousStep: null,
    singleLineResult: null,
    submitted: null
  },
  newExrSubmittedId: null,
  newFrameSubmittedId: null,
  unitsSuggestions: {},
  langIds: {},
  lemmas: {},
  poses: {},
  glosses: null,
  userFrame: {
    step: null,
    previousStep: null,
    reusing: false,
    editing: false,
    fullFrame: {
      events: {},
      tags: [],
      pragmatics: [],
      conditions: [],
      sitStructure: null,
      examples: [],
      frame_id: 'new1'
    }
    },
  frameAnnotation: {}
})