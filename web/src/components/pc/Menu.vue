<template>
    <div class="navMenu">
        <template v-for="navMenu in navMenus">
            <el-menu-item v-if="!navMenu.children" :key="navMenu.id" :index="navMenu.name"
                          @click="redirect(navMenu.name,navMenu.alias)">
                <el-icon>
                    <component :is="navMenu.icon"></component>
                </el-icon>
                <span slot="title">{{ navMenu.alias }}</span>
            </el-menu-item>
            <el-sub-menu v-if="navMenu.children" :index="navMenu.name">
                <template #title>
                    <el-icon>
                        <component :is="navMenu.icon"></component>
                    </el-icon>
                    <span>{{ navMenu.alias }}</span>
                </template>
                <el-menu-item
                    :index="child.name"
                    v-for="child in navMenu.children"
                    @click="redirect(child.name,child.alias)"
                >
                    <el-icon>
                        <component :is="child.icon"></component>
                    </el-icon>
                    <span>{{ child.alias }}</span>
                </el-menu-item>
            </el-sub-menu>
        </template>
    </div>
</template>

<script setup>
import {onMounted, ref, watch} from 'vue'
import {useRouter} from 'vue-router'
import {useStore} from 'vuex'

const router = useRouter();
const store = useStore();
const navMenus = ref([]);
const props = defineProps(['navMenus'])

const redirect = (link, name) => {
    router.push(link)
    store.state.tagName = name;
}

onMounted(() => {
    navMenus.value = props.navMenus
})

watch(() => props.navMenus, () => {
    navMenus.value = props.navMenus
})
</script>

<style>
.el-menu-item.is-active {
    color: #409EFF !important;
}
</style>