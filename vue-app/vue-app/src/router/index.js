import Vue from 'vue'
import VueRouter from 'vue-router'
import ProductForm from '@/components/ProductForm.vue'
import ProductView from '@/components/ProductView'
import MailListForm from '@/components/MailListForm'
import ProcurementForm from '@/components/ProcurementForm'
import SupplierForm from '@/components/SupplierForm'
import SupplierView from '@/components/SupplierView'
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
        path: '/products',
        name: 'ProductView',
        component: ProductView
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
    {
        path: '/suppliers',
        name: 'SupplierView',
        component: SupplierView
    },
    {
        path: '/add-supplier',
        name: 'SupplierForm',
        component: SupplierForm
    },
];

export default new VueRouter({
    routes
});

