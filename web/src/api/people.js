import request from '@/utils/request'

export function peopleAdd(data) {
    return request({
        url: '/people',
        method: 'post',
        data
    })
}

export function peopleDelete(ids) {
    return request({
        url: '/people',
        method: 'delete',
        params: {
            id: ids
        }
    })
}

export function peopleUpdate(data) {
    return request({
        url: '/people',
        method: 'put',
        data
    })
}

export function peopleList(params) {
    return request({
        url: '/people',
        method: 'get',
        params
    })
}