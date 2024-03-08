import { ElMessage } from 'element-plus';

export const public_elmsg_info = (msg: string) => {
    ElMessage({ type: 'info', message: msg })
};

export const public_elmsg_success = (msg: string) => {
    ElMessage({ type: 'success', message: msg })
};

export const public_elmsg_warning = (msg: string) => {
    ElMessage({ type: 'warning', message: msg })
};

export const public_elmsg_error = (msg: string) => {
    ElMessage({ type: 'error', message: msg })
};