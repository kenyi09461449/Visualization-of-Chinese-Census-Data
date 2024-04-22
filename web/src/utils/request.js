import axios from 'axios'
import router from '../router'
import {ElMessage} from 'element-plus'

// create an axios instance
const service = axios.create({
    baseURL: '/api', // url = base url + request url
    timeout: 60000, // request timeout
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        // 'token': sessionStorage.getItem('token'),
        'X-Requested-With': 'XMLHttpRequest',
    },
})

// add request interceptor
service.interceptors.request.use(
    function (config) {
        // var token = localStorage.getItem('token');
        // // console.log(token)
        // if (token) {
        //     config.headers.token = token
        // }
        return config
    },
    function (error) {
        return Promise.reject(error)
    }
)

// add response interceptor
service.interceptors.response.use(
    function (response) {
        // console.log(response)
        const res = response.data

        if (res.code === 401) {
            // 401
            ElMessage.error(res.msg)
            router.push({path: '/'})
        } else {
            return response.data
        }
    },
    function (error) {
        console.log(error)
        if (error.response.status === 401) {
            ElMessage.error("Please login first!")
            router.push({path: '/'})
        }
        return Promise.reject(error)
    }
)
export default service