document.addEventListener('DOMContentLoaded', () => {
  const menuButton = document.getElementById('menuButton');
  const sidebar = document.getElementById('sidebar');
  menuButton?.addEventListener('click', () => sidebar.classList.toggle('open'));

  document.querySelectorAll('.flash-close').forEach((button) => {
    button.addEventListener('click', () => button.parentElement.remove());
  });

  const form = document.getElementById('transactionForm');
  if (!form) return;
  form.addEventListener('submit', (event) => {
    let valid = true;
    form.querySelectorAll('[required]').forEach((input) => {
      const field = input.closest('.field');
      const error = field?.querySelector('.field-error');
      const empty = !input.value.trim();
      const invalidAmount = input.name === 'amount' && Number(input.value) <= 0;
      if (empty || invalidAmount) {
        valid = false;
        field?.classList.add('invalid');
        if (error) error.textContent = invalidAmount ? 'Enter an amount greater than ₹0.' : 'This field is required.';
      } else {
        field?.classList.remove('invalid');
        if (error) error.textContent = '';
      }
    });
    if (!valid) event.preventDefault();
  });
});
