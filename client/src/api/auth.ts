import http from "@/utils/axios";

export const regist = async (username: string, zhuname: string, email: string, password: string) => {
  return await http.post("api/ess/auth/regist/", { username: username, zhuname: zhuname, email: email, password: password });
};

export const login = async (user: string, pwd: string, is_ldap_login: boolean, zhuname?: string) => {
  if (is_ldap_login) {
    return await http.post("api/ess/auth/login/", { user: user, pwd: pwd, is_ldap_login: is_ldap_login, zhuname: zhuname});
  }
  else {
    return await http.post("api/ess/auth/login/", { user: user, pwd: pwd, is_ldap_login: is_ldap_login});
  }
}


export const updatepwd = async (username: string, password: string) => {
  return await http.post("api/ess/auth/changepwd/", { username: username, password: password });
}

export const updateuserimg = async (username: string, imgurl: string) => {
  return await http.post("api/ess/auth/changeuserimg/", { username: username, imgurl: imgurl });
}

export const get_user_info = async (username: string) => {
  return await http.post("api/ess/auth/get_user_info/", { username: username });
};