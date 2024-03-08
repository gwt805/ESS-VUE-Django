import http from "@/utils/axios";

// user
export const admin_get_user_info_list = async (currentPage:number, pageSize:number, email: string) => {
    return await http.post("api/ess/admin/admin_get_user_info_list/", {currentPage: currentPage, pageSize: pageSize, email: email});
};

export const admin_get_user_info = async (username: string) => {
    return await http.post("api/ess/admin/admin_get_user_info/", {username: username});
};

export const admin_update_user_info = async ( auth:string, username: string, zh_uname: string, email: string, group: string, img: string, power: string) => {
    return await http.post("api/ess/admin/admin_update_user_info/", {auth: auth, username: username, zh_uname: zh_uname, email: email, group: group, img: img, power: power});
};

export const admin_update_user_pwd = async (auth: string, username: string, password: string) => {
    return await http.post("api/ess/admin/admin_update_user_pwd/", {auth: auth, username: username, password: password});
};

// project
export const admin_get_project_info_list = async (currentPage: number, pageSize: number, pname: string) => {
    return await http.post("api/ess/admin/admin_get_project_info_list/", {currentPage: currentPage, pageSize: pageSize, pname: pname});;
};

export const admin_add_project = async (auth: string, pname: string) => {
    return await http.post("api/ess/admin/admin_add_project/", {auth: auth, pname: pname});
};

export const admin_get_project_info = async (id: number) => {
    return await http.post("api/ess/admin/admin_get_project_info/", {id: id});
};

export const admin_update_project_info = async (auth: string, id: number, pname: string) => {
    return await http.post("api/ess/admin/admin_update_project_info/", {auth: auth, id: id, pname: pname});
};

export const admin_delete_project = async (auth: string, id: number) => {
    return await http.post("api/ess/admin/admin_delete_project/", {auth: auth, id: id});
};

// supplier
export const admin_get_supplier_info_list = async (currentPage: number, pageSize: number) => {
    return await http.post("api/ess/admin/admin_get_supplier_info_list/", {currentPage: currentPage, pageSize: pageSize});
};

export const admin_add_supplier = async (auth: string, name: string) => {
    return await http.post("api/ess/admin/admin_add_supplier/", {name: name, auth: auth});
};

export const admin_get_supplier_info = async (id: number) => {
    return await http.post("api/ess/admin/admin_get_supplier_info/", {id: id});
};

export const admin_update_supplier_info = async (auth: string, id: number, name: string) => {
    return await http.post("api/ess/admin/admin_update_supplier_info/", {auth: auth, id: id, name: name});
};

export const admin_delete_psupplier = async (auth: string, id: number) => {
    return await http.post("api/ess/admin/admin_delete_supplier/", {auth: auth, id: id});
};

// task kind
export const admin_get_task_kind_info_list = async (currentPage: number, pageSize: number) => {
    return await http.post("api/ess/admin/admin_get_task_kind_info_list/", {currentPage: currentPage, pageSize: pageSize });
};

export const admin_add_task_kind = async (auth: string, kinds: string) => {
    return await http.post("api/ess/admin/admin_add_task_kind/", { auth: auth, kinds: kinds });
};

export const admin_get_task_kind_info = async (id: number) => {
    return await http.post("api/ess/admin/admin_get_task_kind_info/", { id: id });
};

export const admin_update_task_kind_info = async (auth: string, id: number, kinds: string) => {
    return await http.post("api/ess/admin/admin_update_task_kind_info/", { auth: auth, id: id, kinds: kinds });
};

export const admin_delete_task_kind = async (auth: string, id: number) => {
    return await http.post("api/ess/admin/admin_delete_task_kind/", { auth: auth, id: id });
};

// year project budget
export const admin_get_ybudget_data = async (year: number, currentPage: number, pageSize: number) => {
    return await http.post("api/ess/admin/admin_get_ybudget_data/", { year: year, currentPage: currentPage, pageSize: pageSize });
};

export const admin_add_ybudget_data = async (username: string, year: number, mpname: string, pnamel: string) => {
    return await http.post("api/ess/admin/admin_add_ybudget_data/", { username: username, year: year, mpname: mpname, pnamel: pnamel });
};

export const admin_get_ybudget_data_one = async (id: number) => {
    return await http.post("api/ess/admin/admin_get_ybudget_data_one/", { id: id });
};

export const admin_update_ybudget_data = async (username: string, id: any, year: number, mpname: string, pnamel: string) => {
    return await http.post("api/ess/admin/admin_update_ybudget_data/", { username: username, id: id, year: year, mpname: mpname, pnamel: pnamel });
};

export const admin_delete_ybudget_data = async (username: string, id: number) => {
    return await http.post("api/ess/admin/admin_delete_ybudget_data/", { username: username, id: id });
};