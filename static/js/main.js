const fileInput = document.querySelector('input[type="file"]');
const preview = document.getElementById('image-preview');

if (fileInput && preview) {
  fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file) {
      preview.src = URL.createObjectURL(file);
      preview.style.display = 'block';
    }
  });
}