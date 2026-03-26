/**
 * SlidePresentation — vanilla JS navigation for HTML slide decks.
 * No external dependencies. Drop in and initialise:
 *   new SlidePresentation('.slide-deck')
 *
 * Features
 * ────────
 * • Keyboard navigation  : ArrowLeft/Right, Space (next), Escape (overview)
 * • Touch / swipe        : horizontal swipe left/right
 * • Intersection Observer: adds `.visible` to slides entering the viewport
 * • Progress bar         : fixed bottom bar showing current / total progress
 * • Navigation dots      : clickable dots for direct slide access
 * • Hash navigation      : updates URL hash as #slide-N and restores on load
 */
class SlidePresentation {
  /**
   * @param {string} containerSelector  CSS selector for the scrolling viewport,
   *                                    e.g. '.slide-deck' or '#deckViewport'
   */
  constructor(containerSelector) {
    this._container = document.querySelector(containerSelector);
    if (!this._container) {
      console.warn('[SlidePresentation] Container not found:', containerSelector);
      return;
    }

    this._slides      = Array.from(this._container.querySelectorAll('.slide'));
    this._total       = this._slides.length;
    this._current     = 0;
    this._isOverview  = false;

    // Internal refs to created / adopted UI elements
    this._progressBar    = null;
    this._dotsContainer  = null;
    this._dots           = [];

    // Debounce handle for scroll events
    this._scrollTimer  = null;
    // Touch tracking
    this._touchStartX  = null;
    this._touchStartY  = null;

    this._buildUI();
    this._bindKeyboard();
    this._bindTouch();
    this._bindScroll();
    this._bindIntersectionObserver();
    this._initFromHash();
  }

  // ── Public API ─────────────────────────────────────────────────────────────

  /** Navigate to slide by 0-based index. */
  goTo(index) {
    index = Math.max(0, Math.min(index, this._total - 1));
    if (this._isOverview) this._closeOverview();
    this._slides[index].scrollIntoView({ behavior: 'smooth', block: 'start' });
    this._updateUI(index);
  }

  next() { this.goTo(this._current + 1); }
  prev() { this.goTo(this._current - 1); }

  /** Toggle the slide grid overview (Escape key). */
  toggleOverview() {
    this._isOverview ? this._closeOverview() : this._openOverview();
  }

  // ── UI Construction ────────────────────────────────────────────────────────

  _buildUI() {
    this._adoptOrCreateProgressBar();
    this._createNavDots();
  }

  /**
   * Re-use the static #deckProgress element if it exists (so the HTML author
   * can keep their markup), otherwise create a fresh bar. Either way, we move
   * it to the bottom of the viewport.
   */
  _adoptOrCreateProgressBar() {
    const existing = document.getElementById('deckProgress');
    if (existing) {
      this._progressBar = existing;
    } else {
      this._progressBar = document.createElement('div');
      this._progressBar.id = 'slideNavProgress';
      this._progressBar.setAttribute('role', 'progressbar');
      this._progressBar.setAttribute('aria-valuemin', '0');
      this._progressBar.setAttribute('aria-valuemax', '100');
      document.body.appendChild(this._progressBar);
    }

    // Position at bottom regardless of original CSS
    Object.assign(this._progressBar.style, {
      position   : 'fixed',
      bottom     : '0',
      top        : 'unset',
      left       : '0',
      width      : '0%',
      height     : '3px',
      background : 'var(--accent, #E8861A)',
      transition : 'width 0.3s ease',
      zIndex     : '201',
      borderRadius: '2px 2px 0 0',
    });
  }

