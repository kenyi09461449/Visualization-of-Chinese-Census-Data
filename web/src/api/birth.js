import request from '@/utils/request'

export function birthAdd(data) {
    return request({
        url: '/birth',
        method: 'post',
        data
    })
}

export function birthDelete(ids) {
    return request({
        url: '/birth',
        method: 'delete',
        params: {
            id: ids
        }
    })
}

export function birthUpdate(data) {
    return request({
        url: '/birth',
        method: 'put',
        data
    })
}

export function birthList(params) {
    return request({
        url: '/birth',
        method: 'get',
        params
    })
}