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

// ---- Cart: update quantity without reloading ----
const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');

document.querySelectorAll('.table .qty-input').forEach(input => {
  input.addEventListener('change', async () => {
    const row = input.closest('tr');
    const res = await fetch(input.dataset.url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrfInput.value,
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: new URLSearchParams({ quantity: input.value }),
    });
    const data = await res.json();

    if (data.removed) row.remove();
    else row.querySelector('.subtotal').textContent = data.subtotal;

    document.getElementById('cart-total').textContent = data.total;
    document.getElementById('cart-count').textContent = data.count;
    if (data.count === 0) location.reload();
  });
});