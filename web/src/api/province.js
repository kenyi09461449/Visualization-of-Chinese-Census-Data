import request from '@/utils/request'

export function provinceAdd(data) {
    return request({
        url: '/province',
        method: 'post',
        data
    })
}

export function provinceDelete(ids) {
    return request({
        url: '/province',
        method: 'delete',
        params: {
            id: ids
        }
    })
}

export function provinceUpdate(data) {
    return request({
        url: '/province',
        method: 'put',
        data
    })
}

export function provinceList(params) {
    return request({
        url: '/province',
        method: 'get',
        params
    })
}