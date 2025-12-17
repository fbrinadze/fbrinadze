/**
 * Theory-inspired Shopify Theme - Global JavaScript
 * Handles core functionality: mobile menu, search, cart drawer, etc.
 */

// ===== Mobile Navigation =====
class MobileNav {
  constructor() {
    this.menuToggle = document.querySelector('[data-menu-toggle]');
    this.menuClose = document.querySelector('[data-menu-close]');
    this.mobileNav = document.querySelector('[data-mobile-nav]');
    this.overlay = document.querySelector('[data-mobile-overlay]');
    this.submenuToggles = document.querySelectorAll('[data-mobile-submenu-toggle]');
    this.submenuBacks = document.querySelectorAll('[data-mobile-submenu-back]');

    this.init();
  }

  init() {
    if (this.menuToggle) {
      this.menuToggle.addEventListener('click', () => this.open());
    }

    if (this.menuClose) {
      this.menuClose.addEventListener('click', () => this.close());
    }

    if (this.overlay) {
      this.overlay.addEventListener('click', () => this.close());
    }

    this.submenuToggles.forEach(toggle => {
      toggle.addEventListener('click', (e) => this.openSubmenu(e));
    });

    this.submenuBacks.forEach(back => {
      back.addEventListener('click', (e) => this.closeSubmenu(e));
    });

    // Close on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        this.close();
      }
    });
  }

  open() {
    this.mobileNav?.classList.add('is-open');
    this.overlay?.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  }

  close() {
    this.mobileNav?.classList.remove('is-open');
    this.overlay?.classList.remove('is-open');
    document.body.style.overflow = '';

    // Close all submenus
    document.querySelectorAll('.header__mobile-nav-item.is-open').forEach(item => {
      item.classList.remove('is-open');
    });
  }

  openSubmenu(e) {
    const item = e.target.closest('.header__mobile-nav-item');
    item?.classList.add('is-open');
  }

  closeSubmenu(e) {
    const item = e.target.closest('.header__mobile-nav-item');
    item?.classList.remove('is-open');
  }
}

// ===== Search Modal =====
class SearchModal {
  constructor() {
    this.toggle = document.querySelector('[data-search-toggle]');
    this.modal = document.querySelector('[data-search-modal]');
    this.close = document.querySelectorAll('[data-search-modal-close]');
    this.input = document.querySelector('[data-search-input]');

    this.init();
  }

  init() {
    if (this.toggle) {
      this.toggle.addEventListener('click', () => this.open());
    }

    this.close.forEach(btn => {
      btn.addEventListener('click', () => this.closeModal());
    });

    // Close on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.modal?.getAttribute('aria-hidden') === 'false') {
        this.closeModal();
      }
    });
  }

  open() {
    this.modal?.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    setTimeout(() => {
      this.input?.focus();
    }, 100);
  }

  closeModal() {
    this.modal?.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }
}

// ===== Cart Drawer =====
class CartDrawer {
  constructor() {
    this.toggle = document.querySelector('[data-cart-toggle]');
    this.drawer = document.querySelector('[data-cart-drawer]');
    this.close = document.querySelectorAll('[data-cart-drawer-close]');

    this.init();
  }

  init() {
    if (this.toggle) {
      this.toggle.addEventListener('click', (e) => {
        e.preventDefault();
        this.open();
      });
    }

    this.close.forEach(btn => {
      btn.addEventListener('click', () => this.closeDrawer());
    });

    // Close on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.drawer?.getAttribute('aria-hidden') === 'false') {
        this.closeDrawer();
      }
    });

    // Handle quantity changes
    this.drawer?.addEventListener('click', (e) => {
      const quantityBtn = e.target.closest('[data-quantity-change]');
      if (quantityBtn) {
        this.handleQuantityChange(quantityBtn);
      }

      const removeBtn = e.target.closest('[data-cart-remove]');
      if (removeBtn) {
        this.handleRemove(removeBtn);
      }
    });
  }

  open() {
    this.drawer?.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  closeDrawer() {
    this.drawer?.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  async handleQuantityChange(btn) {
    const key = btn.dataset.quantityChange;
    const action = btn.dataset.quantityAction;
    const item = btn.closest('[data-cart-item]');
    const valueEl = item.querySelector('[data-quantity-value]');
    let quantity = parseInt(valueEl.textContent);

    if (action === 'plus') {
      quantity++;
    } else if (action === 'minus' && quantity > 0) {
      quantity--;
    }

    await this.updateCart(key, quantity);
  }

  async handleRemove(btn) {
    const key = btn.dataset.cartRemove;
    await this.updateCart(key, 0);
  }

  async updateCart(key, quantity) {
    try {
      const response = await fetch('/cart/change.js', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: key, quantity })
      });

      if (response.ok) {
        // Refresh the page to update cart
        window.location.reload();
      }
    } catch (error) {
      console.error('Error updating cart:', error);
    }
  }
}

