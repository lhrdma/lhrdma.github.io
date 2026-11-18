const button = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.nav-row');
button.addEventListener('click', () => {
  const expanded = button.getAttribute('aria-expanded') === 'true';
  button.setAttribute('aria-expanded', String(!expanded));
  button.textContent = expanded ? '菜单' : '收起';
  navigation.classList.toggle('is-open', !expanded);
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {
    button.click();
    button.focus();
  }
});
document.querySelectorAll('.nav-row a').forEach((link) => {
  link.addEventListener('click', () => {
    if (button.getAttribute('aria-expanded') === 'true') button.click();
  });
});
document.querySelectorAll('.proto-table-wrap').forEach((region, index) => {
  region.tabIndex = 0;
  region.setAttribute('role', 'region');
  region.setAttribute('aria-label', `实验数据表 ${index + 1}，可横向滚动`);
});
