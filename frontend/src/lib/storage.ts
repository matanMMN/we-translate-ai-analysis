export function readFromStorage(key: string) {
    return localStorage.getItem(key);
}

export function writeToStorage(key: string, data: string) {
    localStorage.setItem(key, data);
}


export function deleteFromStorage(key: string){
    localStorage.removeItem(key)
}