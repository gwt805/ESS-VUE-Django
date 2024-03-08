import http from "@/utils/axios";

export const user_list = async () => {
  return await http.get("/api/ess/pubcli/get_user_list");
};

export const project_list = async () => {
  return await http.get("/api/ess/pubcli/get_project_list");
};

export const supplier_list = async () => {
  return await http.get("/api/ess/pubcli/get_supplier_list");
};

export const anno_task_kind_list = async () => {
  return await http.get("/api/ess/pubcli/get_anno_task_kind_list");
};
