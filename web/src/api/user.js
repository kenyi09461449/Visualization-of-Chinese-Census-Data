import request from '@/utils/request'

export function userLogin(data) {
    return request({
        url: '/login',
        method: 'post',
        data: data,
    })
}

export function userRegister(data) {
    return request({
        url: '/register',
        method: 'post',
        data: data,
    })
}

export function userAdd(data) {
    return request({
        url: '/user',
        method: 'post',
        data
    })
}

export function userDelete(ids) {
    return request({
        url: '/user',
        method: 'delete',
        params: {
            id: ids
        }
    })
}

export function userUpdate(data) {
    return request({
        url: '/user',
        method: 'put',
        data
    })
}

export function userList(params) {
    return request({
        url: '/user',
        method: 'get',
        params
    })
}

export function userStarList(data) {
    return request({
        url: '/user/star',
        method: 'get',
        params: data,
    })
}

export function userStar(data) {
    return request({
        url: '/user/star',
        method: 'post',
        data: data,
    })
}

export function userUnStar(data) {
    return request({
        url: '/user/star',
        method: 'delete',
        data: data,
    })
}