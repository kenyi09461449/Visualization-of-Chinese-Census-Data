<script setup>
import {useRouter} from "vue-router";
import {useStore} from "vuex";
import {onMounted, ref} from "vue";

const router = useRouter();
const store = useStore();

const activeIndex = ref('')
const handleSelect = (key, keyPath) => {
    activeIndex.value = key
};

const handleLogout = () => {
    window.localStorage.clear()
    window.sessionStorage.clear()
    router.push('/login')
}

const handleHome = () => {
    router.push('/index')
}

const handleMyCollection = () => {
    router.push('/collection')
}

const handleJump = () => {
    router.push('/index')
}

const init = () => {
    // user if login
    if (!window.sessionStorage.getItem('user')) {
        router.push('/login')
        console.log("no login")
    }
}

onMounted(() => {
    init()
})
</script>

<template>
    <el-container>
        <el-header>
            <el-menu
                class="el-menu-demo"
                mode="horizontal"
                :ellipsis="false"
                @select="handleSelect"
            >
                <el-menu-item index="0" @click="handleHome">
                    <img
                        style="width: 200px;height: 50px;"
                        src="/logo.png"
                        alt="Logo"
                    />
                </el-menu-item>
                <div class="flex-grow"/>
                <el-sub-menu index="2">
                    <template #title>Welcome, {{ store.state.user.username }}</template>
                    <el-menu-item index="2-1" @click="handleMyCollection">My collection</el-menu-item>
                    <el-menu-item index="2-1" @click="handleLogout">Logout</el-menu-item>
                </el-sub-menu>
            </el-menu>
        </el-header>

        <el-main>
            <el-card shadow="always">
                <template #header>
                    <div class="card-header">
                        <h1>
                            China census data visualization website
                        </h1>
                    </div>
                </template>
                <p class="el-card-content">
                    As the most populous country in the world, China's population structure, distribution and changes
                    have an important impact on the socio-economic development of China and the world. With the rapid
                    development of Chinese society and the acceleration of urbanization, the demand for in-depth
                    analysis of China's population data is growing. However, although the seventh Chinese census
                    provides rich demographic data, these data are often presented in lengthy reports that lack
                    intuitive presentation methods, making it difficult for the general public to understand and
                    utilize. Therefore, this study aims to use data visualization technology to present the seventh
                    Chinese census data on a public-facing website in an interactive and intuitive manner to promote a
                    deeper understanding of China's population situation.
                </p>

                <p class="el-card-content">

                    The goal of this project is to develop a website for a broad audience that will present the main
                    characteristics, trends, and geographical distribution of China's population through visual means
                    such as charts, maps, and data graphics. Through this website, users can easily explore various
                    aspects of China's population, including but not limited to age structure, gender ratio, urban and
                    rural distribution, etc. In addition, the website will also provide functions such as historical
                    data comparison to help users better understand the historical trajectory and future direction of
                    China's population development.
                </p>

                <p class="el-card-content">
                    Through the implementation of this project, we hope to provide an open, intuitive and trustworthy
                    platform for scholars, policymakers, media workers and the general public to promote more in-depth
                    research, discussion and understanding of China's population issues. At the same time, we also hope
                    that this project can provide an example for the application of data visualization technology in the
                    field of demographics, and provide experience and inspiration for the development of similar
                    projects in the future.
                </p>

                <el-button plain type="primary" @click="handleJump">
                    Start exploring
                </el-button>
            </el-card>
        </el-main>
    </el-container>
</template>

<style scoped>
.flex-grow {
    flex-grow: 1;
}

.el-main {
    margin: 20px auto;
    width: 80% !important;

    padding: unset !important;
}

.el-header {
    padding: 0;
}

.el-card-content {
    margin: 20px 0;
    line-height: 20px;
    //letter-spacing: px;
    text-indent: 20px;
}

.chart-tab {
    background-color: white;
    width: 100%;
    margin: 30px auto;
    padding: 50px;
}

.chart {
    width: 100%;
    height: 60vh;
}

.footer {
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}

.footer-desc {

}
</style>