const API = {
    // Backend URI
    BACKEND_BASE_API_URI : window.location.hostname === 'localhost' ? 'http://localhost:5000/api/v1' : 'https://foroden.com/en/api/v1/',


    // Get requests
    makeGetRequest: async (endpoint) => {
        try {
            const response = await fetch(endpoint);
            return await response.json(); 
        } catch (error) {
            console.log(error);
            throw new Error("Failed to make the GET request.");
        }
    },

    // Post requests
    makePostRequest: async (endpoint, data, fromFormData=false) => {
        try {
            let response;
            if(fromFormData){
                response = await fetch(endpoint, {
                    method: "POST",
                    body: data
                });
            }else{
                response = await fetch(endpoint, {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
            }
            return await response.json();
        } catch (error) {
            console.log(error);
            throw new Error("Failed to make the POST request.");
        }
    },

    // Patch requests
    makePatchRequest: async (endpoint, data, fromFormData=false) => {
        try {
            let response;
            if(fromFormData){
                response = await fetch(endpoint, {
                    method: "PATCH",
                    body: data
                });
            }else{
                response = await fetch(endpoint, {
                    method: "PATCH",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
            }
            return await response.json();
        } catch (error) {
            console.log(error);
            throw new Error("Failed to make the PATCH request.");
        }
    },

    // Delete requests
    makeDeleteRequest: async (endpoint, data, fromFormData=false) => {
        try {
            let response;
            if(fromFormData){
                response = await fetch(endpoint, {
                    method: "DELETE",
                    body: data
                });
            }else{
                response = await fetch(endpoint, {
                    method: "DELETE",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
            }
            return await response.json();
        } catch (error) {
            console.log(error);
            throw new Error("Failed to make the DELETE request.");
        }
    },

    // Invoices 
    invoices: {
        // Fetch single invoice GET api/v1/invoices/fetch/:id
        fetchSingle: async (id) => {
            const endpoint = `${API.BACKEND_BASE_API_URI}/invoices/fetch/${id}`;
            return await API.makeGetRequest(endpoint);
        },

        // Fetch all invoices GET api/v1/invoices/fetch
        fetchAll: async () => {
            const endpoint = `${API.BACKEND_BASE_API_URI}/invoices/fetch/all`;
            return await API.makeGetRequest(endpoint);
        },

        // Update invoice PATCH api/v1/invoices/update/
        update: async (id) => {
            const endpoint = `${API.BACKEND_BASE_API_URI}/invoices/update`;
            return await API.makePatchRequest(endpoint, id);
        },

        // Delete invoice DELETE api/v1/invoices/delete
        delete: async (id) => {
            const endpoint = `${API.BACKEND_BASE_API_URI}/invoices/delete`;
            return await API.makeDeleteRequest(endpoint, id);
        },
    } 


}