import request from '@/utils/request'


export function getChartData(url, params) {
    return request({
        url: url,
        method: 'get',
        params: params,
    })
}