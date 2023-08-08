const fileInput = document.getElementById('file-input');
const uploadedFilesList = document.getElementById('uploaded-files-list');
const dragDropArea = document.getElementById('drag-drop-area');
const fileCountElement = document.getElementById('file-count');

fileInput.addEventListener('change', updateUploadedFilesList);
dragDropArea.addEventListener('dragover', handleDragOver);
dragDropArea.addEventListener('dragleave', handleDragLeave);
dragDropArea.addEventListener('drop', handleDrop);
dragDropArea.addEventListener('click', openFileInput);

function updateUploadedFilesList(event) {
    uploadedFilesList.innerHTML = '';
    const files = event.target.files;
    fileCountElement.textContent = files.length;
    if (files.length > 0) {
        for (const file of files) {
            const fileItem = document.createElement('div');
            fileItem.textContent = file.name;
            uploadedFilesList.appendChild(fileItem);
        }
    }
}

function handleDragOver(event) {
    event.preventDefault();
    dragDropArea.classList.add('drag-over');
}

function handleDragLeave(event) {
    event.preventDefault();
    dragDropArea.classList.remove('drag-over');
}

function handleDrop(event) {
    event.preventDefault();
    dragDropArea.classList.remove('drag-over');
    fileInput.files = event.dataTransfer.files;
    updateUploadedFilesList(event);
}

function openFileInput() {
    fileInput.click();
}

document.addEventListener("DOMContentLoaded", function () {
    const mobileMenuToggle = document.querySelector(".mobile-menu-toggle");
    const sidebar = document.querySelector(".sidebar");
  
    mobileMenuToggle.addEventListener("click", function () {
      sidebar.classList.toggle("sidebar-open");
      document.body.classList.toggle("sidebar-open"); // Füge diese Zeile hinzu
      mobileMenuToggle.classList.toggle("open");
    });
});
