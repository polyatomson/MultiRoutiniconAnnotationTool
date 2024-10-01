import { createApp } from 'vue'
import PrimeVue from 'primevue/config';
import '/node_modules/primeflex/primeflex.css'
import 'primevue/resources/themes/lara-light-green/theme.css'
import 'primeicons/primeicons.css'

import ScrollPanel from 'primevue/scrollpanel';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
// import ColumnGroup from 'primevue/columngroup';   // optional
import Row from 'primevue/row';                   // optional
import InputText from 'primevue/inputtext';                   // optional
import Menubar from 'primevue/menubar';
import MultiSelect from 'primevue/multiselect';
import Tag from 'primevue/tag';
import Toast from 'primevue/toast';
import ToastService from 'primevue/toastservice';
import Stepper from 'primevue/stepper';
import StepperPanel from 'primevue/stepperpanel';
import RadioButton from 'primevue/radiobutton';
import Textarea from 'primevue/textarea';
import AccordionTab from 'primevue/accordiontab';
import Accordion from 'primevue/accordion';

import App from './App.vue';
// import GlossesTable from './components/GlossesTable.vue';
// import NewExpression from './components/NewExpression.vue';
import EnterExpression from './components/EnterExpression.vue';
import SplitExpression from './components/SplitExpression.vue';
import AssignGlosses from './components/AssignGlosses.vue';
import CheckExpression from './components/CheckExpression.vue';
import SituationStructure from './components/SituationStructure.vue';
import Conditions from './components/Conditions.vue';
import SituationTags from './components/SituationTags.vue';
import RoutineExample from './components/RoutineExample.vue';
import CheckFrame from './components/CheckFrame.vue';
import NewExpression from './components/NewExpression.vue';
import GlossingExamples from './components/GlossingExamples.vue'
import PickExpressions from './components/PickExpressions.vue'
// import Example from './components/Example.vue';

import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import Badge from 'primevue/badge';
import Card from 'primevue/card';
import AutoComplete from 'primevue/autocomplete';
import InputGroup from 'primevue/inputgroup';
import SelectButton from 'primevue/selectbutton';
import BlockUI from 'primevue/blockui';
import ContextMenu from 'primevue/contextmenu';
import Message from 'primevue/message';
// import OverlayPanel from 'primevue/overlaypanel';
import DynamicDialog from 'primevue/dynamicdialog';
import DialogService from 'primevue/dialogservice';
import Dialog from 'primevue/dialog';
import FloatLabel from 'primevue/floatlabel';
import InputGroupAddon from 'primevue/inputgroupaddon'
import InputSwitch from 'primevue/inputswitch';
import FramesTable from './components/FramesTable.vue';
import NewFrame from './components/NewFrame.vue';
import CheckRoutine from './components/CheckRoutine.vue';
import Chart from 'primevue/chart';
import PickConstruction from './components/PickConstruction.vue';
import InputNumber from 'primevue/inputnumber';
import ConfirmPopup from 'primevue/confirmpopup';
// import NewExpression from './components/NewExpression.vue';
import ConfirmationService from 'primevue/confirmationservice';
import Inplace from 'primevue/inplace';
import BadgeDirective from 'primevue/badgedirective';
import EditFrame from './components/EditFrame.vue';
import router from './router.js'
import TabPanel from 'primevue/tabpanel';
import TabView from 'primevue/tabview';
import ConfirmDialog from 'primevue/confirmdialog';
import SplitButton from 'primevue/splitbutton';
import Checkbox from 'primevue/checkbox';
import CascadeSelect from 'primevue/cascadeselect'
import Chips from 'primevue/chips';
import Chip from 'primevue/chip';

const app = createApp(App);
app.use(PrimeVue);
app.use(ToastService);
app.use(ConfirmationService);
app.use(router)
app.use(DialogService)
app.directive('badge', BadgeDirective)
// app.component('gloss-table', GlossesTable);
// app.component('new-expression', NewExpression);
app.component('enter-expression', EnterExpression);
app.component('split-expression', SplitExpression);
app.component('assign-glosses', AssignGlosses);
app.component('check-expression', CheckExpression);
app.component('pick-constructions', PickConstruction)
app.component('glossing-examples', GlossingExamples);
app.component('pick-expressions', PickExpressions);
app.component('SplitButton', SplitButton)
app.component('situation-structure', SituationStructure)
app.component('conditions', Conditions)
app.component('situation-tags', SituationTags)
app.component('routine-example', RoutineExample)
app.component('check-frame', CheckFrame)
app.component('check-routine', CheckRoutine)
app.component('edit-frame', EditFrame)
app.component('DataTable', DataTable);
app.component('Column', Column);
app.component('Row', Row);
app.component('Button', Button);
app.component('InputText', InputText);
app.component('Dropdown', Dropdown);
app.component('Menubar', Menubar);
app.component('Badge', Badge);
app.component('Card', Card);
app.component('AutoComplete', AutoComplete);
app.component('InputGroup', InputGroup);
app.component('SelectButton', SelectButton);
app.component('ScrollPanel', ScrollPanel);
app.component('BlockUI', BlockUI)
app.component('ContextMenu', ContextMenu)
app.component('MultiSelect', MultiSelect)
app.component('Tag', Tag)
app.component('Message', Message)
app.component('Toast', Toast)
app.component('Dialog', Dialog)
app.component('FloatLabel', FloatLabel)
app.component('InputGroupAddon', InputGroupAddon)
app.component('InputSwitch', InputSwitch)
app.component('Stepper', Stepper)
app.component('StepperPanel', StepperPanel)
app.component('new-expression', NewExpression)
app.component('new-frame', NewFrame)
app.component('frames-table', FramesTable)
app.component('RadioButton', RadioButton)
app.component('Textarea', Textarea)
app.component('Chart', Chart)
app.component('InputNumber', InputNumber)
app.component('ConfirmPopup', ConfirmPopup)
app.component('TabView', TabView)
app.component('TabPanel', TabPanel)
app.component('Accordion', Accordion)
app.component('AccordionTab', AccordionTab)
app.component('Inplace', Inplace)
app.component('DynamicDialog', DynamicDialog)
app.component('ConfirmDialog', ConfirmDialog)
app.component('Checkbox', Checkbox)
app.component('CascadeSelect', CascadeSelect)
app.component('Chips', Chips)
app.component('Chip', Chip)
app.mount('#app');