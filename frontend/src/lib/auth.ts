export function setToken(token: string) {
    localStorage.setItem("pc_token", token);
  }
  
  export function getToken(): string | null {
    return localStorage.getItem("pc_token");
  }
  
  export function clearToken() {
    localStorage.removeItem("pc_token");
  }
  