document.addEventListener('DOMContentLoaded', () => {
  initProductGallery();
});

function initProductGallery() {
  const image = document.getElementById('mainProductImg');
  const buttons = document.querySelectorAll('[data-product-src]');

  if (!image || !buttons.length) return;

  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      image.src = button.dataset.productSrc;
      image.alt = button.dataset.productAlt;

      buttons.forEach((item) => {
        const selected = item === button;
        item.classList.toggle('active', selected);
        item.setAttribute('aria-pressed', String(selected));
      });
    });
  });
}
