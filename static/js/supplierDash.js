document.addEventListener("DOMContentLoaded", () => {
    let pageNum = 1;
    let fetchState = {
        "stores_loaded": false,
        "products_loaded": false,
        "contract_loaded": false,
        "buyer_contract_loaded": false,
        "services_loaded": false,
    }

    const BASE_API_URL = 'http://localhost:8000';
    const BASE_URL = 'http://localhost:8000';

    const fetchData = async (url, has_page_num=true) => {
        let response;
        if (has_page_num) {
            response = await fetch(`${BASE_API_URL}/${url}/?page=${pageNum}`);
        }
        else {
            response = await fetch(`${BASE_API_URL}/${url}`);
        }
        if (response.ok) {
            const data = await response.json();
            return data;
        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    const paginate = (response, invoker) => {
        document.querySelector('.table-pagination #next-page').addEventListener('click', () => {
            if (response.count / 10 > pageNum)
            {
                pageNum = pageNum + 1;
                invoker();
            }
        })

        document.querySelector('.table-pagination #previous-page').addEventListener('click', () => {
            if (pageNum > 1)
            {
                pageNum--;
                invoker();
            }
        })
        document.querySelector('.table-pagination #current-page').textContent = pageNum;
        document.querySelector('.table-pagination #current-page-0').textContent = pageNum;
        document.querySelector('.table-pagination #max-page').textContent = Math.ceil(response.count / 10);
    }


    // STORES
    const renderStores = async () => {
        if (!fetchState["stores_loaded"]) {
            pageNum = 1;
            fetchState["stores_loaded"] = true;
        }

        let response = await fetchData(url='api/stores');

        const tableBody = document.querySelector('table#stores tbody');

        if (tableBody.childNodes.length > 0) {
            while (tableBody.firstChild) {
                tableBody.removeChild(tableBody.firstChild);
            }

            document.querySelector('#table-item-count').textContent = response.count;
    
            response.results.forEach((record, i) => {
                let tableRow = document.createElement('tr')
                tableRow.setAttribute('data-slug', record.slug);
                tableRow.setAttribute('data-id', record.id);
                tableRow.innerHTML = `
                    <td>${i + 1}</td>
                    <td>${record.name}</td>
                    <td>${record.products}</td>
                    <td>${record.created_on}</td>
                `;
                tableBody.appendChild(tableRow);
                tableRow.addEventListener('click', async () => {
                    if (!isClientModalOpen) {
                        // fetch client data
                        // open modal
                        fetchData(`product/${record.slug}`, has_page_num=false)
                        .then(response => openProductModal(response));                        
                    }
                })
            })
        }

        // change page number
        paginate(response, invoker = renderStores)
    }

    const storesTable = document.querySelector("table#stores");
    if (storesTable) {
        renderStores();
    }
    // STORES

    // PRODUCTS
    const renderProducts = async () => {
        if (!fetchState["products_loaded"]) {
            pageNum = 1;
            fetchState["products_loaded"] = true;
        }

        let response = await fetchData(url='api/products');

        const tableBody = document.querySelector('table#products tbody');

        if (tableBody.childNodes.length > 0) {
            while (tableBody.firstChild) {
                tableBody.removeChild(tableBody.firstChild);
            }

            document.querySelector('#table-item-count').textContent = response.count;
    
            response.results.forEach((record, i) => {
                let tableRow = document.createElement('tr')
                tableRow.setAttribute('data-slug', record.slug);
                tableRow.setAttribute('data-id', record.id);
                tableRow.innerHTML = `
                    <td>${i + 1}</td>
                    <td>${record.name}</td>
                    <td>${record.sub_category.category.name}</td>
                    <td>${record.sub_category.name}</td>
                    <td>${record.currency} ${record.price}</td>
                    <td>${record.created_on}</td>
                    <td>0</td>
                `;
                tableBody.appendChild(tableRow);
                tableRow.addEventListener('click', async () => {
                    if (!isClientModalOpen) {
                        // fetch client data
                        // open modal
                        fetchData(`product/${record.slug}`, has_page_num=false)
                        .then(response => openProductModal(response));                        
                    }
                })
            })
        }

        // change page number
        paginate(response, invoker = renderProducts)
    }

    const productsTable = document.querySelector("table#products");
    if (productsTable) {
        renderProducts();
    }
    // PRODUCTS

    // CONTRACTS
    const renderContracts = async () => {
        if (!fetchState["contract_loaded"]) {
            pageNum = 1;
            fetchState["contract_loaded"] = true;
        }

        let response = await fetchData(url='api/contracts');

        const tableBody = document.querySelector('table#contracts tbody');

        if (tableBody.childNodes.length > 0) {
            while (tableBody.firstChild) {
                tableBody.removeChild(tableBody.firstChild);
            }

            document.querySelector('#table-item-count').textContent = response.count;
    
            response.results.forEach((record, i) => {
                let tableRow = document.createElement('tr')
                tableRow.setAttribute('data-id', record.id);
                tableRow.innerHTML = `
                    <td>${i + 1}</td>
                    <td>${record.service.name}</td>
                    <td>${record.buyer.username}</td>
                    <td>${record.created_on}</td>
                    <td style="display:grid; justify-content:center;align-items:center;"><a href="${BASE_URL}/suppliers/dashboard/contractsdetails/${record.id}"><i class="fa fa-info-circle"></i></a></td>
                `;
                tableBody.appendChild(tableRow);
            })
        }

        // change page number
        paginate(response, invoker = renderContracts)
    }

    const contractsTable = document.querySelector("table#contracts");
    if (contractsTable) {
        renderContracts();
    }
    // CONTRACTS

    // SERVICES
    const renderServices = async () => {
        if (!fetchState["services_loaded"]) {
            pageNum = 1;
            fetchState["services_loaded"] = true;
        }

        let response = await fetchData(url='api/services');
        console.log(response)

        const tableBody = document.querySelector('table#services tbody');

        if (tableBody.childNodes.length > 0) {
            while (tableBody.firstChild) {
                tableBody.removeChild(tableBody.firstChild);
            }

            document.querySelector('#table-item-count').textContent = response.count;
    
            response.results.forEach((record, i) => {
                let tableRow = document.createElement('tr')
                tableRow.setAttribute('data-id', record.id);
                tableRow.innerHTML = `
                    <td>${i + 1}</td>
                    <td>${record.name}</td>
                    <td>${record.description.slice(0,150)} ...</td>
                    <td>${record.currency} ${record.price}</td>
                    <td>${record.created_on}</td>
                    <td style="display:grid; justify-content:center;align-items:center;"><a href="${BASE_URL}/suppliers/dashboard/contractsdetails/${record.id}"><i class="fa fa-info-circle"></i></a></td>
                `;
                tableBody.appendChild(tableRow);
                tableRow.addEventListener('click', async () => {
                    if (!isClientModalOpen) {
                        // fetch client data
                        // open modal
                        fetchData(`product/${record.slug}`, has_page_num=false)
                        .then(response => openProductModal(response));                        
                    }
                })
            })
        }

        // change page number
        paginate(response, invoker = renderServices)
    }

    const servicesTable = document.querySelector("table#services");
    if (servicesTable) {
        renderServices();
    }
    // SERVICES

    // BUYER CONTRACTS
    const renderBuyerContracts = async () => {
        if (!fetchState["buyer_contract_loaded"]) {
            pageNum = 1;
            fetchState["buyer_contract_loaded"] = true;
        }

        let response = await fetchData(url='api/contracts');

        const tableBody = document.querySelector('table#buyer-contracts tbody');

        if (tableBody.childNodes.length > 0) {
            while (tableBody.firstChild) {
                tableBody.removeChild(tableBody.firstChild);
            }

            document.querySelector('#table-item-count').textContent = response.count;
    
            response.results.forEach((record, i) => {
                let tableRow = document.createElement('tr')
                tableRow.setAttribute('data-id', record.id);
                tableRow.innerHTML = `
                    <td>${i + 1}</td>
                    <td>${record.service.name}</td>
                    <td>${record.supplier.username}</td>
                    <td>${record.created_on}</td>
                    <td style="display:grid; justify-content:center;align-items:center;"><a href="${BASE_URL}/buyer/dashboard/contractsdetails/${record.id}"><i class="fa fa-info-circle"></i></a></td>
                `;
                tableBody.appendChild(tableRow);
            })
        }

        // change page number
        paginate(response, invoker = renderBuyerContracts)
    }

    const buyerContractsTable = document.querySelector("table#buyer-contracts");
    if (buyerContractsTable) {
        renderBuyerContracts();
    }
    // BUYER CONTRACTS
});


if(window.innerWidth < 800)
{
    if (window.location.href.includes('/admin/') || window.location.href.includes('dashboard')) {
        let domain = full = location.protocol + '//' + location.host
        window.location.replace(`${domain}/blocked`);
    }
}