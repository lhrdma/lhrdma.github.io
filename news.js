const newsArchive = document.querySelector('.news-archive');
const lightbox = document.querySelector('.news-lightbox');
const lightboxCaption = lightbox.querySelector('figcaption');
const previewImage = new Image();
lightboxCaption.before(previewImage);
let previewTrigger;

newsArchive.addEventListener('click', (event) => {
  const trigger = event.target.closest('.news-card-media button');
  if (!trigger) return;

  const image = trigger.querySelector('img');
  previewTrigger = trigger;
  previewImage.src = image.currentSrc || image.src;
  previewImage.alt = image.alt;
  lightboxCaption.textContent = trigger.nextElementSibling.textContent;
  lightbox.showModal();
});

lightbox.addEventListener('click', (event) => {
  if (event.target === lightbox) lightbox.close();
});

lightbox.addEventListener('close', () => {
  if (!lightbox.open) previewTrigger?.focus({ preventScroll: true });
});
