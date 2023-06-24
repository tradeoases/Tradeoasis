var dropArea = document.querySelectorAll('.drop-area');
if (dropArea && dropArea.length > 0) {
    dropArea.forEach(elem => elem.addEventListener('dragover', event => {
        event.preventDefault();
        elem.classList.add('drag-over');
    }, false))
    dropArea.forEach(elem => elem.addEventListener('dragleave', event => {
        event.preventDefault();
        elem.classList.remove('drag-over');
    }, false))
}
if (document.getElementById("product-images-area") != null) {
    document.getElementById("product-images-area")
        .addEventListener('drop', (event) => {
            event.preventDefault();
            document.getElementById("product-images-area").classList.remove('drag-over');

            var files = event.dataTransfer.files;
            document.getElementById("product-images").files = files;

            // Handle the dropped files here or trigger form submission
            renderSelectedImages()
        }, false);
}

if (document.getElementById("product-videos-area") != null) {
    document.getElementById("product-videos-area")
        .addEventListener('drop', (event) => {
            event.preventDefault();
            document.getElementById("product-videos-area").classList.remove('drag-over');

            var files = event.dataTransfer.files;
            document.getElementById("product-videos").files = files;

            // Handle the dropped files here or trigger form submission
            renderSelectedVideos()
        }, false);
}
if (document.getElementById("product-images") != null) {
    document.getElementById("product-images")
        .addEventListener("change", (event) => renderSelectedImages(event))
}

function renderSelectedImages (event) {
    let imageInput = document.getElementById("product-images");
    let previewContainer = document.querySelector(".selected-images#images")
    // Clear the existing previews
    previewContainer.innerHTML = '';

    // Get the selected files
    const selectedFiles = Array.from(imageInput.files);

    // Iterate over the selected files
    for (let i = 0; i < selectedFiles.length; i++) {
        const file = selectedFiles[i];

        // Create a preview element for each file
        const previewElement = document.createElement('div');
        previewElement.classList.add('preview');

        // Create an image element for the preview
        const imageElement = document.createElement('img');
        imageElement.src = URL.createObjectURL(file);
        imageElement.alt = file.name;

        // Attach a click event handler to unselect the image
        imageElement.addEventListener('click', () => {
            // Remove the file from the selectedFiles array
            const newFiles = selectedFiles.filter(f => f !== file);

            // Create a new FileList object
            const newFileList = new DataTransfer();
            newFiles.forEach(f => newFileList.items.add(f));

            // Set the new FileList object as the input's files
            imageInput.files = newFileList.files;

            // Rebuild the previews
            renderSelectedImages();
        });

        // Append the image element to the preview element
        previewElement.appendChild(imageElement);

        // Append the preview element to the container
        previewContainer.appendChild(previewElement);
    }
}

if (document.getElementById("product-videos") != null) {
document.getElementById("product-videos")
    .addEventListener("change", (event) => renderSelectedVideos(event))
}

function renderSelectedVideos (event) {
    let imageInput = document.getElementById("product-videos");
    let previewContainer = document.querySelector(".selected-images#videos")
    // Clear the existing previews
    previewContainer.innerHTML = '';

    // Get the selected files
    const selectedFiles = Array.from(imageInput.files);

    // Iterate over the selected files
    for (let i = 0; i < selectedFiles.length; i++) {
        const file = selectedFiles[i];

        // Create a preview element for each file
        const previewElement = document.createElement('div');
        previewElement.classList.add('preview');

        // Create an image element for the preview
        const imageElement = document.createElement('video');
        imageElement.src = URL.createObjectURL(file);
        imageElement.alt = file.name;

        // Attach a click event handler to unselect the image
        imageElement.addEventListener('click', () => {
            // Remove the file from the selectedFiles array
            const newFiles = selectedFiles.filter(f => f !== file);

            // Create a new FileList object
            const newFileList = new DataTransfer();
            newFiles.forEach(f => newFileList.items.add(f));

            // Set the new FileList object as the input's files
            imageInput.files = newFileList.files;

            // Rebuild the previews
            renderSelectedVideos();
        });

        // Append the image element to the preview element
        previewElement.appendChild(imageElement);

        // Append the preview element to the container
        previewContainer.appendChild(previewElement);
    }
}

if (document.getElementById("bulk_upload_file_area") != null) {
    document.getElementById("bulk_upload_file_area")
        .addEventListener('drop', (event) => {
            event.preventDefault();
            document.getElementById("bulk_upload_file_area").classList.remove('drag-over');

            var files = event.dataTransfer.files;
            document.getElementById("bulk_upload_file").files = files;
            let previewContainer = document.querySelector(".selected-excel-file#file")
            previewContainer.style.display = "block"
        }, false);
        
    document.getElementById("bulk_upload_file")
        .addEventListener("change", (event) => {
            let previewContainer = document.querySelector(".selected-excel-file#file")
            previewContainer.style.display = "block"
        })
}