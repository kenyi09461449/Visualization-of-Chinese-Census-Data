import {createRouter, createWebHashHistory} from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'default',
        component: () => import('@/views/Login.vue')
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('@/views/Login.vue')
    },
    {
        path: '/register',
        name: 'register',
        component: () => import('@/views/Register.vue')
    },
    {
        path: '/home',
        name: 'home',
        component: () => import('@/views/Home.vue')
    },
    {
        path: '/index',
        name: 'index',
        component: () => import('@/views/Index.vue')
    },
    {
        path: '/collection',
        name: 'collection',
        component: () => import('@/views/Collection.vue')
    },
    {
        path: '/dashboard',
        name: 'DashBoard',
        component: () => import('@/views/admin/DashBoard.vue'),
        children: [
            // admin start
            {
                path: '',
                name: 'Default',
                component: () => import('@/views/admin/User.vue')
            },
            {
                path: '/user',
                name: 'UserList',
                component: () => import('@/views/admin/User.vue')
            },
            {
                path: '/age',
                name: 'AgeList',
                component: () => import('@/views/admin/Age.vue')
            },
            {
                path: '/birth',
                name: 'BirthList',
                component: () => import('@/views/admin/Birth.vue')
            },
            {
                path: '/gdp',
                name: 'GdpList',
                component: () => import('@/views/admin/Gdp.vue')
            },
            {
                path: '/people',
                name: 'PeopleList',
                component: () => import('@/views/admin/People.vue')
            },
            {
                path: '/province',
                name: 'ProvinceList',
                component: () => import('@/views/admin/Province.vue')
            },
            // admin end
        ]
    }
]

const router = createRouter({
    history: createWebHashHistory(process.env.BASE_URL),
    routes
})

export default router
