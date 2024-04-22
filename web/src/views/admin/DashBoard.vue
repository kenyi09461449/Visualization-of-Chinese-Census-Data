<script>
import Menu from "@/components/pc/Menu.vue";
import menu from "@/router/menu";
import Header from "@/views/layout/Header.vue";

export default {
    name: "DashBoard",
    components: {
        Header,
        Menu: Menu
    },
    data() {
        return {
            // activeIndex: '/index',
            menuData: [],
            year: new Date().getFullYear()
        };
    },
    mounted() {
        this.menuData = menu.root
    },
    methods: {
        logout() {
            this.$store.commit('REMOVE_INFO');
            this.$router.push('/login');
        }
    }
};
</script>

<template>
    <el-container class="el-container-fix">
        <Header></Header>

        <el-container>
            <el-aside width="250px" class="el-aside">
                <el-menu
                    :default-active="$route.path"
                    background-color="#fff"
                    text-color="#312f2fd4"
                    text-align="left"
                    active-text-color="#fff"
                >
                    <Menu :navMenus="menuData"></Menu>
                </el-menu>
            </el-aside>

            <el-container>
                <el-main>
                    <router-view></router-view>
                </el-main>
            </el-container>
        </el-container>
    </el-container>
</template>

<style scoped>
.el-container-fix {
    flex-direction: column;
}

.el-header-fix {
    background-color: rgb(23, 146, 255);
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.left {
    font-size: 24px;
}

.text-large {
    color: white;
}

.el-aside {
    background-color: #fff;
    height: calc(100vh - 80px);
    border: 0;
}

.el-main {
    --el-main-padding: 20px auto;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    background-color: #f0f2f5;
    padding: 10px 5px;
}

.el-footer-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: fixed;
    bottom: 0;
    text-align: right;
    width: 100%;
}

.el-page-header__header {
    margin-left: 10px;
    margin-bottom: 10px;
}

.el-menu-item:hover {
    background-color: rgb(154 181 219 / 22%);
}
</style>