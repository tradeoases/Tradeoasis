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
    if (nav.dataset['page'] === 'client') {
        const clientRoutes = ["client-overview", "client-suppliers","client-buyers", "client-contracts","client-products","client-suppliers-overview","client-buyers-overview", "client-contracts-overview","client-products-overview"];
        
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

        clientModalCloseActivator.addEventListener('click', () => {
            closeClientModel()
        })

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


        productModalCloseActivator.addEventListener('click', () => {
            closeProductModel()
        })


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

        contractModalCloseActivator.addEventListener('click', () => {
            closecontractModel()
        })

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

    }
    
    // client page


    // manager page

        // client page
        if (nav.dataset['page'] === 'manager') {
            const clientRoutes = ["manager-overview", "manager-showroom","manager-services","manager-products","manager-showroom-overview","manager-services-overview",];
            
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
});