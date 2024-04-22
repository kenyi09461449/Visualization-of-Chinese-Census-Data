<script setup>
import {ref, reactive, onMounted} from 'vue';
import {userLogin} from "@/api/user";
// import Footer from "@/views/pc/layout/Footer.vue";
import {useRouter} from "vue-router";
import {useStore} from "vuex";
import {ElMessage} from "element-plus";

const store = useStore();
const router = useRouter();

// loginForm
const loginForm = reactive({
    username: '',
    password: ''
});

// verify username
const validateUsername = (rule, value, callback) => {
    if (!value) {
        callback(new Error('Please enter your username'));
    } else {
        callback();
    }
};

// verify password
const validatePassword = (rule, value, callback) => {
    if (value.length < 6) {
        callback(new Error('The password can not be less than 6 digits'));
    } else {
        callback();
    }
};

const loginFormRef = ref(null);

// validate form
const validateForm = (callback) => {
    loginFormRef.value.validate((valid) => {
        if (valid) {
            callback();
        } else {
            console.log('error submit!!');
        }
    });
};

// loginForm ref
const loginRules = {
    username: [
        {required: true, trigger: 'blur', validator: validateUsername}
    ],
    password: [
        {required: true, trigger: 'blur', validator: validatePassword}
    ]
};

// loading state
const loading = ref(false);

// current year
const year = new Date().getFullYear();

// login request
const handleLogin = () => {
    validateForm(() => {
        loading.value = true;
        let params = {...loginForm};
        userLogin(params)
            .then((res) => {
                loading.value = false;
                if (res.code === 200) {
                    // save token and userinfo
                    store.commit('SET_USERINFO', res.data);
                    ElMessage.success('Login successful!');
                    if (res.data.role === 0) {
                        router.push({name: 'UserList'});
                    } else {
                        router.push({name: 'home'});
                    }
                } else {
                    ElMessage.error(res.msg);
                }
            })
            .catch((error) => {
                console.error(error);
                loading.value = false;
            });
    });
};

</script>


<template>
    <div v-loading.fullscreen.lock="loading" element-loading-text="loading" element-loading-spinner="el-icon-loading"
         element-loading-background="rgba(0, 0, 0, 0.6)" class="login-container" :style="bg">

        <video src="/bg/bg.mp4" class="bg-video" muted loop autoplay></video>

        <div class="left-title">
            <h1 class="main-title">POPULATION DATA ANALYSIS</h1>
            <h3 class="main-desc">
                <a href="https://data.stats.gov.cn/">Data from https://data.stats.gov.cn/</a>
            </h3>
        </div>

        <div class="left-right">
            <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on"
                     label-position="left">
                <div class="title-container">
                    <h3 class="app-title">Login</h3>
                </div>

                <el-form-item prop="username">
                    <el-input v-model="loginForm.username" placeholder="Email / Username" size="large"
                              tabIndex="-1">
                        <template #prefix>
                            <el-icon class="el-input__icon">
                                <User/>
                            </el-icon>
                        </template>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input ref="password"
                              v-model="loginForm.password" size="large" show-password
                              placeholder="Password" name="password" tabIndex="-1" auto-complete="on"
                              @keyup.enter="handleLogin"
                    >
                        <template #prefix>
                            <el-icon class="el-input__icon">
                                <Lock/>
                            </el-icon>
                        </template>
                    </el-input>
                </el-form-item>

                <el-form-item>
                    <el-button type="primary" class="login-btn"
                               @click.native.prevent="handleLogin"
                               @keyup.enter.prevent="handleLogin">
                        Sign in
                    </el-button>
                </el-form-item>

                <div class="more-options">
                    <div class="more-options-left">
                        <div class="no-account-tips">Not a user?</div>
                        <div>
                            <el-link :underline="false" type="primary" href="#/register">Register</el-link>
                        </div>
                    </div>
                    <div class="more-options-right">

                    </div>
                </div>
            </el-form>
        </div>

    </div>

    <Footer class="footer"></Footer>
</template>

<style scoped>
.login-container {
    display: flex;
    justify-content: space-around;
    align-self: center;
    flex-direction: row;
    align-items: center;
    width: 100%;
    height: 100%;
}

.bg-video {
    width: 100%;
    height: 100%;
    position: absolute;
    object-fit: cover;
}

.left-title {
    margin-left: 100px;
    z-index: 99;
    color: white;
}

.main-title {
    font-size: 78px;
}

.main-desc {
    font-size: 32px;
}

.main-desc a {
    color: white;
    text-decoration: none;
}

.left-right {
    margin-right: 100px;
}

.title-container {
    margin: 30px auto;
}

.login-form {
    width: 500px;
    margin: 0 auto;
    padding: 20px;
    border-radius: 5px;
    background-color: #fff;
    z-index: 99;
    opacity: 0.85;
}

.app-title {
    text-align: center;
}

.login-btn {
    width: 100%;
    margin-bottom: 20px;
}

.footer {
    width: 100%;
    height: 20px;
    text-align: center;
    font-size: 14px;
    color: #000000;
    position: fixed;
    bottom: 30px;
}

.footer-company {
    color: white;
    width: 380px;
    margin: 0 auto;
}

.footer-company a {
    color: white;
}

.more-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.more-options-left {
    display: flex;
    justify-content: flex-start;
    align-items: center;
    gap: 10px;
    width: 50%;
}

.no-account-tips {
    font-size: 14px;
}

.footer {
    position: fixed;
    bottom: 10px;
    z-index: 99;
    color: white;
    font-size: 16px;
}
</style>