<script setup>
import {onMounted, ref} from 'vue';
import {useRouter} from "vue-router";
import {useStore} from "vuex";


const router = useRouter();
const store = useStore();

const jumpPage = (name) => {
    router.push({name});
}

const init = () => {
    // user is not login
    console.log("userinfo",store.state.user)
    if (!store.state.user) {
        router.push({name: 'Login'});
    }
}

const logout = () => {
    store.commit('REMOVE_INFO');
    router.push('/');
}

onMounted(() => {
    init();
})
</script>

<template>
    <el-header class="header">
        <div class="header-container">
            <div class="logo" @click="jumpPage('Home')">
                <div class="logo-img">
                    <img src="/logo.png">
                </div>
            </div>
            <div class="btn-group" v-if="!store.state.user">
                <div class="login">
                    <el-button type="primary" @click="jumpPage('Login')">Log in</el-button>
                </div>
                <div class="register">
                    <el-button @click="jumpPage('Register')">Sign up</el-button>
                </div>
            </div>
            <div class="btn-group" v-else>
                <el-popover
                    placement="bottom"
                    :width="300"
                    trigger="click"
                    v-if="store.state.user.role ===1"
                >
                    <template #reference>
                        <el-text class="welcome">
                            <el-icon size="22">
                                <Bell/>
                            </el-icon>
                        </el-text>
                    </template>
                </el-popover>

                <el-dropdown>
                    <el-avatar :size="50">
                        {{ store.getters.getUser.username }}
                    </el-avatar>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item @click="logout">Sign out</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </div>
        </div>
    </el-header>
</template>


<style scoped>
.header {
    width: 100%;
    height: 80px;
    box-shadow: 0 5px 10px 0 rgba(17, 58, 93, 0.1);
    background: #e1f1f8;
    //background: #5470c6;
}

.welcome {
    color: black;
}

.header-container {
    height: 80px;
    margin: auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    display: flex;
    justify-content: space-evenly;
    gap: 10px;
    align-items: center;
    cursor: pointer;
}

.logo-img > img {
    width: 250px;
    height: 80px;
}

.btn-group {
    display: flex;
    justify-content: space-evenly;
    gap: 10px;
}

.logo > .logo-desc {
    font-size: 40px;
    line-height: 80px;
}


.btn-group .el-avatar {
    outline: none;
}

.notice {
    width: 96%;
    max-height: 500px;
    overflow-y: scroll;
    scrollbar-width: none;
    -ms-overflow-style: none;
}

.notice-item {
    width: 100%;
    display: flex;
    flex-direction: column;
    margin-top: 10px;
}

.notice-item:not(:last-child) {
    border-bottom: 1px solid #e1dede;
}

.notice-title {
    font-weight: bolder;
}

.notice-date {
    font-size: 14px;
    color: #ccc9c9;
}

.notice-title-date {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.notice-content {
    margin-top: 10px;
    margin-bottom: 20px;
}
</style>