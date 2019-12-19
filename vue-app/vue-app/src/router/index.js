import Vue from 'vue'
import VueRouter from 'vue-router'
import ProductForm from '@/components/ProductForm.vue'
import ProductView from '@/components/ProductView'
import ProductDetailView from '@/components/ProductDetailView'
import MailListForm from '@/components/MailListForm'
import InvoiceForm from '@/components/InvoiceForm'
import InvoiceView from '@/components/InvoiceView'
import SupplierForm from '@/components/SupplierForm'
import SupplierView from '@/components/SupplierView'
import Dashboard from '@/components/Dashboard'
import OutstandingView from '@/components/OutstandingView'
import PaymentsView from '@/components/PaymentsView'
import PaymentsForm from '@/components/PaymentsForm'
import SignUpForm from '@/components/SignUpForm'
import SignInForm from '@/components/SignInForm'
import CategoryView from '@/components/CategoryView'

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
        path: '/outstanding',
        name: 'OutstandingView',
        component: OutstandingView
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
        path: '/categories',
        name: 'CategoryView',
        component: CategoryView
    },
    {
        path: '/add-contact',
        name: 'MailListForm',
        component: MailListForm
    },
    {
        path: '/invoices',
        name: 'InvoiceView',
        component: InvoiceView
    },
    {
        path: '/add-invoice',
        name: 'InvoiceForm',
        component: InvoiceForm
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
];

export default new VueRouter({
    routes
});

