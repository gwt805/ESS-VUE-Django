import http from "@/utils/axios";

export const add_cronjob = async (weekday: number, hour: number, minute: number, second: number) => {
    return await http.post("api/ess/cronjob/add_cronjob/", {weekday: weekday, hour: hour, minute: minute, second: second})
};

export const get_cronjob = async () => {
    return await http.post("api/ess/cronjob/get_cronjob/");
};
export const get_cronjob_log = async () => {
    return await http.post("api/ess/cronjob/get_cronjob_log/");
};

export const del_cronjob = async (id: number) => {
    return await http.post("api/ess/cronjob/del_cronjob/", { id: id });
};