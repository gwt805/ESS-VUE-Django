import http from "@/utils/axios";

// project name
export const admin_get_slesspn = async (currentPage: number, pageSize: number) => {
    return await http.post("api/ess/admin/admin_get_slesspn/", { currentPage: currentPage, pageSize: pageSize });
};

export const admin_add_slesspn = async (username: string, esspname: string, slpname: string) => {
    return await http.post("api/ess/admin/admin_add_slesspn/", { username: username, esspname: esspname, slpname: slpname });
};

export const admin_get_slesspn_one = async (id: number) => {
    return await http.post("api/ess/admin/admin_get_slesspn_one/", { id: id });
};

export const admin_update_slesspn = async (username: string, id: number, esspname: string, slpname: string) => {
    return await http.post("api/ess/admin/admin_update_slesspn/", {username: username, id: id, esspname: esspname, slpname: slpname});
};

export const admin_delete_slesspn = async (username: string, id: number) => {
    return await http.post("api/ess/admin/admin_delete_slesspn/", { username: username, id: id });
};

// vender
export const admin_get_slessvd = async (currentPage: number, pageSize: number) => {
    return await http.post("api/ess/admin/admin_get_slessvd/", { currentPage: currentPage, pageSize: pageSize });
};

export const admin_add_slessvd = async (username: string, essvender: string, slvender: string) => {
    return await http.post("api/ess/admin/admin_add_slessvd/", { username: username, essvender: essvender, slvender: slvender });
};

export const admin_get_slessvd_one = async (id: number) => {
    return await http.post("api/ess/admin/admin_get_slessvd_one/", { id: id });
};

export const admin_update_slessvd = async (username: string, id: number, essvender: string, slvender: string) => {
    return await http.post("api/ess/admin/admin_update_slessvd/", { username: username, id: id, essvender: essvender, slvender: slvender });
};

export const admin_delete_slessvd = async (username: string, id: number) => {
    return await http.post("api/ess/admin/admin_delete_slessvd/", { username: username, id: id });
};