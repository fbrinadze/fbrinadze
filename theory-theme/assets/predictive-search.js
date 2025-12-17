/**
 * Theory-inspired Shopify Theme - Predictive Search JavaScript
 * Handles search suggestions functionality
 */

class PredictiveSearch {
  constructor() {
    this.input = document.querySelector('[data-search-input]');
    this.results = document.querySelector('[data-predictive-search]');
    this.debounceTimeout = null;

    this.init();
  }

  init() {
    if (!this.input || !this.results) return;

    this.input.addEventListener('input', (e) => {
      this.debounce(() => this.search(e.target.value), 300);
    });
  }

  debounce(callback, delay) {
    clearTimeout(this.debounceTimeout);
    this.debounceTimeout = setTimeout(callback, delay);
  }

  async search(query) {
    if (query.length < 2) {
      this.results.innerHTML = '';
      return;
    }

    try {
      const response = await fetch(`/search/suggest.json?q=${encodeURIComponent(query)}&resources[type]=product&resources[limit]=6`);
      const data = await response.json();

      this.renderResults(data.resources.results.products);
    } catch (error) {
      console.error('Predictive search error:', error);
    }
  }

  renderResults(products) {
    if (!products || products.length === 0) {
      this.results.innerHTML = '<p class="predictive-search__no-results">No results found</p>';
      return;
    }

    const html = products.map(product => `
      <a href="${product.url}" class="predictive-search__item">
        <div class="predictive-search__image">
          ${product.featured_image?.url ? `<img src="${product.featured_image.url}&width=80" alt="${product.title}" loading="lazy">` : ''}
        </div>
        <div class="predictive-search__content">
          <h4 class="predictive-search__title">${product.title}</h4>
          <p class="predictive-search__price">${this.formatMoney(product.price_min)}</p>
        </div>
      </a>
    `).join('');

    this.results.innerHTML = `<div class="predictive-search__results">${html}</div>`;
  }

  formatMoney(cents) {
    return '$' + (cents / 100).toFixed(2);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new PredictiveSearch();
});
