import request from '@/utils/request'


export function upload(data) {
    return request({
        url: '/upload',
        method: 'post',
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        data
    })
}

export function _export(data) {
    return request({
        url: '/export',
        method: 'get',
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        params: data
    })
}

export function _import(data) {
    return request({
        url: '/import',
        method: 'post',
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        data
    })
}