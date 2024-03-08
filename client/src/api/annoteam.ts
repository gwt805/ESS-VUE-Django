import http from "@/utils/axios";

export const search_annoteam_data = async (
  searchdata: any,
  pageIndex: number,
  pageSize: number
) => {
  return await http.post("/api/ess/annoteam/search_anno_team_data/", {
    uname: searchdata.uname,
    pname: searchdata.pname,
    begin_time: searchdata.begin_time,
    last_time: searchdata.last_time,
    taskid: searchdata.task_id,
    taskkind: searchdata.task_kind,
    supplier: searchdata.supplier,
    pageIndex: pageIndex,
    pageSize: pageSize,
  });
};

export const add_anno_task_data = async (
  auth:string,
  tsuname: string,
  tspname: string,
  tswaibao: string,
  tstask_id: string,
  tsdtime: string,
  tskind: string,
  tspnums: string,
  tsknums: string,
  tsptimes: string
) => {
  return await http.post("api/ess/annoteam/add_anno_task_data/", {
    auth: auth,
    tsuname: tsuname,
    tspname: tspname,
    tswaibao: tswaibao,
    tstask_id: tstask_id,
    tsdtime: tsdtime,
    tskind: tskind,
    tspnums: tspnums,
    tsknums: tsknums,
    tsptimes: tsptimes,
  })
};

export const get_anno_task_data_one = async (id: number) => {
  return await http.post("api/ess/annoteam/get_anno_task_data_one/", { id: id });
};

export const get_all_anno_team_data = async (searchdata: any) => {
  return await http.post("api/ess/annoteam/get_all_anno_team_data/", {
    uname: searchdata.uname,
    pname: searchdata.pname,
    begin_time: searchdata.begin_time,
    last_time: searchdata.last_time,
    taskid: searchdata.task_id,
    taskkind: searchdata.task_kind,
    supplier: searchdata.supplier,
  });
};

export const update_anno_task_data = async (
  auth:string,
  id: number,
  tsuname: string,
  tspname: string,
  tswaibao: string,
  tstask_id: string,
  tsdtime: string,
  tskind: string,
  tspnums: number,
  tsknums: string,
  tsptimes: number
) => {
  return await http.post("api/ess/annoteam/update_anno_task_data/", {
    auth:auth,
    id: id,
    tsuname: tsuname,
    tspname: tspname,
    tswaibao: tswaibao,
    tstask_id: tstask_id,
    tsdtime: tsdtime,
    tskind: tskind,
    tspnums: tspnums,
    tsknums: tsknums,
    tsptimes: tsptimes,
  });
};

export const delete_anno_task_data = async (id: number, auth: string) => {
  return await http.post("api/ess/annoteam/delete_anno_task_data/", {
    id: id,
    auth: auth,
  });
};

export const get_anno_team_efficiency = async (
  nbt: string,
  nlt: string,
  lbt: string,
  llt: string
) => {
  return await http.post("api/ess/annoteam/get_anno_team_efficiency/", {
    nbt: nbt,
    nlt: nlt,
    lbt: lbt,
    llt: llt,
  });
};

export const get_anno_team_person_performance = async (
  begin_time: string,
  last_time: string,
  uname: string
) => {
  return await http.post("/api/ess/annoteam/get_anno_team_person/", {
    begin_time: begin_time,
    last_time: last_time,
    uname: uname,
  });
};

export const get_anno_team_task_count = async (
  uname: string,
  kind: string,
  supplier: string,
  begin_time: string,
  last_time: string
) => {
  return await http.post("api/ess/annoteam/get_anno_team_task_count/", {
    uname: uname,
    kind: kind,
    supplier: supplier,
    begin_time: begin_time,
    last_time: last_time,
  });
};
