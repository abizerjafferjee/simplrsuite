import Vue from 'vue'
import VueRouter from 'vue-router'
import ProductForm from '@/components/ProductForm.vue'
import ProductTable from '@/components/ProductTable'
import MailListForm from '@/components/MailListForm'
import ProcurementForm from '@/components/ProcurementForm'
import Dashboard from '@/components/Dashboard'

Vue.use(VueRouter)

const routes = [
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard
    },
    {
        path: '/add-products',
        name: 'ProductForm',
        component: ProductForm
    },
    {
        path: '/view-products',
        name: 'ProductTable',
        component: ProductTable
    },
    {
        path: '/add-contact',
        name: 'MailListForm',
        component: MailListForm
    },
    {
        path: '/add-inventory',
        name: 'ProcurementForm',
        component: ProcurementForm
    },
];

export default new VueRouter({
    routes
});

