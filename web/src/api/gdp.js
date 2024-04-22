import request from '@/utils/request'

export function gdpAdd(data) {
    return request({
        url: '/gdp',
        method: 'post',
        data
    })
}

export function gdpDelete(ids) {
    return request({
        url: '/gdp',
        method: 'delete',
        params: {
            id: ids
        }
    })
}

export function gdpUpdate(data) {
    return request({
        url: '/gdp',
        method: 'put',
        data
    })
}

export function gdpList(params) {
    return request({
        url: '/gdp',
        method: 'get',
        params
    })
}