// ===== Dropdown Navigation =====
class DropdownNav {
  constructor() {
    this.dropdownToggles = document.querySelectorAll('.header__nav-link--dropdown');
    this.init();
  }

  init() {
    this.dropdownToggles.forEach(toggle => {
      toggle.addEventListener('click', (e) => {
        e.preventDefault();
        const expanded = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', !expanded);
      });
    });
  }
}

// ===== Quantity Selectors =====
class QuantitySelector {
  constructor() {
    this.selectors = document.querySelectorAll('.main-product__quantity-wrapper, .main-cart__quantity-wrapper');
    this.init();
  }

  init() {
    this.selectors.forEach(selector => {
      const minusBtn = selector.querySelector('[data-quantity-minus]');
      const plusBtn = selector.querySelector('[data-quantity-plus]');
      const input = selector.querySelector('input');

      if (minusBtn && input) {
        minusBtn.addEventListener('click', () => {
          const currentValue = parseInt(input.value);
          if (currentValue > parseInt(input.min || 1)) {
            input.value = currentValue - 1;
            input.dispatchEvent(new Event('change'));
          }
        });
      }

      if (plusBtn && input) {
        plusBtn.addEventListener('click', () => {
          const currentValue = parseInt(input.value);
          const max = parseInt(input.max || 99);
          if (currentValue < max) {
            input.value = currentValue + 1;
            input.dispatchEvent(new Event('change'));
          }
        });
      }
    });
  }
}

// ===== Product Variant Selector =====
class VariantSelector {
  constructor() {
    this.container = document.querySelector('.main-product__variants');
    this.form = document.querySelector('#product-form');
    this.product = window.product || null;

    this.init();
  }

  init() {
    if (!this.container || !this.product) return;

    this.container.addEventListener('click', (e) => {
      const btn = e.target.closest('.main-product__option-button');
      if (!btn) return;

      // Update active state
      const optionGroup = btn.closest('.main-product__option-values');
      optionGroup.querySelectorAll('.main-product__option-button').forEach(b => {
        b.classList.remove('is-active');
      });
      btn.classList.add('is-active');

      // Update option value display
      const optionName = btn.dataset.optionName;
      const optionValue = btn.dataset.optionValue;
      const valueDisplay = this.container.querySelector(`[data-option-value="${optionName}"]`);
      if (valueDisplay) {
        valueDisplay.textContent = optionValue;
      }

      // Find and select the matching variant
      this.updateVariant();
    });
  }

  updateVariant() {
    const selectedOptions = [];
    this.container.querySelectorAll('.main-product__option').forEach(option => {
      const activeBtn = option.querySelector('.main-product__option-button.is-active');
      if (activeBtn) {
        selectedOptions.push(activeBtn.dataset.optionValue);
      }
    });

    // Find matching variant
    const variant = this.product.variants.find(v => {
      return v.options.every((opt, index) => opt === selectedOptions[index]);
    });

    if (variant) {
      // Update form
      const variantInput = this.form?.querySelector('[name="id"]');
      if (variantInput) {
        variantInput.value = variant.id;
      }

      // Update URL
      const url = new URL(window.location);
      url.searchParams.set('variant', variant.id);
      window.history.replaceState({}, '', url);

      // Update price
      this.updatePrice(variant);

      // Update button state
      this.updateButton(variant);
    }
  }

