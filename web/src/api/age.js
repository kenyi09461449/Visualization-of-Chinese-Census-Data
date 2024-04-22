import request from '@/utils/request'

export function ageAdd(data) {
    return request({
        url: '/age',
        method: 'post',
        data
    })
}

export function ageDelete(ids) {
    return request({
        url: '/age',
        method: 'delete',
        params: {
            id: ids
        }
    })
}

export function ageUpdate(data) {
    return request({
        url: '/age',
        method: 'put',
        data
    })
}

export function ageList(params) {
    return request({
        url: '/age',
        method: 'get',
        params
    })
}