import {createApp} from 'vue'

import ElementPlus from 'element-plus'
import 'element-plus/theme-chalk/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import BaiduMap from 'vue-baidu-map-3x';
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'
import store from './store'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(store)
app.use(router)
app.use(ElementPlus)
app.use(BaiduMap, {
    ak: 'xmzV94OpCNnSPWDBSBsOya7h6iPCzzYC'
})

app.mount('#app')