  _createNavDots() {
    this._dotsContainer = document.createElement('div');
    this._dotsContainer.className = 'slide-nav-dots';
    this._dotsContainer.setAttribute('role', 'navigation');
    this._dotsContainer.setAttribute('aria-label', 'Slide navigation');

    Object.assign(this._dotsContainer.style, {
      position   : 'fixed',
      bottom     : '18px',
      left       : '50%',
      transform  : 'translateX(-50%)',
      display    : 'flex',
      gap        : '7px',
      alignItems : 'center',
      zIndex     : '202',
    });

    this._slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.setAttribute('aria-label', 'Go to slide ' + (i + 1));
      dot.setAttribute('aria-current', 'false');

      Object.assign(dot.style, {
        width        : '8px',
        height       : '8px',
        borderRadius : '50%',
        border       : '2px solid rgba(255,255,255,0.65)',
        background   : 'transparent',
        cursor       : 'pointer',
        padding      : '0',
        outline      : 'none',
        transition   : 'all 0.2s ease',
        flexShrink   : '0',
      });

      dot.addEventListener('click', () => this.goTo(i));
      dot.addEventListener('mouseenter', () => {
        if (i !== this._current) {
          dot.style.background = 'rgba(255,255,255,0.45)';
        }
      });
      dot.addEventListener('mouseleave', () => {
        if (i !== this._current) {
          dot.style.background = 'transparent';
        }
      });

      this._dotsContainer.appendChild(dot);
      this._dots.push(dot);
    });

    document.body.appendChild(this._dotsContainer);
  }

  // ── Event Binding ──────────────────────────────────────────────────────────

  _bindKeyboard() {
    document.addEventListener('keydown', (e) => {
      // Ignore when user is typing in an input/textarea
      if (e.target.matches('input, textarea, select, [contenteditable]')) return;

      switch (e.key) {
        case 'ArrowRight':
        case 'ArrowDown':
          e.preventDefault();
          this.next();
          break;
        case 'ArrowLeft':
        case 'ArrowUp':
          e.preventDefault();
          this.prev();
          break;
        case ' ':
          e.preventDefault();
          this.next();
          break;
        case 'Escape':
          e.preventDefault();
          this.toggleOverview();
          break;
        case 'Home':
          e.preventDefault();
          this.goTo(0);
          break;
        case 'End':
          e.preventDefault();
          this.goTo(this._total - 1);
          break;
      }
    });
  }

  _bindTouch() {
    // Detect horizontal swipe (left/right) without interfering with
    // the native vertical scroll-snap behaviour of the container.
    this._container.addEventListener('touchstart', (e) => {
      const t = e.changedTouches[0];
      this._touchStartX = t.clientX;
      this._touchStartY = t.clientY;
    }, { passive: true });

    this._container.addEventListener('touchend', (e) => {
      if (this._touchStartX === null) return;
      const dx = this._touchStartX - e.changedTouches[0].clientX;
      const dy = this._touchStartY - e.changedTouches[0].clientY;

      // Only act on predominantly horizontal gestures with sufficient distance
      if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 44) {
        dx > 0 ? this.next() : this.prev();
      }

      this._touchStartX = null;
      this._touchStartY = null;
    }, { passive: true });
  }

  _bindScroll() {
    // Keep UI in sync as the user free-scrolls (e.g. on mobile / trackpad)
    this._container.addEventListener('scroll', () => {
      if (this._scrollTimer) clearTimeout(this._scrollTimer);
      this._scrollTimer = setTimeout(() => {
        const idx = this._detectCurrentSlide();
        if (idx !== this._current) this._updateUI(idx);
      }, 80);
    }, { passive: true });
  }

  _bindIntersectionObserver() {
    if (!('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          // Slide entered the viewport — mark visible for CSS transitions
          entry.target.classList.add('visible');
        }
      });
    }, {
      root      : this._container,
      threshold : 0.45,   // slide must be ~half visible before triggering
    });

    this._slides.forEach(slide => observer.observe(slide));
  }

  // ── Hash Navigation ────────────────────────────────────────────────────────

  _initFromHash() {
    const match = window.location.hash.match(/^#slide-(\d+)$/);
    if (match) {
      const idx = parseInt(match[1], 10) - 1;
      if (idx > 0 && idx < this._total) {
        // Small delay lets the browser finish its initial layout / scroll
        setTimeout(() => this.goTo(idx), 120);
        return;
      }
    }
    this._updateUI(0);
  }

  _updateHash(index) {
    const tag = '#slide-' + (index + 1);
    if (window.location.hash !== tag) {
      history.replaceState(null, '', tag);
    }
  }

  // ── Internal State ─────────────────────────────────────────────────────────

  /** Find which slide occupies the centre of the container viewport. */
  _detectCurrentSlide() {
    const vh = this._container.clientHeight;
    for (let i = 0; i < this._slides.length; i++) {
      const rect = this._slides[i].getBoundingClientRect();
      if (rect.top >= -vh * 0.4 && rect.top <= vh * 0.6) return i;
    }
    return this._current;
  }

  /** Synchronise all UI chrome to the given 0-based slide index. */
  _updateUI(index) {
    this._current = index;

    // ── Progress bar ─────────────────────────────────────────────────────
    const pct = this._total > 1 ? ((index + 1) / this._total) * 100 : 100;
    this._progressBar.style.width = pct + '%';
    this._progressBar.setAttribute('aria-valuenow', Math.round(pct));

    // ── Nav dots ──────────────────────────────────────────────────────────
    this._dots.forEach((dot, i) => {
      const active = i === index;
      Object.assign(dot.style, {
        width       : active ? '22px' : '8px',
        borderRadius: active ? '4px'  : '50%',
        background  : active ? 'var(--accent, #E8861A)' : 'transparent',
        borderColor : active ? 'var(--accent, #E8861A)' : 'rgba(255,255,255,0.65)',
      });
      dot.setAttribute('aria-current', active ? 'true' : 'false');
    });

    // ── HUD counter (static element, optional) ────────────────────────────
    const hud = document.getElementById('deckHud');
    if (hud) hud.textContent = (index + 1) + ' / ' + this._total;

    // ── URL hash ──────────────────────────────────────────────────────────
    this._updateHash(index);
  }

  // ── Overview Mode (Escape) ─────────────────────────────────────────────────

  _openOverview() {
    this._isOverview = true;

    let overlay = document.getElementById('slideNavOverview');
    if (overlay) {
      overlay.style.display = 'grid';
      return;
    }

    overlay = document.createElement('div');
    overlay.id = 'slideNavOverview';
    Object.assign(overlay.style, {
      position        : 'fixed',
      inset           : '0',
      background      : 'rgba(10,15,25,0.88)',
      backdropFilter  : 'blur(10px)',
      zIndex          : '300',
      display         : 'grid',
      gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
      gap             : '20px',
      padding         : '36px',
      overflowY       : 'auto',
    });

    // Close on bare overlay click
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) this._closeOverview();
    });

    // ESC closes
    const escHandler = (e) => {
      if (e.key === 'Escape') {
        this._closeOverview();
        document.removeEventListener('keydown', escHandler);
      }
    };
    document.addEventListener('keydown', escHandler);

    this._slides.forEach((slide, i) => {
      const thumb = document.createElement('button');
      thumb.type = 'button';
      thumb.setAttribute('aria-label', 'Go to slide ' + (i + 1));

      const isActive = i === this._current;
      Object.assign(thumb.style, {
        background   : 'var(--bg-primary, #fff)',
        border       : isActive
          ? '3px solid var(--accent, #E8861A)'
          : '3px solid rgba(255,255,255,0.12)',
        borderRadius : '6px',
        overflow     : 'hidden',
        cursor       : 'pointer',
        padding      : '14px 16px',
        aspectRatio  : '16 / 9',
        display      : 'flex',
        flexDirection: 'column',
        alignItems   : 'flex-start',
        justifyContent: 'flex-start',
        transition   : 'transform 0.18s ease, border-color 0.18s ease',
        color        : 'var(--text-primary, #0D1B2A)',
        fontFamily   : 'var(--font-body, sans-serif)',
        textAlign    : 'left',
      });

      // Slide number
      const num = document.createElement('span');
      Object.assign(num.style, {
        fontSize   : '9px',
        fontWeight : '700',
        letterSpacing: '0.08em',
        color      : 'var(--text-secondary, #5A6A7A)',
        marginBottom: '6px',
        display    : 'block',
      });
      num.textContent = 'SLIDE ' + (i + 1);

      // Title text (grab h1 if available)
      const h1 = slide.querySelector('h1');
      const title = document.createElement('span');
      Object.assign(title.style, {
        fontSize  : '11px',
        fontWeight: '600',
        lineHeight: '1.35',
        overflow  : 'hidden',
        display   : '-webkit-box',
        WebkitLineClamp: '3',
        WebkitBoxOrient: 'vertical',
      });
      title.textContent = h1 ? h1.textContent.trim().slice(0, 60) : '—';

      thumb.appendChild(num);
      thumb.appendChild(title);

      thumb.addEventListener('click', () => {
        this._closeOverview();
        this.goTo(i);
      });
      thumb.addEventListener('mouseenter', () => {
        thumb.style.transform = 'scale(1.04)';
        if (!isActive) thumb.style.borderColor = 'rgba(255,255,255,0.35)';
      });
      thumb.addEventListener('mouseleave', () => {
        thumb.style.transform = 'scale(1)';
        if (!isActive) thumb.style.borderColor = 'rgba(255,255,255,0.12)';
      });

      overlay.appendChild(thumb);
    });

    document.body.appendChild(overlay);
  }

  _closeOverview() {
    this._isOverview = false;
    const overlay = document.getElementById('slideNavOverview');
    if (overlay) overlay.style.display = 'none';
  }
}
