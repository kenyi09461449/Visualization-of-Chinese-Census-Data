<script setup>
import {onMounted, ref} from 'vue';
import {ElMessage, ElMessageBox} from "element-plus";
import {userAdd, userDelete, userList, userUpdate} from "@/api/user.js";
import {upload} from "@/api/upload.js";

const queryInfo = ref({
    pageNo: 1,
    pageSize: 10,
    username: "",
    email: "",
    phone: ""
});

const dataList = ref([]);
const total = ref(0);

const addDialogVisible = ref(false);
const addForm = ref({});

const editDialogVisible = ref(false);
const editForm = ref({});

const getDataList = () => {
    userList(queryInfo.value).then((res) => {
        if (res.code === 200) {
            dataList.value = res.data.list;
            total.value = res.data.total || 0;
        } else {
            ElMessage.error(res.msg);
        }
    }).catch((err) => {
        console.log(err);
    });
}

const resetDataList = () => {
    queryInfo.value = {
        pageNo: 1,
        pageSize: 10,
        username: "",
        email: "",
        phone: ""
    };
    getDataList();
}

const handleSizeChange = (newSize) => {
    queryInfo.value.pageSize = newSize;
    getDataList();
}

const handleCurrentChange = (newPage) => {
    queryInfo.value.pageNo = newPage;
    getDataList();
}

const showEditBox = (user) => {
    editForm.value = user
    editDialogVisible.value = true
}

// delete user by id
const deleteById = async (id) => {
    const confirmResult = await ElMessageBox.confirm(
        "Confirm deletion?",
        "Tips",
        {
            confirmButtonText: "Confirm",
            cancelButtonText: "Cancel",
            type: "warning",
        }
    ).catch((err) => err);

    if (confirmResult === "confirm") {
        userDelete(id).then((res) => {
            if (res.code === 200) {
                getDataList();
                ElMessage.success("Delete success");
            } else {
                ElMessage.error("Delete failed");
            }
        }).catch((err) => {
            console.log(err);
            ElMessage.error("Network error");
        });
    }
}

const addUser = () => {
    userAdd(addForm.value).then((res) => {
        if (res.code === 200) {
            getDataList()
            addDialogVisible.value = false
            ElMessage.success("Add success");
        } else {
            ElMessage.error("Add failed");
        }
    })
}

const editUser = () => {
    userUpdate(editForm.value).then((res) => {
        if (res.code === 200) {
            getDataList()
            editDialogVisible.value = false
            ElMessage.success("Update success");
        } else {
            ElMessage.error("Update failed");
        }
    })
}

const handleUpload = (file, callback) => {
    const formData = new FormData()
    formData.append('file', file.file) // 传入bpmn文件

    upload(formData).then((res) => {
        if (res.code === 200) {
            ElMessage.success("Upload success");
            callback && callback(res);
        } else {
            ElMessage.error("Upload failed");
        }
    }).catch((err) => {
        ElMessage.error("Network error");
    });
}

const handleAddUserAvatar = (file) => {
    handleUpload(file, (res) => {
        addForm.value.avatar = res.data
    })
}

const handleEditUserAvatar = (file) => {
    handleUpload(file, (res) => {
        editForm.value.avatar = res.data
    })
}

// load data
onMounted(() => {
    getDataList();
})
</script>


<template>
    <el-container class="el-container-fix">
        <el-header>
            <el-row :gutter="20">
                <el-col :span="4">
                    <el-input
                        placeholder="Enter username"
                        v-model="queryInfo.username"
                        clearable
                        @clear="getDataList"
                        @keydown.enter="getDataList"
                    >
                        <template #prepend>Username</template>
                    </el-input>
                </el-col>
                <el-col :span="4">
                    <el-input
                        placeholder="Enter user email"
                        v-model="queryInfo.email"
                        clearable
                        @clear="getDataList"
                        @keydown.enter="getDataList"
                    >
                        <template #prepend>Email</template>
                    </el-input>
                </el-col>
                <el-col :span="6">
                    <el-button type="primary" @click="getDataList">
                        Search
                    </el-button>
                    <el-button type="info" @click="resetDataList">
                        Reset
                    </el-button>
                    <el-button type="primary" plain @click="addDialogVisible = true">
                        Add
                    </el-button>
                </el-col>
            </el-row>
        </el-header>

        <el-main>
            <el-table
                :data="dataList"
                height="650"
                ref="filterTable"
                :border="true"
                stripe
            >
                <el-table-column prop="id" label="id" width="80"></el-table-column>
                <el-table-column prop="username" label="Username"></el-table-column>
                <el-table-column prop="email" label="Email"></el-table-column>
                <el-table-column prop="create_at" label="Registration Time"></el-table-column>
                <el-table-column label="Action" width="300">
                    <template #default="scope">
                        <el-button
                            type="warning"
                            size="small"
                            icon="Edit"
                            @click="showEditBox(scope.row)"
                        >Edit
                        </el-button>
                        <el-button
                            size="small"
                            type="danger"
                            icon="Delete"
                            @click="deleteById(scope.row.id)"
                        >Delete
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </el-main>

        <el-row>
            <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="queryInfo.pageNo"
                :page-sizes="[10, 20, 50, 100]"
                :page-size="queryInfo.pageSize"
                :total="total"
                layout="total,prev, pager, next,jumper"
            >
            </el-pagination>
        </el-row>
    </el-container>

    <el-dialog title="Add user" v-model="addDialogVisible" width="30%">
        <el-form :model="addForm">
            <el-form-item prop="username">
                <el-input v-model="addForm.username" placeholder="Username" size="large"
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
                          v-model="addForm.password" size="large"
                          placeholder="Password" name="password" tabIndex="-1" auto-complete="on"
                >
                    <template #prefix>
                        <el-icon class="el-input__icon">
                            <Lock/>
                        </el-icon>
                    </template>
                </el-input>
            </el-form-item>
            <el-form-item prop="email">
                <el-input ref="email"
                          v-model="addForm.email" size="large"
                          placeholder="Email" name="email" tabIndex="-1" auto-complete="on"
                >
                    <template #prefix>
                        <el-icon class="el-input__icon">
                            <ChatDotRound/>
                        </el-icon>
                    </template>
                </el-input>
            </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="addUser">Confirm</el-button>
        </span>
    </el-dialog>

    <el-dialog title="Edit user" v-model="editDialogVisible" width="30%">
        <el-form :model="editForm">
            <el-form-item prop="username">
                <el-input v-model="editForm.username" placeholder="Username" size="large"
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
                          v-model="editForm.password" size="large"
                          placeholder="Password" name="password" tabIndex="-1" auto-complete="on"
                >
                    <template #prefix>
                        <el-icon class="el-input__icon">
                            <Lock/>
                        </el-icon>
                    </template>
                </el-input>
            </el-form-item>
            <el-form-item prop="email">
                <el-input ref="email"
                          v-model="editForm.email" size="large"
                          placeholder="Email" name="email" tabIndex="-1" auto-complete="on"
                >
                    <template #prefix>
                        <el-icon class="el-input__icon">
                            <ChatDotRound/>
                        </el-icon>
                    </template>
                </el-input>
            </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="editUser">Confirm</el-button>
        </span>
    </el-dialog>
</template>

<style scoped>
.el-container-fix {
    width: 98%;
    margin: auto;
    padding: 20px 0;
}

.row-image {
    width: 50%;
    height: 100px;
}
</style>