document.addEventListener('DOMContentLoaded', () => {
    const imgMagnifier = document.querySelector('.img-magnifier');
    const productImagesContainer = document.querySelector('.product-images-list');

    if ((imgMagnifier && imgMagnifier != null) && (productImagesContainer && productImagesContainer != null)) {
        
        const productImgs = productImagesContainer.querySelectorAll('img');
        let activeImg = productImgs[0];
        activeImg.classList.add('active');
        
        // set initial image
        let mainImg = imgMagnifier.querySelector('img');
        mainImg.src = activeImg.src;

        productImgs.forEach(img => img.addEventListener('click', () => {
            activeImg.classList.remove('active');
            activeImg = img;
            mainImg.src = activeImg.src;
            activeImg.classList.add('active');
        }));

        // magnify product image
        imgMagnifier.addEventListener('mouseenter', (e) => {
            
            // // scale up image
            // mainImg.style.transform = 'scale(1.2)';

            // // move image
            // mainImg.style.transform = `translate(${-(e.clientX /e.clientX) +10 }px, ${-e.clientY}px)`
        })
    }

})