  updatePrice(variant) {
    const priceEl = document.querySelector('.main-product__price');
    if (!priceEl) return;

    const regularPrice = priceEl.querySelector('.main-product__price-regular');
    const comparePrice = priceEl.querySelector('.main-product__price-compare');
    const badge = priceEl.querySelector('.main-product__price-badge');

    if (regularPrice) {
      regularPrice.textContent = this.formatMoney(variant.price);
      regularPrice.classList.toggle('main-product__price-regular--sale', variant.compare_at_price > variant.price);
    }

    if (comparePrice) {
      if (variant.compare_at_price > variant.price) {
        comparePrice.textContent = this.formatMoney(variant.compare_at_price);
        comparePrice.style.display = '';
      } else {
        comparePrice.style.display = 'none';
      }
    }

    if (badge) {
      badge.style.display = variant.compare_at_price > variant.price ? '' : 'none';
    }
  }

  updateButton(variant) {
    const button = document.querySelector('.main-product__add-button');
    if (!button) return;

    if (variant.available) {
      button.disabled = false;
      button.textContent = 'Add to Cart';
    } else {
      button.disabled = true;
      button.textContent = 'Sold Out';
    }
  }

  formatMoney(cents) {
    return '$' + (cents / 100).toFixed(2);
  }
}

// ===== Quick Add =====
class QuickAdd {
  constructor() {
    this.init();
  }

  init() {
    document.addEventListener('click', async (e) => {
      const btn = e.target.closest('[data-quick-add]');
      if (!btn) return;

      e.preventDefault();
      const variantId = btn.dataset.quickAdd;

      btn.disabled = true;
      btn.innerHTML = '<span class="icon-spinner"></span>';

      try {
        await this.addToCart(variantId);
        // Open cart drawer
        const cartDrawer = document.querySelector('[data-cart-drawer]');
        cartDrawer?.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        // Refresh to update cart
        window.location.reload();
      } catch (error) {
        console.error('Error adding to cart:', error);
        btn.disabled = false;
        btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10 4V16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M4 10H16" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>';
      }
    });
  }

  async addToCart(variantId) {
    const response = await fetch('/cart/add.js', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        items: [{
          id: variantId,
          quantity: 1
        }]
      })
    });

    if (!response.ok) {
      throw new Error('Failed to add to cart');
    }

    return response.json();
  }
}

// ===== Collection Filters =====
class CollectionFilters {
  constructor() {
    this.filterToggle = document.querySelector('[data-filter-toggle]');
    this.sidebar = document.querySelector('[data-filter-sidebar]');
    this.overlay = document.querySelector('[data-filter-overlay]');
    this.close = document.querySelector('[data-filter-close]');
    this.sortSelect = document.querySelector('[data-sort-select]');

    this.init();
  }

  init() {
    if (this.filterToggle) {
      this.filterToggle.addEventListener('click', () => this.openFilters());
    }

    if (this.close) {
      this.close.addEventListener('click', () => this.closeFilters());
    }

    if (this.overlay) {
      this.overlay.addEventListener('click', () => this.closeFilters());
    }

    if (this.sortSelect) {
      this.sortSelect.addEventListener('change', (e) => {
        const url = new URL(window.location);
        url.searchParams.set('sort_by', e.target.value);
        window.location = url.toString();
      });
    }
  }

  openFilters() {
    this.sidebar?.classList.add('is-open');
    this.overlay?.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  }

  closeFilters() {
    this.sidebar?.classList.remove('is-open');
    this.overlay?.classList.remove('is-open');
    document.body.style.overflow = '';
  }
}

// ===== Product Recommendations =====
class ProductRecommendations {
  constructor() {
    this.container = document.querySelector('[data-section-type="product-recommendations"]');
    this.init();
  }

  init() {
    if (!this.container) return;

    const url = this.container.dataset.url;
    if (!url) return;

    fetch(url)
      .then(response => response.text())
      .then(text => {
        const html = document.createElement('div');
        html.innerHTML = text;
        const recommendations = html.querySelector('[data-section-type="product-recommendations"]');
        if (recommendations && recommendations.innerHTML.trim()) {
          this.container.innerHTML = recommendations.innerHTML;
        }
      })
      .catch(error => {
        console.error('Error loading product recommendations:', error);
      });
  }
}

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', () => {
  new MobileNav();
  new SearchModal();
  new CartDrawer();
  new DropdownNav();
  new QuantitySelector();
  new VariantSelector();
  new QuickAdd();
  new CollectionFilters();
  new ProductRecommendations();
});
