import {createStore} from 'vuex'

export default createStore({
    state: {
        app: {
            "name": "PopulationDataAnalyze",
            "version": "1.0.0",
            "host": "http://" + window.location.hostname + ":5000",
        },
        user: JSON.parse(sessionStorage.getItem("user")) || {},
        token: sessionStorage.getItem("token") || "",
        tabName: 'HOME'
    },
    mutations: {
        SET_TOKEN: (state, token) => {
            state.token = token
            sessionStorage.setItem("token", token)
        },
        SET_USERINFO: (state, user) => {
            state.user = user
            sessionStorage.setItem("user", JSON.stringify(user))
        },
        REMOVE_INFO: (state) => {
            sessionStorage.setItem("token", '')
            sessionStorage.removeItem("user")
            state.user = {}
        }
    },
    getters: {
        getUser: state => {
            return state.user
        },
        getHost: state => {
            return state.app.host
        }
    },
    actions: {},
    modules: {}
})
