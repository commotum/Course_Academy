const API_BASE_URL = '/api';

// class API {
//     constructor() {
//         this.xhr = this.createXHR();
//         this.requestQueue = [];
//         this.requestTimeout = 20000;
//         this.routes = {};
//     }

//     createXHR() {
//         let xhr;

//         try {
//             xhr = new XMLHttpRequest();
//         } catch (e) {
//             xhr = new ActiveXObject('Microsoft.XMLHTTP');
//         }

//         return xhr;
//     }

//     send(method, url, data, callback) {
//         const request = {
//             method: method,
//             url: url,
//             data: data,
//             callback: callback
//         };

//         this.requestQueue.push(request);

//         if (!this.xhr.readyState || this.xhr.readyState == 4) { // Uninitialized or Complete
//             this.processNextRequest();
//         }
//     }

//     processNextRequest() {
//         try {
//             if (this.requestQueue.length > 0) {
//                 const request = this.requestQueue[0];

//                 if (request.isProcessing) { return; }

//                 request.isProcessing = true;

//                 this.xhr.open(request.method, request.url, true);


//                 const verb = request.method
//                 const contentMD5 = CryptoJS.MD5(body).toString(CryptoJS.enc.Hex);
//                 const contentType = 'application/json';
//                 const timestamp = Math.floor(Date.now() / 1000);
//                 const requestURI = `/api/party`;
//                 const nonce = crypto.randomBytes(16).toString('base64');

//                 const headers = {
//                     'Accept': 'application/json',
//                     'Content-Type': contentType,
//                     'Strict-Transport-Security': "max-age=31536000",
//                     'Public-API-Key': publicKey,
//                     'Authorization': `TXC-HMAC-SHA256 ${publicKey}:${signature}`,
//                     'X-TXC-Nonce': nonce,
//                     'X-TXC-Timestamp': timestamp
//                 };

//                 this.xhr.onloadend = () => {
//                     if (this.xhr.status === 404) {
//                         request.callback(null, {
//                             type: 'SessionTimeout',
//                             message: "Oops, it looks like your session may have timed out. Please log back into to resume."
//                         });
//                     }
//                 }

//                 this.xhr.onreadystatechange = this.processStateChange.bind(this);

//                 if (request.method == 'GET') {
//                     this.xhr.send(null);
//                 } else if (request.method == 'POST') {
//                     const body = JSON.stringify(request.data);

//                     const signature = this.generateSignature(secretKey, verb, contentMD5, contentType, timestamp, requestURI, nonce);

//                     if (typeof(request.data) == 'object') {
//                         this.xhr.setRequestHeader("Content-Type", "application/json");
//                         this.xhr.send(JSON.stringify(request.data));
//                     } else {
//                         this.xhr.send(request.data);
//                     }
//                 }
//             }
//         } catch(e) {
//             setTimeout(this.processNextRequest.bind(this), 10);
//         }
//     }

//     processStateChange() {
//         if (this.xhr.readyState == 4) { // Complete
//             if (this.xhr.status == 200) {

//                 if (this.timerID) {
//                     clearTimeout(this.timerID);
//                     delete this.timerID;
//                 }

//                 const request = this.requestQueue.shift();;

//                 if (request.callback != null) {
//                     const responseText = this.trim(this.xhr.responseText);

//                     const response = eval('(' + responseText + ')');
//                     request.callback(null, response);
//                 }

//                 // Avoid memory leak in MSIE: clean up the onComplete event handler
//                 this.xhr.onreadystatechange = function() {};

//                 // Must not reenter Ajax. Schedule next request in 10ms
//                 setTimeout(this.processNextRequest.bind(this), 10);

//             } else {
//                 const request = this.requestQueue.shift();
//                 request.callback({
//                     type: 'ConnectionError',
//                     message: "Oops, it looks like there was a network error. Please check your internet connection."
//                 }, null);

//                 setTimeout(this.processNextRequest.bind(this), 10);
//             }
//         }
//     }

//     _get(url, key, callback) {
//         this.send('GET', url, key, null, callback);
//     }

//     async get(url) {
//         const key = await this.getKey();
//         return new Promise((resolve, reject) => {
//             this._get(url, (error, response) => {
//                 if (error) {
//                     reject(error);
//                 } else {
//                     resolve(response);
//                 }
//             });
//         });
//     }

//     _post(url, data, key, callback) {
//         this.send('GET', url, key, data, callback);
//     }

//     async post(url, data) {
//         const key = await this.getKey();
//         return new Promise((resolve, reject) => {
//             this._post(url, data, key, (error, response) => {
//                 if (error) {
//                     reject(error);
//                 } else {
//                     resolve(response);
//                 }
//             });
//         });
//     }
    
//     async getKey() {
//         const key = await this.get('/api/getKey');
//         return key;
//     }

//     trim(input) {
//         return input.replace(/^\s*|\s*$/g, ''); // Trim whitespace to prevent obfuscation
//     }

//     resetRoutes() {
//         this.routes = {};
//     }

//     addRoute(func, screen) {
//         this.routes[screen] = func.bind(this);
//     }
// }

// const api = new API();

let api = {
    _get: (url, callback) => {
        Core.get(url, (error, response) => {
            callback(error, response);
        });
    },
    _post: (url, data, callback) => {
        data = data ? data : {};

        Core.post(url, data, (error, response) => {
            if (callback && typeof callback === "function") {
                callback(error, response);
            }
        });
    },    
};

api.get = async (url) => {
    return new Promise((resolve, reject) => {
        api._get(url, (error, response) => {
            if (error) {
                resolve(null);
            } else {
                resolve(response);
            }
        });
    });
};

api.post = async (url, data) => {
    return new Promise((resolve, reject) => {
        api._post(url, data, (error, response) => {
            if (error) {
                resolve(null);
            } else {
                resolve(response);
            }
        });
    });
};