<script setup>
import {onMounted, ref} from 'vue';
import {ElMessage, ElMessageBox} from "element-plus";
import {provinceAdd, provinceDelete, provinceList, provinceUpdate} from "@/api/province.js";
import {_export, _import, upload} from "@/api/upload.js";
import {ElLoading} from 'element-plus'

const queryInfo = ref({
    pageNo: 1,
    pageSize: 10,
    year: "",
});

const dataList = ref([]);
const total = ref(0);

const addDialogVisible = ref(false);
const addForm = ref({});

const editDialogVisible = ref(false);
const editForm = ref({});

const getDataList = () => {
    provinceList(queryInfo.value).then((res) => {
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
        year: ""
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

const showEditBox = (data) => {
    editForm.value = data
    editDialogVisible.value = true
}

// delete province by id
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
        provinceDelete(id).then((res) => {
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
    provinceAdd(addForm.value).then((res) => {
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
    provinceUpdate(editForm.value).then((res) => {
        if (res.code === 200) {
            getDataList()
            editDialogVisible.value = false
            ElMessage.success("Update success");
        } else {
            ElMessage.error("Update failed");
        }
    })
}

const importData = async (file) => {
    const formData = new FormData();
    formData.append("file", file.file);
    let res = await upload(formData);

    if (res.code !== 200) {
        ElMessage.error("Import failed");
        return
    }

    const loading = ElLoading.service({
        lock: true,
        text: 'Import data...',
        background: 'rgba(0, 0, 0, 0.7)',
    })

    let result = await _import({
        data: "province",
        file: res.data
    });

    if (result.code === 200) {

        ElMessage.success("Import success");
        getDataList();
    } else {
        ElMessage.error("Import failed");
    }

    // close loading
    loading.close();
}

const exportData = () => {
    console.log("export")
    _export({
        "data": "province"
    }).then((res) => {
        if (res.code === 200) {
            window.open(res.data);
            ElMessage.success("Export success");
        } else {
            ElMessage.error("Export failed");
        }
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
                    <el-input v-model="queryInfo.year" placeholder="Year"></el-input>
                </el-col>
                <el-col :span="4">
                    <el-button type="primary" @click="getDataList">
                        Search
                    </el-button>
                    <el-button type="info" @click="resetDataList">
                        Reset
                    </el-button>
                    <el-button type="primary" plain @click="addDialogVisible = true">
                        Create
                    </el-button>
                </el-col>
                <el-col :span="1.5">
                    <el-upload
                        ref="uploadRef"
                        class="upload-demo" :show-file-list="false"
                        :http-request="importData"
                    >
                        <template #trigger>
                            <el-button type="success">Import</el-button>
                        </template>
                    </el-upload>
                </el-col>
                <el-col :span="2">
                    <el-button type="warning" @click="exportData">Export</el-button>
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
                <el-table-column prop="year" label="Year"></el-table-column>
                <el-table-column prop="province" label="Province"></el-table-column>
                <el-table-column prop="total" label="Gdp"></el-table-column>
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

    <el-dialog title="Add" v-model="addDialogVisible" width="30%">
        <el-form :model="addForm">
            <el-form-item prop="year">
                <el-input ref="year" v-model="addForm.year" size="large" placeholder="Year" name="year" tabIndex="-1"
                          auto-complete="on"></el-input>
            </el-form-item>
            <el-form-item prop="birth">
                <el-input v-model="addForm.province" size="large" placeholder="Province" name="birth" tabIndex="-1"
                          auto-complete="on"></el-input>
            </el-form-item>
            <el-form-item prop="death">
                <el-input v-model="addForm.total" size="large" placeholder="Gdp" name="death"
                          tabIndex="-1" auto-complete="on"></el-input>
            </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="addUser">Confirm</el-button>
        </span>
    </el-dialog>

    <el-dialog title="Edit" v-model="editDialogVisible" width="30%">
        <el-form :model="editForm">
            <el-form-item prop="year">
                <el-input ref="year" v-model="editForm.year" size="large" placeholder="Year" name="year" tabIndex="-1"
                          auto-complete="on"></el-input>
            </el-form-item>
            <el-form-item prop="birth">
                <el-input v-model="editForm.province" size="large" placeholder="Province" name="birth" tabIndex="-1"
                          auto-complete="on"></el-input>
            </el-form-item>
            <el-form-item prop="death">
                <el-input v-model="editForm.total" size="large" placeholder="Gdp" name="death"
                          tabIndex="-1" auto-complete="on"></el-input>
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