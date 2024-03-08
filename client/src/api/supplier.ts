import http from "@/utils/axios";

export const get_supplier_data = async (
  pname: string,
  supplier: string,
  send_begin_time: string,
  send_last_time: string,
  pay_begin_time: string,
  pay_last_time: string,
  pageIndex: number,
  pageSize: number
) => {
  return await http.post("api/ess/supplier/get_supplier_task_data/", {
    pname: pname,
    supplier: supplier,
    send_begin_time: send_begin_time,
    send_last_time: send_last_time,
    pay_begin_time: pay_begin_time,
    pay_last_time: pay_last_time,
    pageIndex: pageIndex,
    pageSize: pageSize,
  });
};

export const get_all_supplier_task_data = async (
  pname: string,
  supplier: string,
  send_begin_time: string,
  send_last_time: string,
  pay_begin_time: string,
  pay_last_time: string
) => {
  return await http.post("api/ess/supplier/get_all_supplier_task_data/", {
    pname: pname,
    supplier: supplier,
    send_begin_time: send_begin_time,
    send_last_time: send_last_time,
    pay_begin_time: pay_begin_time,
    pay_last_time: pay_last_time
  });
};

export const get_supplier_task_data_one = async (id: number) => {
  return await http.post("api/ess/supplier/get_supplier_task_data_one/", { id: id })
}

export const add_supplier_task_data = async (
  auth: string,
  user: string,
  pname: string,
  send_data_batch: string,
  send_data_time: string,
  pnums: number,
  data_source: string,
  scene: string,
  send_reason: string,
  key_frame_extracted_methods: string,
  ann_field_flag: string,
  wb_name: string
) => {
  return await http.post("api/ess/supplier/add_supplier_task_data/", {
    auth: auth,
    user: user,
    pname: pname,
    send_data_batch: send_data_batch,
    send_data_time: send_data_time,
    pnums: pnums,
    data_source: data_source,
    scene: scene,
    send_reason: send_reason,
    key_frame_extracted_methods: key_frame_extracted_methods,
    ann_field_flag: ann_field_flag,
    wb_name: wb_name,
  });
};

export const update_supplier_task_data = async (
  auth: string,
  id: string,
  user: string,
  pname: string,
  send_data_batch: string,
  send_data_time: string,
  pnums: number,
  data_source: string,
  scene: string,
  send_reason: string,
  ann_field_flag: string,
  key_frame_extracted_methods: string,
  begin_check_data_time: string,
  last_check_data_time: string,
  get_data_time: string,
  ann_meta_data: Array<any>,
  anno_task_id: string,
  wb_name: string,
  username: string
) => {
  return await http.post("api/ess/supplier/update_supplier_task_data/", {
    auth: auth,
    id: id,
    user: user,
    pname: pname,
    send_data_batch: send_data_batch,
    send_data_time: send_data_time,
    pnums: pnums,
    data_source: data_source,
    scene: scene,
    send_reason: send_reason,
    ann_field_flag: ann_field_flag,
    key_frame_extracted_methods: key_frame_extracted_methods,
    begin_check_data_time: begin_check_data_time,
    last_check_data_time: last_check_data_time,
    get_data_time: get_data_time,
    ann_meta_data: ann_meta_data,
    anno_task_id: anno_task_id,
    wb_name: wb_name,
    username: username
  });
};

export const delete_supplier_task_data = async (id: number, uname: string) => {
  return await http.post("api/ess/supplier/delete_supplier_task_data/", {
    id: id,
    uname: uname,
  });
};

export const get_supplier_task_count = async (
  select_time_method: string,
  supplier_name: string,
  start_time: string,
  last_time: string
) => {
  return await http.post("api/ess/supplier/get_supplier_task_count/", {
    select_time_method: select_time_method,
    supplier_name: supplier_name,
    start_time: start_time,
    last_time: last_time,
  });
};

export const get_supplier_data_jsfs = async () => {
  return await http.get("api/ess/supplier/get_supplier_data_jsfs/");
};

export const add_budget_data = async (username: string, year: number, proname: string, money: number) => {
  return await http.post("api/ess/budget/add_budget_data/", { username: username, year: year, proname: proname, money: money });
};

export const get_budget_all_data = async (year: number, currentPage: number, pageSize: number) => {
  return await http.post("api/ess/budget/get_budget_all_data/", { year: year, currentPage: currentPage, pageSize: pageSize });
};

export const get_budget_one_data = async (id: number) => {
  return await http.post("api/ess/budget/get_budget_one_data/", { id: id });
};

export const update_budget_data = async (
  username: string,
  id: number,
  proname: string,
  ann_budget: number,
  one_third_report_time: string,
  one_third_report_file: string,
  two_third_report_time: string,
  two_third_report_file: string,
  third_third_report_time: string,
  third_third_report_file: string
) => {
  return await http.post("api/ess/budget/update_budget_data/", {
    username: username,
    id: id,
    proname: proname,
    ann_budget: ann_budget,
    one_third_report_time: one_third_report_time,
    one_third_report_file: one_third_report_file,
    two_third_report_time: two_third_report_time,
    two_third_report_file: two_third_report_file,
    third_third_report_time: third_third_report_time,
    third_third_report_file: third_third_report_file
  })
};

export const delete_budget_data = async (username: string, id: number) => {
  return await http.post("api/ess/budget/delete_budget_data/", { username: username, id: id });
};