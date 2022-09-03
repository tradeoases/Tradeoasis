class Modal {
    // Build the template
    static build(product) {
        const template = document.createElement('div');
        template.innerHTML = `
            <div class="modal">
            <div class="modal-head">
                <h2>Edit Product</h2>
                <i class="ti-close" id="close-modal"></i>
            </div>
            <div class="modal-body">
                <div class="edit-form">
                    <form action="">
                        <div class="" style="position:relative;z-index:5;block-size:auto;width:fit-content;">
                            <div
                                style="background-color:#fff;padding:0 .2rem;width:fit-content;block-size:auto;position:absolute;z-index:10;top:1%;left:0%;transform: translate(50%, -50%);">
                                <h3 class="flex" style="margin:0;">Product Details</h3>
                            </div>
                            <div class="product-name-category"
                                style="justify-content:flex-start;block-size:fit-content;border:1px solid rgb(238, 234, 234);border-radius:0;padding:.8rem .6rem;">
                                <div>
                                    <div class="">
                                        <label for="produt-name">Product Name</label>
                                        <input type="text" name="product-name" id="product-name" value="${product.name}">
                                    </div>
                                    <div class="">
                                        <label for="produt-model">Model</label>
                                        <input type="text" name="product-model" id="product-model"
                                            value="${product.model}">
                                    </div>
                                    <div class="">
                                        <label for="produt-serial">Serial Number</label>
                                        <input type="text" name="product-serial" id="product-serial" value="${product.serial}">
                                    </div>
                                    <div class="">
                                        <label for="product-category">Category</label>
                                        <select name="product-category" id="product-category">
                                            <option value="">${product.category}</option>
                                            <option value="">Gadgets</option>
                                            <option value="">Gadgets</option>
                                            <option value="">Gadgets</option>
                                            <option value="">Gadgets</option>
                                        </select>
                                    </div>
                                    <div class="">
                                        <label for="produt-price">Product Price</label>
                                        <input type="text" name="product-price" id="product-price" value="${product.price}">
                                    </div>
                                </div>

                                <div class="" style="margin-top:.8rem;">
                                    <label for="product-description">Description</label>
                                    <textarea name="product-description" id="product-description" cols="30"
                                        rows="10">${product.description}</textarea>
                                </div>
                            </div>
                        </div>
                        <div class="" style="position:relative;z-index:5;block-size:auto;width:100%;margin-top:1.6rem;">
                            <div
                                style="background-color:#fff;padding:0 .2rem;width:fit-content;block-size:auto;position:absolute;z-index:10;top:1%;left:0%;transform: translate(50%, -50%);">
                                <h3 class="flex" style="margin:0;">Product Images</h3>
                            </div>
                            <div class="product-name-category"
                                style="justify-content:flex-start;block-size:fit-content;border:1px solid rgb(238, 234, 234);border-radius:0;padding:.8rem .6rem;width:100%;">
                                <div class="" style="margin-top:.4rem;">
                                    <label for="product-image"></label>
                                    <input type="file" name="product-image" id="product-image">
                                </div>
                            </div>
                        </div>
                        <div class="product-save-cancel flex mt-5" style="margin-top:.8rem;">
                            <div class="">
                                <input type="submit" value="Save" name="btn-create" class="btn">
                            </div>
                            <div class="">
                                <input type="submit" value="Cancel" name="btn-cancel" class="btn">
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <div class="modal-foot">

            </div>
        </div>
        `;
        return template;
    }

    // Display the modal
    static show(product) {
        const modal = this.build(product);
        document.body.appendChild(modal);
    }

    // Remove the modal
    static hide(event) {
        const modal = event.target.parentElement.parentElement.parentElement;
        document.body.removeChild(modal);
    }

}

document.addEventListener("DOMContentLoaded", () => {
    let pageNum = 1;
    let fetchState = {
        "stores_loaded": false,
        "products_loaded": false,
        "contract_loaded": false,
        "buyer_contract_loaded": false,
        "services_loaded": false,
    }

    const BASE_API_URL = 'http://127.0.0.1:8000';
    const BASE_URL = 'http://127.0.0.1:8000';

    const fetchData = async (url, has_page_num = true) => {
        let response;
        if (has_page_num) {
            response = await fetch(
                `${BASE_API_URL}/${url}/?page=${pageNum}`, {
                method: "GET",
                mode: "same-origin",
                cache: "no-cache",
                credentials: 'same-origin'
            });
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
            if (response.count / 10 > pageNum) {
                pageNum = pageNum + 1;
                invoker();
            }
        })

        document.querySelector('.table-pagination #previous-page').addEventListener('click', () => {
            if (pageNum > 1) {
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

        let response = await fetchData(url = 'api/stores');

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
                    // if (!isClientModalOpen) {
                    //     // fetch client data
                    //     // open modal
                    //     fetchData(`product/${record.slug}`, has_page_num=false)
                    //     .then(response => openProductModal(response));                        
                    // }

                    tableRow.addEventListener('click', (e) => {
                        // Retrieve data for this row
                        // and construct the object to pass to the modal

                        const id = tableRow.querySelectorAll('td')[0].textContent;
                        const serial = tableRow.querySelectorAll('td')[1].textContent;
                        const name = tableRow.querySelectorAll('td')[2].textContent;
                        const description = tableRow.querySelectorAll('td')[3].textContent;

                        const obj = { id, serial, name, description };

                        // Open Modal
                        Modal.show(obj);

                        // Close Modal
                        document.querySelector('#close-modal').addEventListener('click', (event) => {
                            if (event.target.classList.contains('ti-close'))
                                Modal.hide(event);
                        });
                    })
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

        let response = await fetchData(url = 'api/products');

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
                        fetchData(`product/${record.slug}`, has_page_num = false)
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

        let response = await fetchData(url = 'api/contracts');

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

        let response = await fetchData(url = 'api/services');
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
                    <td>${record.description.slice(0, 150)} ...</td>
                    <td>${record.currency} ${record.price}</td>
                    <td>${record.created_on}</td>
                    <td style="display:grid; justify-content:center;align-items:center;"><a href="${BASE_URL}/suppliers/dashboard/contractsdetails/${record.id}"><i class="fa fa-info-circle"></i></a></td>
                `;
                tableBody.appendChild(tableRow);
                tableRow.addEventListener('click', async () => {
                    if (!isClientModalOpen) {
                        // fetch client data
                        // open modal
                        fetchData(`product/${record.slug}`, has_page_num = false)
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

        let response = await fetchData(url = 'api/contracts');

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


if (window.innerWidth < 800) {
    if (window.location.href.includes('/admin/') || window.location.href.includes('dashboard')) {
        let domain = full = location.protocol + '//' + location.host
        window.location.replace(`${domain}/blocked`);
    }
}