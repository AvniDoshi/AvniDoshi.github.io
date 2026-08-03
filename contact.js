const fileInput = document.querySelector('#contact-files');
const fileSummary = document.querySelector('#attachment-summary');
const selectedFilesList = document.querySelector('#selected-files');
let selectedFiles = [];

const fileKey = (file) => `${file.name}-${file.size}-${file.lastModified}`;

const formatFileSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

const syncInputFiles = () => {
    const transfer = new DataTransfer();
    selectedFiles.forEach((file) => transfer.items.add(file));
    fileInput.files = transfer.files;
};

const renderSelectedFiles = () => {
    selectedFilesList.replaceChildren();
    fileSummary.textContent = selectedFiles.length
        ? `${selectedFiles.length} file${selectedFiles.length === 1 ? '' : 's'} selected`
        : 'No files selected';

    selectedFiles.forEach((file) => {
        const item = document.createElement('li');
        const details = document.createElement('span');
        const name = document.createElement('strong');
        const size = document.createElement('small');
        const removeButton = document.createElement('button');

        name.textContent = file.name;
        size.textContent = formatFileSize(file.size);
        details.append(name, size);

        removeButton.type = 'button';
        removeButton.textContent = 'Remove';
        removeButton.setAttribute('aria-label', `Remove ${file.name}`);
        removeButton.addEventListener('click', () => {
            selectedFiles = selectedFiles.filter((selectedFile) => fileKey(selectedFile) !== fileKey(file));
            syncInputFiles();
            renderSelectedFiles();
        });

        item.append(details, removeButton);
        selectedFilesList.append(item);
    });
};

fileInput.addEventListener('change', () => {
    const existingKeys = new Set(selectedFiles.map(fileKey));
    Array.from(fileInput.files).forEach((file) => {
        if (!existingKeys.has(fileKey(file))) {
            selectedFiles.push(file);
            existingKeys.add(fileKey(file));
        }
    });
    syncInputFiles();
    renderSelectedFiles();
});
