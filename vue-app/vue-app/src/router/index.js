import Vue from 'vue'
import VueRouter from 'vue-router'
import ProductForm from '@/components/ProductForm.vue'
import ProductView from '@/components/ProductView'
import ProductDetailView from '@/components/ProductDetailView'
import MailListForm from '@/components/MailListForm'
import ProcurementForm from '@/components/ProcurementForm'
import ProcurementView from '@/components/ProcurementView'
import SupplierForm from '@/components/SupplierForm'
import SupplierView from '@/components/SupplierView'
import SupplierDetailView from '@/components/SupplierDetailView'
import Dashboard from '@/components/Dashboard'
import PaymentsView from '@/components/PaymentsView'
import PaymentsForm from '@/components/PaymentsForm'
import SignUpForm from '@/components/SignUpForm'
import SignInForm from '@/components/SignInForm'

Vue.use(VueRouter)

const routes = [
    {
        path: '/signin',
        name: 'SignIn',
        component: SignInForm
    },
    {
        path: '/signup',
        name: 'SignUp',
        component: SignUpForm
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard
    },
    {
        path: '/payments',
        name: 'PaymentsView',
        component: PaymentsView
    },
    {
        path: '/record-payment',
        name: 'PaymentsForm',
        component: PaymentsForm
    },
    {
        path: '/add-product',
        name: 'ProductForm',
        component: ProductForm
    },
    {
        path: '/products',
        name: 'ProductView',
        component: ProductView
    },
    {
        path: '/product-detail',
        name: 'ProductDetailView',
        component: ProductDetailView
    },
    {
        path: '/add-contact',
        name: 'MailListForm',
        component: MailListForm
    },
    {
        path: '/inventory',
        name: 'ProcurementView',
        component: ProcurementView
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
        component: SupplierForm,
        props: true
    },
    {
        path: '/supplier-detail',
        name: 'SupplierDetailView',
        component: SupplierDetailView
    },
];

export default new VueRouter({
    routes
});

