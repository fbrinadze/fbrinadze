/**
 * Theory-inspired Shopify Theme - Cart JavaScript
 * Handles cart page functionality
 */

class CartPage {
  constructor() {
    this.form = document.querySelector('.main-cart__form');
    this.items = document.querySelectorAll('.main-cart__item');

    this.init();
  }

  init() {
    if (!this.form) return;

    // Handle quantity changes
    this.items.forEach(item => {
      const minusBtn = item.querySelector('[data-quantity-minus]');
      const plusBtn = item.querySelector('[data-quantity-plus]');
      const input = item.querySelector('[data-quantity-input]');
      const removeBtn = item.querySelector('[data-cart-remove]');

      if (minusBtn && input) {
        minusBtn.addEventListener('click', () => {
          const currentValue = parseInt(input.value);
          if (currentValue > 0) {
            input.value = currentValue - 1;
          }
        });
      }

      if (plusBtn && input) {
        plusBtn.addEventListener('click', () => {
          const currentValue = parseInt(input.value);
          input.value = currentValue + 1;
        });
      }

      if (removeBtn && input) {
        removeBtn.addEventListener('click', () => {
          input.value = 0;
          this.form.submit();
        });
      }
    });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new CartPage();
});
