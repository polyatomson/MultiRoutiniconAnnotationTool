import { createMemoryHistory, createRouter, createWebHistory } from 'vue-router'

import Home from './components/Home.vue'
import GlossesTable from './components/GlossesTable.vue';
import NewExpression from './components/NewExpression.vue';
import NewFrame from './components/NewFrame.vue';
import NewRoutine from './components/NewRoutine.vue'
import FramesTable from './components/FramesTable.vue'
import RoutinesTable from './components/RoutinesTable.vue'
import CxsTable from './components/CxsTable.vue'
import Routine from './components/Routine.vue'
// import PickExpressions from './components/PickExpressions.vue';
import AdvancedSearch from './components/AdvancedSearch.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/glosses', component: GlossesTable },
  { path: '/new-expression', component: NewExpression },
  { path: '/new-frame', component: NewFrame },
  { path: '/new-routine', component: NewRoutine },
  { path: '/all-frames', component: FramesTable },
  { path: '/all-routines', component: RoutinesTable },
  { path: '/all-cxs', component: CxsTable },
  { path: '/routine/:id', name: 'routine', component: Routine },
  { path: '/search', component: AdvancedSearch }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router