document.addEventListener('DOMContentLoaded', () => {
    // state
    const clientModal = document.querySelector("#client-modal");
    const clientModalCloseActivator = document.querySelector('#client-modal-deactivator');
    let isClientModalOpen = false;

    const productModal = document.querySelector("#product-modal");
    const productModalCloseActivator = document.querySelector('#product-modal-deactivator');
    let isProductModalOpen = false;


    const contractModal = document.querySelector("#contract-modal");
    const contractModalCloseActivator = document.querySelector('#contract-modal-deactivator');
    let isContractModalOpen = false;

    const operationConfirmModal = document.querySelector("#operation-confirm-modal");
    let isOperationConfirmModal = false;

    const serviceModal = document.querySelector("#manager-service-modal");
    const serviceModalCloseActivator = document.querySelector("#manager-service-modal-deactivator");
    let isServiceModalOpen = false;


    // track active tabs
    let activeTab = null;

    // utils
    // requests
    const fetchData = async () => {
        
    }
    // requests
    
    
    
    // detect page
    const nav = document.querySelector('nav[data-page]');
    
    // client page
    // if (nav && nav.dataset['page'] === 'client') {
        const clientRoutes = ["client-overview", "client-suppliers","client-buyers", "client-contracts","client-products","client-suppliers-overview","client-buyers-overview", "client-contracts-overview","client-products-overview"];
        
        // SWITCHING TABS
        activeTab = clientRoutes[0];
        
        clientRoutes.forEach(route => {
            const activator = document.querySelector(`#${route}-activator`);
            const section = document.querySelector(`#${route.split('-').slice(0,2).join('-')}-section`);

            if (route === activeTab) {
                try {
                    activator.classList.add('active');
                    section.classList.remove('cs-hidden');
                    section.classList.add('cs-grid');
                } catch (e)  {

                }
            }

            if(activator) {
                activator.addEventListener('click', () => {
                    if (activator.id != `${activeTab}-activator`) {
                        
                        // change active tab state
                        document.querySelector(`#${activeTab}-activator`).classList.remove('active');
                        document.querySelector(`#${activeTab}-section`).classList.remove('cs-grid');
                        document.querySelector(`#${activeTab}-section`).classList.add('cs-hidden');

                        section.classList.remove('cs-hidden');
                        section.classList.add('cs-grid');
                        
                        activeTab = activator.id.split('-').slice(0,2).join('-');                    
                        document.querySelector(`#${activeTab}-activator`).classList.add('active');

                        // fetch data
                    }
                });
            }
        });

        // SWITCHING TABS
        
        // CLIENT MODAL
        const clientItems = document.querySelectorAll('.client-item'); 
        const closeClientModel = () => {
            clientModal.classList.remove('cs-grid');
            clientModal.classList.add('cs-hidden');
            isClientModalOpen = false;
            document.body.classList.remove('modal-open');
        }
        
        const openClientModal = () => {
            document.body.classList.add('modal-open');
            clientModal.classList.remove('cs-hidden');
            clientModal.classList.add('cs-grid');
            isClientModalOpen = true;

            if (isClientModalOpen) {
                clientModal.querySelector('#suspend-btn').addEventListener('click', (e) => openOperationConfirmModal(msg='Are you sure you want to suspend client account.', postUrl='test/', data={"id": e.target.dataset['userid']}))
            }
        }

        if (clientModalCloseActivator) {
            clientModalCloseActivator.addEventListener('click', () => {
                closeClientModel()
            })
        }

        document.body.addEventListener('click', (e) => {
            // if (!isClientModalOpen && e.target != clientModal && !(e.target.localName == 'td' || e.target.classList.contains('client-item')) && !(e.target == clientModal)) {
            //     closeClientModel()
            // }

            if (!isClientModalOpen && !isProductModalOpen) {

            }

        });

        // client selected
        if (clientItems && clientItems != undefined) {
            clientItems.forEach(item => {
                item.addEventListener('click', async () => {
                    if (!isClientModalOpen) {
                        // fetch client data
                        // open modal
                        let client = await fetchData();
                        openClientModal(client);
                    }
                })  
            })
        }
        // CLIENT MODAL


        // PRODUCT MODAL
        const productItems = document.querySelectorAll('.product-item');

        const closeProductModel = () => {
            productModal.classList.remove('cs-grid');
            productModal.classList.add('cs-hidden');
            isProductModalOpen = false;
            document.body.classList.remove('modal-open');
        }
        
        const openProductModal = () => {
            document.body.classList.add('modal-open');
            productModal.classList.remove('cs-hidden');
            productModal.classList.add('cs-grid');
            isProductModalOpen = true;


            if (isProductModalOpen) {
                productModal.querySelector('#suspend-btn').addEventListener('click', (e) => openOperationConfirmModal(msg='Are you sure you want to suspend product.', postUrl='test/', data={"id": e.target.dataset['productid']}))
            }
        }

        if (productModalCloseActivator) {
            productModalCloseActivator.addEventListener('click', () => {
                closeProductModel()
            })
        }

        if (productItems && productItems != undefined) {
            productItems.forEach(item => {
                item.addEventListener('click', async () => {
                    if (!isProductModalOpen) {
                        // fetch client data
                        // open modal
                        let client = await fetchData();
                        openProductModal(client);
                    }
                })  
            })
        }
        // PRODUCT MODAL

        // CONTRACT MODAL
        const contractItems = document.querySelectorAll('.contract-item');

        const closecontractModel = () => {
            contractModal.classList.remove('cs-grid');
            contractModal.classList.add('cs-hidden');
            isContractModalOpen = false;
            document.body.classList.remove('modal-open');
        }
        
        const openContractModal = () => {
            document.body.classList.add('modal-open');
            contractModal.classList.remove('cs-hidden');
            contractModal.classList.add('cs-grid');
            isContractModalOpen = true;

            if (isContractModalOpen) {
                contractModal.querySelector('#suspend-btn').addEventListener('click', (e) => openOperationConfirmModal(msg='Are you sure you want to suspend contract.', postUrl='test/', data={"id": e.target.dataset['contractid']}))
            }
        }

        if (contractModalCloseActivator) {
            contractModalCloseActivator.addEventListener('click', () => {
                closecontractModel()
            })
        }

        if (contractItems && contractItems != undefined) {
            contractItems.forEach(item => {
                item.addEventListener('click', async () => {
                    if (!isContractModalOpen) {
                        // fetch client data
                        // open modal
                        let client = await fetchData();
                        openContractModal(client);
                    }
                })  
            })
        }
        // CONTRACT MODAL

    // }
    
    // client page


    // manager page

        // client page
        if (nav && nav.dataset['page'] === 'manager') {
            const clientRoutes = ["manager-overview", "manager-showroom","manager-services", "manager-memberships","manager-showroom-overview","manager-services-overview","manager-memberships-overview"];
            
            // SWITCHING TABS
            activeTab = clientRoutes[0];
            
            clientRoutes.forEach(route => {
                const activator = document.querySelector(`#${route}-activator`);
                const section = document.querySelector(`#${route.split('-').slice(0,2).join('-')}-section`);
    
                if (route === activeTab) {
                    activator.classList.add('active');
                    section.classList.remove('cs-hidden');
                    section.classList.add('cs-grid');
                }
    
                if(activator) {
                    activator.addEventListener('click', () => {
                        if (activator.id != `${activeTab}-activator`) {
                            
                            // change active tab state
                            document.querySelector(`#${activeTab}-activator`).classList.remove('active');
                            document.querySelector(`#${activeTab}-section`).classList.remove('cs-grid');
                            document.querySelector(`#${activeTab}-section`).classList.add('cs-hidden');
    
                            section.classList.remove('cs-hidden');
                            section.classList.add('cs-grid');
                            
                            activeTab = activator.id.split('-').slice(0,2).join('-');                    
                            document.querySelector(`#${activeTab}-activator`).classList.add('active');
    
                            // fetch data
                        }
                    });
                }
            });
    
            // SWITCHING TABS
            
            const closeServiceModel = () => {
                serviceModal.classList.remove('cs-grid');
                serviceModal.classList.add('cs-hidden');
                isServiceModalOpen = false;
                document.body.classList.remove('modal-open');
            }
            serviceModalCloseActivator.addEventListener('click', () => closeServiceModel());

            const openServiceModel = async (id) => {
                // fetch
                data = await fetchData();

                document.body.classList.add('modal-open');
                serviceModal.classList.remove('cs-hidden');
                serviceModal.classList.add('cs-grid');
                isServiceModalOpen = true;

                if (isServiceModalOpen) {
                    serviceModal.querySelector('#suspend-btn').addEventListener('click', (e) => {
                        openOperationConfirmModal(msg='Are you sure you want to delete this service.', postUrl='test/', data={"id": e.target.dataset['serviceid']})
                    })
                }
            }

            const serviceItems = document.querySelectorAll('.manager-service-item');
            serviceItems.forEach(item => {
                item.addEventListener('click', (e) => {
                    if (!isServiceModalOpen) {
                        openServiceModel(id = e.target.dataset['itemid']);
                    }
                })
            })
        }    

    // manager page


    // CONFIRM MODAL
    const openOperationConfirmModal = (msg, postUrl, data) => {
        operationConfirmModal.querySelector('#confirm-msg').textContent = msg;
        operationConfirmModal.querySelector('form').action = postUrl;

        document.body.classList.add('modal-open');
        operationConfirmModal.classList.remove('cs-hidden');
        operationConfirmModal.classList.add('cs-grid');
        isOperationConfirmModal = true;

        if (operationConfirmModal) {
            operationConfirmModal.querySelector('#cancel-operation').addEventListener('click', () => {
                operationConfirmModal.classList.add('cs-hidden');
                operationConfirmModal.classList.remove('cs-grid');
                isOperationConfirmModal = false;
            })

            operationConfirmModal.querySelector('form').addEventListener('click', (e) => {
                e.preventDefault();
            })
        }
    }
    // CONFIRM MODAL

    document.querySelectorAll('table td:not(.delete)').forEach(cell => {
        const MAXWORDCOUNT = 13;
        if (cell.textContent.split(" ").length > MAXWORDCOUNT) {
            cell.textContent = `${cell.textContent.split(" ").slice(0, MAXWORDCOUNT).join(" ")} ....`
        }
    })

    const handleAddInput = (target, subCategoryCount, subCategoryGroup, lastAddElem) => {
        // remove add btn
        lastAddElem.removeChild(target)
        const deleteInputBtn = lastAddElem.querySelector('.delete-input');

        // add delete btn
        deleteInputBtn.classList.remove('cs-hidden');
        deleteInputBtn.classList.add('cs-grid');

        // handle delete inputs
        deleteInputBtn.addEventListener('click', (e) => {
            console.log(subCategoryCount)
            subCategoryGroup.removeChild(subCategoryGroup.querySelector(`.subcategory-inputs[data-subcategorycount="${subCategoryCount}"]`));
        })

        // create form element
        const subCategoryElem = document.createElement('div');
        subCategoryElem.classList.add(...['cs-grid', 'cs-align-center', 'subcategory-inputs']);

        subCategoryElem.innerHTML = `
            <input type="text" name='subcategory-${subCategoryCount + 1}' id="subcategory-${subCategoryCount + 1}" placeholder="Sub Category Name" required>
            <input type="file" name="sub-category-image-${subCategoryCount + 1}" id="sub-category-image-${subCategoryCount + 1}" required>
            <button class="btn cs-grid cs-justify-center cs-align-center cs-bg-hover-color cs-text-secondary br-full" id="add-input" style="padding: 1rem .5rem;" onclick="(function(){
            })();return false;">
                <i class="fa fa-plus"></i>
            </button>

            <button class="btn cs-justify-center cs-align-center cs-bg-hover-color cs-text-secondary br-full cs-hidden delete-input" data-subcategoryDeleteCcount="${subCategoryCount + 1}" style="padding: 1rem .5rem;" onclick="(function(){
            })();return false;">
                <i class="fa fa-trash"></i>
            </button>
        `
        let _subCategoryCount = subCategoryCount + 1;
        
        subCategoryElem.dataset['subcategorycount'] = _subCategoryCount;
        subCategoryGroup.appendChild(subCategoryElem);

        lastAddElem = subCategoryElem;

        const addInputBtn = lastAddElem.querySelector('#add-input');
        addInputBtn.addEventListener('click', () => handleAddInput(addInputBtn, _subCategoryCount, subCategoryGroup, lastAddElem));
    }

    // add form inputs
    const categoryForm = document.querySelector('#category-form');
    if (categoryForm && categoryForm != undefined) {
        let subCategoryCount = 1;
        const subCategoryGroup = document.querySelector('#subCategory-group');
        let lastAddElem = document.querySelector(`.subcategory-inputs[data-subcategorycount="1"]`)


        const addInputBtn = lastAddElem.querySelector('#add-input');
        addInputBtn.addEventListener('click', () => handleAddInput(addInputBtn, subCategoryCount, subCategoryGroup, lastAddElem));
    }

    // active tba should not reload page
    document.querySelectorAll('a').forEach(tab => {
        tab.addEventListener('click', (e) => {
            console.log(e.target.classList)
            if ((e.target.classList.contains('active') && !e.target.classList.contains('manager')) || (e.target.parentNode.classList.contains('active') && !e.target.parentNode.classList.contains('manager'))) {
                e.preventDefault();
            }
        })
    })

    // notification popup
    const notificationCta = document.querySelector('.notification-cta');
    const notificationPopup =  document.querySelector('.notification-list')
    notificationCta.addEventListener('click', () => {
        notificationPopup.classList.toggle('cs-hidden');
        notificationPopup.classList.toggle('cs-grid');
    });

    const navEmphCta = document.querySelector('#nav-emph-cta');
    if (navEmphCta) {
        navEmphCta.addEventListener('click', () => {
            const ctaEmph = document.querySelector('.cta-emph');
            ctaEmph.classList.toggle('cs-hidden');
            ctaEmph.classList.toggle('cs-grid');
        });
    }
});