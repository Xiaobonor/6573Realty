// app/static/property_management/rental/script.js
const collapsibleHeaders = document.querySelectorAll('.collapsible .collapsible-header');
collapsibleHeaders.forEach(header => {
    header.addEventListener('click', () => {
        const content = header.nextElementSibling;
        const icon = header.querySelector('i');
        if (content.style.display === 'block') {
            content.style.display = 'none';
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
        } else {
            content.style.display = 'block';
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-up');
        }
    });
});

let currentImageIndex = 0;
let imageFiles = [];

document.getElementById('images').addEventListener('change', function (event) {
    imageFiles = Array.from(event.target.files);
    if (imageFiles.length > 0) {
        displayImage(0);
    }
});

function displayImage(index) {
    const reader = new FileReader();
    reader.onload = function (e) {
        const imgElement = document.getElementById('current-image');
        imgElement.src = e.target.result;
        imgElement.style.display = 'block';
        document.querySelector('.remove-image-btn').style.display = 'flex';
    }
    reader.readAsDataURL(imageFiles[index]);
    currentImageIndex = index;
}

function prevImage() {
    if (currentImageIndex > 0) {
        displayImage(currentImageIndex - 1);
    }
}

function nextImage() {
    if (currentImageIndex < imageFiles.length - 1) {
        displayImage(currentImageIndex + 1);
    }
}

function removeImage() {
    imageFiles.splice(currentImageIndex, 1);
    if (imageFiles.length > 0) {
        if (currentImageIndex === imageFiles.length) {
            currentImageIndex--;
        }
        displayImage(currentImageIndex);
    } else {
        const imgElement = document.getElementById('current-image');
        imgElement.src = '';
        imgElement.style.display = 'none';
        document.querySelector('.remove-image-btn').style.display = 'none';
        document.getElementById('upload_text').style.display = 'block';
    }
}

document.querySelectorAll('select').forEach(select => {
    select.addEventListener('change', function () {
        const parent = this.closest('.form-group');
        if (this.id === 'electric' || this.id === 'water' || this.id === 'management_fee' || this.id === 'internet') {
            if (this.value === 'false') {
                parent.querySelector('.additional-fee').style.display = 'block';
            } else {
                parent.querySelector('.additional-fee').style.display = 'none';
            }
        } else if (this.id === 'negotiation') {
            if (this.value === 'true') {
                parent.querySelector('.negotiation-price').style.display = 'block';
            } else {
                parent.querySelector('.negotiation-price').style.display = 'none';
            }
        }
    });
});

async function compressImage(file) {
    const img = document.createElement("img");
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");

    return new Promise((resolve, reject) => {
        img.onload = () => {
            let width = img.width;
            let height = img.height;

            const max_size = 1024;
            if (width > height) {
                if (width > max_size) {
                    height *= max_size / width;
                    width = max_size;
                }
            } else {
                if (height > max_size) {
                    width *= max_size / height;
                    height = max_size;
                }
            }

            canvas.width = width;
            canvas.height = height;
            ctx.drawImage(img, 0, 0, width, height);
            canvas.toBlob((blob) => {
                resolve(blob);
            }, 'image/jpeg', 0.7);
        };

        img.onerror = (error) => {
            reject(error);
        };

        img.src = URL.createObjectURL(file);
    });
}

function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

document.getElementById('property-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const alertSuccess = document.getElementById('alert-success');
    const alertError = document.getElementById('alert-error');
    const files = imageFiles;

    try {
        const compressedFilesPromises = files.map(async file => {
            if (file.size > 5 * 1024 * 1024) {
                const compressedBlob = await compressImage(file);
                return new File([compressedBlob], file.name, {type: 'image/jpeg'});
            }
            return file;
        });

        const compressedFiles = await Promise.all(compressedFilesPromises);

        const base64FilesPromises = compressedFiles.map(file => fileToBase64(file));
        const base64Files = await Promise.all(base64FilesPromises);

        formData.delete('images');
        base64Files.forEach((base64, index) => {
            formData.append('images', base64);
        });

        const response = await fetch('/api/v1/rent/management/new', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            alertSuccess.textContent = '租屋物件建立成功!';
            alertSuccess.style.display = 'block';
            alertError.style.display = 'none';
            setTimeout(() => {
                window.location.href = result.redirect_url;
            }, 2000);
        } else {
            alertError.textContent = `建立租屋物件時發生錯誤: ${result.error}`;
            alertError.style.display = 'block';
            alertSuccess.style.display = 'none';
        }
    } catch (error) {
        alertError.textContent = `建立租屋物件時發生錯誤: ${error.message}`;
        alertError.style.display = 'block';
        alertSuccess.style.display = 'none';
    }
});

document.querySelectorAll('select').forEach(select => {
    const parent = select.closest('.form-group');
    if (select.id === 'electric' || select.id === 'water' || select.id === 'management_fee' || select.id === 'internet') {
        if (select.value === 'false') {
            parent.querySelector('.additional-fee').style.display = 'block';
        } else {
            parent.querySelector('.additional-fee').style.display = 'none';
        }
    }
    if (select.id === 'negotiation' && select.value === 'true') {
        parent.querySelector('.negotiation-price').style.display = 'block';
    }
});

document.getElementById('image-upload-preview').addEventListener('click', function () {
    document.getElementById('images').click();
});

function handleFiles(files) {
    document.getElementById('upload_text').style.display = 'none';
    imageFiles = Array.from(files);
    if (imageFiles.length > 0) {
        displayImage(0);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    document.getElementById('image-upload-preview').classList.add('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    document.getElementById('image-upload-preview').classList.remove('dragover');
    handleFiles(event.dataTransfer.files);
}

document.getElementById('image-upload-preview').addEventListener('dragleave', function () {
    this.classList.remove('dragover');
});